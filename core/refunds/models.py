import secrets
import string

from django.conf import settings
from django.db import models
from django.utils import timezone

from core.contrib.db.fields import DecimalIntField
from core.general.model_types import CommonCourtesyTitles, ZoneStationType
from core.general.models import BaseAuditModel, BaseValidModel

from core.refunds.model_types import (
    CreditCardTypes,
    RefundPayTypes,
    PurchaseTypeChoices,
    RoutingStatusChoices,
    SentForProcessingChoices,
    CaseType,
    CaseTicketStatus,
    PaymentType,
    InvoiceStatus,
    CaseStatus,
    CaseStatusDetail,
)


def generate_sequence_number():
    """Generate 12-digit random sequence number."""
    return "".join(secrets.choice(string.digits) for _ in range(12))


class Refund(models.Model):
    """Main refund case model with customer and ticket information."""
    sequence_number = models.CharField(
        max_length=20, unique=True, help_text="Sequence#", blank=True
    )

    routing_status = models.CharField(max_length=15, null=True, choices=RoutingStatusChoices)
    open_date = models.DateTimeField(null=True, blank=True)

    from_dept = models.ForeignKey(
        "general.Department",
        on_delete=models.SET_NULL,
        related_name="refund_from_department",
        db_column="from_dept_id",
        null=True,
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="refunds_from",
    )

    route_to_dept = models.ForeignKey(
        "general.Department",
        on_delete=models.SET_NULL,
        related_name="refund_to_department",
        db_column="route_to_dept_id",
        null=True,
    )

    route_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="refunds_routed_to",
    )

    originally_entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="refunds_entered",
    )
    date_entered = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="refunds_updated",
    )
    update_date = models.DateTimeField(auto_now=True)

    # Customer Information
    title = models.CharField(max_length=20, blank=True, choices=CommonCourtesyTitles)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.ForeignKey(
        "general.Country",
        on_delete=models.SET_NULL,
        related_name="refund_country",
        db_column="country_id",
        null=True,
    )
    intl_zip = models.CharField(max_length=20, blank=True)
    day_phone = models.CharField(max_length=20, blank=True)
    evening_phone = models.CharField(max_length=20, blank=True)
    extension = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)

    current_status = models.ForeignKey(
        "general.Status",
        on_delete=models.SET_NULL,
        related_name="refund_status",
        db_column="current_status_id",
        null=True,
    )

    notified_by = models.ForeignKey(
        "refunds.NotifiedBy",
        on_delete=models.SET_NULL,
        related_name="refunds_notified_by",
        db_column="notified_by_id",
        null=True,
    )

    form_number = models.CharField(max_length=50, blank=True)

    status_changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="refunds_status_changed",
    )
    status_date = models.DateTimeField(null=True, blank=True)
    refund_reason = models.ForeignKey(
        "refunds.RefundReason",
        on_delete=models.SET_NULL,
        related_name="refund_reason",
        db_column="refund_reason_id",
        null=True,
    )
    cust_notified_by = models.ForeignKey(
        "refunds.CustomerNotifiedBy",
        on_delete=models.SET_NULL,
        related_name="refunds_customers_notified_by",
        db_column="cust_notified_by_id",
        null=True,
    )

    reason_text = models.TextField(blank=True)

    approval_justification = models.ForeignKey(
        "refunds.RefundJustification",
        on_delete=models.SET_NULL,
        related_name="refunds_approval_justification",
        db_column="approval_justification_id",
        null=True,
    )

    denial_justification = models.ForeignKey(
        "refunds.RefundJustification",
        on_delete=models.SET_NULL,
        related_name="refunds_denial_justification",
        db_column="denial_justification_id",
        null=True,
    )

    # Ticket Info Section
    purchased_date_time = models.DateTimeField(null=True)
    loose_ticket = models.BooleanField(default=False)
    cust_service_petty_cash = models.BooleanField(default=False)

    connecting_service = models.ForeignKey(
        "general.ConnectingService",
        on_delete=models.SET_NULL,
        related_name="refunds_connecting_service",
        db_column="connecting_service_id",
        null=True,
    )
    other_connecting_service = models.CharField(max_length=100, blank=True)

    # Payment & Purchase Details
    purchase_type = models.CharField(max_length=50, blank=True, choices=PurchaseTypeChoices)
    card_type = models.CharField(max_length=50, blank=True, choices=CreditCardTypes)
    card_number = models.CharField(max_length=50, blank=True)
    exp_year = models.CharField(max_length=5, blank=True)
    exp_month = models.CharField(max_length=3, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    merchant_order_id = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=100, blank=True)
    order_reference = models.CharField(max_length=100, blank=True)
    date_recorded_by_station = models.DateTimeField(null=True, blank=True)

    sent_for_processing = models.CharField(
        max_length=100, choices=SentForProcessingChoices, blank=True
    )
    remarks = models.TextField(blank=True)
    paid_date = models.DateField(null=True, blank=True)
    check_number = models.CharField(max_length=50, blank=True)
    amount_refunded = DecimalIntField(
        max_digits=10, decimal_places=2, default=0.00, blank=True
    )
    total_amount_of_refund = DecimalIntField(
        max_digits=10, decimal_places=2, default=0.00
    )
    fee = DecimalIntField(max_digits=10, decimal_places=2, default=10.00)
    final_refund = DecimalIntField(max_digits=10, decimal_places=2, default=0.00)

    company = models.ForeignKey(
        "general.Company",
        on_delete=models.SET_NULL,
        null=True,
        related_name="refund_company_id",
        db_column="company_id",
    )

    # SalesForce Integration
    sf_id = models.CharField(max_length=50, blank=True, db_column="sf_id")
    contact_sf_id = models.CharField(max_length=50, blank=True, db_column="contact_sf_id")

    # Case Management
    case_type = models.CharField(max_length=20, choices=CaseType, default=CaseType.REFUND, db_column="case_type")
    case_status = models.CharField(max_length=20, choices=CaseStatus, blank=True, db_column="case_status")
    case_status_detail = models.CharField(max_length=30, choices=CaseStatusDetail, blank=True, db_column="case_status_detail")
    payment_type = models.CharField(max_length=20, choices=PaymentType, blank=True, db_column="payment_type")
    settlement_total = DecimalIntField(max_digits=10, decimal_places=2, default=0.00, db_column="settlement_total")

    # CORE Transaction Link
    device_id = models.IntegerField(null=True, blank=True, db_column="deviceid")
    device_class_id = models.IntegerField(null=True, blank=True, db_column="deviceclassid")
    sales_transaction_no = models.IntegerField(null=True, blank=True, db_column="salestransactionno")
    unique_ms_id = models.IntegerField(null=True, blank=True, db_column="uniquemsid")

    def __str__(self):
        return (
            f"Refund {self.sequence_number} - " + f"{self.first_name} {self.last_name}"
        )

    def save(self, *args, **kwargs):
        user = None

        if not self.pk and user is not None:
            self.originally_entered_by = user
            self.date_entered = timezone.now()

        if user is not None:
            self.status_changed_by = user
            self.status_date = timezone.now()
            self.last_updated_by = user

        if not self.sequence_number:
            while True:
                new_seq = generate_sequence_number()
                if not Refund.objects.filter(sequence_number=new_seq).exists():
                    self.sequence_number = new_seq
                    break

        super().save(*args, **kwargs)


