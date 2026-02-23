"""Refund business logic service layer."""

from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from core.refunds.model_types import (
    CaseStatus,
    CaseStatusDetail,
    CaseTicketStatus,
    CaseType,
    InvoiceStatus,
)

CORE_DEVICE_CLASS_ID = 303
CORE_DEVICE_ID = 90000001


class RefundService:
    """Refund business operations — called by views.py."""

    @staticmethod
    @transaction.atomic
    def create_refund(form, ticket_formset, user):
        """Create a new refund case."""
        refund = form.save(commit=False)
        refund.case_type = CaseType.REFUND
        refund.case_status = CaseStatus.RECEIVED
        refund.originally_entered_by = user
        refund.save()
        ticket_formset.instance = refund
        ticket_formset.save()
        RefundService.add_case_log(refund, f"Case created by {user.username}.", user)
        return refund

    @staticmethod
    @transaction.atomic
    def update_refund(form, ticket_formset, user):
        """Update an existing refund, detect status changes."""
        old_status = None
        if form.instance.pk:
            from core.refunds.models import Refund
            try:
                old_status = Refund.objects.get(pk=form.instance.pk).case_status
            except Refund.DoesNotExist:
                pass

        refund = form.save(commit=False)
        refund.last_updated_by = user
        refund.save()
        ticket_formset.instance = refund
        ticket_formset.save()

        if old_status and old_status != refund.case_status:
            RefundService.add_case_log(
                refund,
                f"Status changed: {old_status} -> {refund.case_status} by {user.username}",
                user,
            )
        return refund

    @staticmethod
    def link_sales_detail(ticket, sd_info):
        """Link a RefundTicket to its original SalesDetail record."""
        ticket.sd_device_id = sd_info.get("device_id")
        ticket.sd_device_class_id = sd_info.get("device_class_id")
        ticket.sd_sales_detail_ev_sequ_no = sd_info.get("sales_detail_ev_sequ_no")
        ticket.sd_sales_transaction_no = sd_info.get("sales_transaction_no")
        ticket.sd_unique_ms_id = sd_info.get("unique_ms_id")
        ticket.sd_correction_counter = sd_info.get("correction_counter", 0)
        ticket.status = CaseTicketStatus.DETAIL_CHECKED
        ticket.save()

    @staticmethod
    def calculate_amounts(refund):
        """Recalculate total, fee, and final refund amounts."""
        tickets = refund.refund_tickets.filter(is_active=True)
        total = sum(
            (t.refund_amount or Decimal("0.00")) * (t.quantity or 1)
            for t in tickets
        )
        refund.total_amount_of_refund = total
        refund.final_refund = total - (refund.fee or Decimal("0.00"))
        refund.settlement_total = refund.final_refund
        refund.save(update_fields=["total_amount_of_refund", "final_refund", "settlement_total"])
        return refund

    @staticmethod
    @transaction.atomic
    def approve_refund(refund, user):
        """Approve refund: update status, calculate, create revenue transaction."""
        refund.case_status = CaseStatus.CLOSED
        refund.case_status_detail = CaseStatusDetail.RESOLVED
        refund.status_changed_by = user
        refund.status_date = timezone.now()
        RefundService.calculate_amounts(refund)
        refund.save()
        RefundService.add_case_log(
            refund, f"Refund APPROVED by {user.username}. Amount: ${refund.final_refund}", user
        )
        return refund

    @staticmethod
    @transaction.atomic
    def deny_refund(refund, reason, user):
        """Deny refund with reason."""
        refund.case_status = CaseStatus.CLOSED
        refund.case_status_detail = CaseStatusDetail.RESOLVED
        refund.status_changed_by = user
        refund.status_date = timezone.now()
        refund.save()
        RefundService.add_case_log(refund, f"Refund DENIED by {user.username}. Reason: {reason}", user)
        return refund

    @staticmethod
    def add_case_log(refund, message, user=None):
        """Add an activity log entry to a case."""
        from core.refunds.models import CaseLog
        return CaseLog.objects.create(refund=refund, message=message, user_new=user)

    @staticmethod
    def create_invoice(refund, user):
        """Create an invoice for an approved refund."""
        from core.refunds.models import Invoice
        invoice = Invoice.objects.create(
            refund=refund, status=InvoiceStatus.OPEN,
            net=refund.final_refund or Decimal("0.00"),
            tax=Decimal("0.00"),
            total=refund.final_refund or Decimal("0.00"),
        )
        RefundService.add_case_log(refund, f"Invoice #{invoice.pk} created. Amount: ${invoice.total}", user)
        return invoice
