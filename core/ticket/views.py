import logging
from datetime import datetime, time, timedelta
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.generic import DetailView, TemplateView

from core.ticket.models import Ticket, TicketScan

logger = logging.getLogger(__name__)


# Create your views here.
class TicketScanDashboardView(
    LoginRequiredMixin, PermissionRequiredMixin, TemplateView
):
    template_name = "ticket/scan/dashboard.html"
    permission_required = "ticket.view_ticketscan"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["end_date_time"] = timezone.now()
        context["start_date_time"] = context["end_date_time"] - timedelta(hours=24)
        context["end_date"] = context["end_date_time"].date()
        context["start_date"] = context["end_date"] - timedelta(days=7)
        start_date = self.request.GET.get("start_date", None)
        end_date = self.request.GET.get("end_date", None)
        if start_date:
            context["start_date"] = parse_date(start_date)
        if end_date:
            context["end_date"] = parse_date(end_date)

        try:
            start_date_time = datetime.combine(
                context["start_date"],
                time.min,
                timezone.get_current_timezone(),
            )
            end_date_time = datetime.combine(
                context["end_date"],
                time.max,
                timezone.get_current_timezone(),
            )
            TicketScan.objects.sync_with_dynamodb_pptix(start_date_time, end_date_time)
            TicketScan.objects.sync_with_dynamodb_etix(start_date_time, end_date_time)
        except Exception:
            logger.exception("Error while syncing with dynamodb")

        return context


ticket_scan_dashboard_view = TicketScanDashboardView.as_view()


class TicketScanDetailView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "ticket/scan/detail.html"
    permission_required = "ticket.view_ticketscan"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["end_date"] = timezone.now().date()
        context["start_date"] = context["end_date"] - timedelta(days=7)
        conductor_id = self.request.GET.get("conductor_id", None)
        train_id = self.request.GET.get("train_id", None)
        tour_id = self.request.GET.get("tour_id", None)
        start_date = self.request.GET.get("start_date", None)
        end_date = self.request.GET.get("end_date", None)
        if start_date:
            context["start_date"] = parse_date(start_date)

        if end_date:
            context["end_date"] = parse_date(end_date)
        context["conductor_id"] = conductor_id
        context["train_id"] = train_id
        context["tour_id"] = tour_id
        return context


ticket_scan_detail_view = TicketScanDetailView.as_view()


class TicketDetailModalView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = "ticket/modal.html"
    model = Ticket
    permission_required = "ticket.view_ticketscan"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["top_logo"] = "images/eticket.svg"
        if self.object.form == "paperticket":
            context["top_logo"] = "images/paperticket.svg"
        return context


ticket_detail_modal_view = TicketDetailModalView.as_view()