class RefundTicket(models.Model):
    """Individual ticket within a refund case."""
    refund = models.ForeignKey(
        Refund, on_delete=models.CASCADE, related_name="refund_tickets"
    )
    ticket = models.OneToOneField(
        "ticket.Ticket",
        on_delete=models.SET_NULL,
        null=True,
        related_name="refund_tickets",
    )
    ticket_number = models.CharField(max_length=50, blank=True)
    article_no = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    version = models.ForeignKey(
        "general.TariffVersions",
        models.CASCADE,
        db_column="versionid",
        null=True,
        blank=True,
    )
    packet_id = models.IntegerField(db_column="packetid", null=True, blank=True)

    sales_packet = models.ForeignObject(
        "tariff.SalesPackets",
        on_delete=models.SET_NULL,
        from_fields=("version_id", "packet_id"),
        to_fields=("version_id", "packet_id"),
        null=True,
        related_name="refund_tickets",
    )
    fare = DecimalIntField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    refund_amount = DecimalIntField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    from_station_id = models.IntegerField(blank=True, null=True)
    from_station_type = models.SmallIntegerField(
        null=True, blank=True, choices=ZoneStationType
    )
    from_station = models.ForeignObject(
        "general.ZoneStation",
        models.DO_NOTHING,
        from_fields=("version", "from_station_id", "from_station_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="refund_ticket_from_station",
        null=True,
    )

    to_station_id = models.IntegerField(blank=True, null=True)
    to_station = models.ForeignObject(
        "general.ZoneStation",
        models.DO_NOTHING,
        from_fields=("version", "from_station_id", "to_station_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="refund_ticket_to_station",
        null=True,
    )
    to_station_type = models.SmallIntegerField(
        null=True, blank=True, choices=ZoneStationType
    )
    amount = DecimalIntField(
        db_column="amount", default=0, decimal_places=2, blank=True
    )
    pay_type_1 = models.IntegerField(choices=RefundPayTypes)
    pay_type_2 = models.IntegerField(choices=RefundPayTypes, null=True, blank=True)

    # Ticket Research & Status
    status = models.CharField(max_length=20, choices=CaseTicketStatus, default=CaseTicketStatus.CREATED, db_column="ticket_status")
    is_active = models.BooleanField(default=True, db_column="is_active")

    # Amount Calculations
    balance_rated_amount = DecimalIntField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="balance_rated_amount")
    initial_amount = DecimalIntField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="initial_amount")
    ticket_fee = DecimalIntField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="ticket_fee")
    final_amount = DecimalIntField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="final_amount")

    # Original SalesDetail Reference
    sd_device_id = models.IntegerField(null=True, blank=True, db_column="sd_deviceid")
    sd_device_class_id = models.IntegerField(null=True, blank=True, db_column="sd_deviceclassid")
    sd_sales_detail_ev_sequ_no = models.IntegerField(null=True, blank=True, db_column="sd_salesdetailevsequno")
    sd_sales_transaction_no = models.IntegerField(null=True, blank=True, db_column="sd_salestransactionno")
    sd_unique_ms_id = models.IntegerField(null=True, blank=True, db_column="sd_uniquemsid")
    sd_correction_counter = models.IntegerField(null=True, blank=True, db_column="sd_correctioncounter")

    def __str__(self):
        return f"Ticket {self.ticket_number} for Refund {self.refund.sequence_number}"

    def save(self, *args, **kwargs):
        self.amount = (self.refund_amount or 0) * self.quantity
        return super().save(*args, **kwargs)


