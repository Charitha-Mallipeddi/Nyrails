from django.contrib import admin, messages
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from import_export.admin import ImportExportActionModelAdmin

from core.ticket.forms import TicketScanRandomDataForm

from .models import Ticket, TicketScan, TicketSource

admin.site.register(TicketSource)


@admin.register(Ticket)
class AdminTicket(ImportExportActionModelAdmin):
    list_display = ("number", "amount", "form")
    search_fields = ("number", "form")


@admin.register(TicketScan)
class AdminTicketScan(ImportExportActionModelAdmin):
    list_display = (
        "ticket",
        "tour_id",
        "conductor_id",
        "train_id",
        "scanned_on",
        "company",
        "source",
    )
    change_list_template = "admin/ticket/scan/change_list.html"
    random_data_template_name = "admin/ticket/scan/random_data.html"
    autocomplete_fields = ["ticket"]
    fields = (
        "ticket",
        "tour_id",
        "conductor_id",
        "train_id",
        "company",
        "source",
        "scanned_on",
        "time_new",
    )
    list_filter = ["company", "source"]

    def get_urls(self):
        urls = super().get_urls()
        info = self.get_model_info()
        my_urls = [
            path(
                "random_data/",
                self.admin_site.admin_view(self.random_data),
                name="{}_{}_random_data".format(*info),
            ),
        ]
        return my_urls + urls

    def random_data(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = TicketScanRandomDataForm(
            data=request.POST or None,
            files=request.FILES or None,
        )
        if form.is_valid():
            call_command(
                "ticket_random_scans",
                date=str(form.cleaned_data["date"]),
                days=form.cleaned_data["days"],
                count=form.cleaned_data["count"],
                ticket_form=form.cleaned_data["ticket_form"],
                dynamodb=form.cleaned_data["is_dynamodb"],
            )
            messages.success(
                request,
                f"{form.cleaned_data['count']} records "
                "of random ticket scan data has been generated",
            )
            url = reverse(
                "admin:{}_{}_changelist".format(*self.get_model_info()),
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(url)
        context["form"] = form
        context["opts"] = self.model._meta  # noqa: SLF001
        return TemplateResponse(request, [self.random_data_template_name], context)