class RefundJustification(BaseAuditModel, BaseValidModel):
    """Approval or denial justification reasons."""
    description = models.CharField(max_length=255)
    denial_description = models.CharField(max_length=255)

    class Meta:
        db_table = "refund_justifications"

    def __str__(self):
        return self.description


class RefundReason(BaseAuditModel, BaseValidModel):
    """Reason for refund request."""
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "refund_reasons"

    def __str__(self):
        return self.description


class NotifiedBy(BaseAuditModel, BaseValidModel):
    """How the refund was initially notified."""
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "notified_by"

    def __str__(self):
        return self.description


class CustomerNotifiedBy(BaseAuditModel, BaseValidModel):
    """How the customer was notified of the decision."""
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "customer_notified_by"

    def __str__(self):
        return self.description


class CaseLog(models.Model):
    """Activity log for case comments and status changes."""

    refund = models.ForeignKey(Refund, on_delete=models.CASCADE, related_name="case_logs", db_column="case_id")
    sf_id = models.CharField(max_length=50, blank=True, db_column="sf_id")
    message = models.TextField()
    time_new = models.DateTimeField(auto_now_add=True, db_column="timenew")
    user_new = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="case_logs_created", db_column="usernew"
    )

    class Meta:
        db_table = "case_log"
        ordering = ["-time_new"]

    def __str__(self):
        return f"Log #{self.pk} for Case {self.refund.sequence_number}"


class CaseContact(models.Model):
    """Customer contact information from SalesForce."""

    sf_id = models.CharField(max_length=50, blank=True, db_column="sf_id")
    description = models.CharField(max_length=255, blank=True)
    is_deleted = models.BooleanField(default=False, db_column="is_deleted")
    primary_contact_id = models.IntegerField(null=True, blank=True, db_column="primary_contact_id")

    class Meta:
        db_table = "case_contact"

    def __str__(self):
        return self.description or f"Contact #{self.pk}"


class CaseContactElements(models.Model):
    """Many-to-many relationship between cases and contacts."""

    refund = models.ForeignKey(Refund, on_delete=models.CASCADE, related_name="contact_elements", db_column="case_id")
    contact = models.ForeignKey(CaseContact, on_delete=models.CASCADE, related_name="case_elements", db_column="contact_id")
    user_new = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, db_column="usernew")
    time_new = models.DateTimeField(auto_now_add=True, db_column="timenew")

    class Meta:
        db_table = "case_contact_elements"
        unique_together = ("refund", "contact")

    def __str__(self):
        return f"Case {self.refund_id} ↔ Contact {self.contact_id}"


class Invoice(models.Model):
    """Refund payment tracking and CTP balance management."""

    date = models.DateTimeField(auto_now_add=True)
    refund = models.ForeignKey(Refund, on_delete=models.CASCADE, related_name="invoices", db_column="case_id")
    status = models.CharField(max_length=10, choices=InvoiceStatus, default=InvoiceStatus.OPEN)
    net = DecimalIntField(max_digits=10, decimal_places=2, default=0)
    tax = DecimalIntField(max_digits=10, decimal_places=2, default=0)
    total = DecimalIntField(max_digits=10, decimal_places=2, default=0)
    paid_date = models.DateTimeField(null=True, blank=True)
    paid_amount = DecimalIntField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "invoice"
        ordering = ["-date"]

    def __str__(self):
        return f"Invoice #{self.pk} for Case {self.refund.sequence_number}"


class InvoiceDetail(models.Model):
    """Line items for invoices."""

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="details", db_column="invoice_id")

    class Meta:
        db_table = "invoice_detail"

    def __str__(self):
        return f"Detail #{self.pk} for Invoice {self.invoice_id}"
