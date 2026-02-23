from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, View
from core.general.models import Company
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from decimal import Decimal
from core.refunds.forms import RefundForm, RefundTicketForm, TransactionLookUpForm, DenialEmailForm, RefundFilterForm
from core.refunds.models import Refund, RefundJustification, RefundReason, NotifiedBy, CustomerNotifiedBy,RefundTicket
from weasyprint import HTML
from io import BytesIO
from django_tomselect.autocompletes import AutocompleteModelView,AutocompleteIterablesView
from core.refunds.model_types import RoutingStatusChoices,PurchaseTypeChoices, SentForProcessingChoices,RefundPayTypes

class RefundListView(LoginRequiredMixin, TemplateView):
    template_name = "list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        refunds = Refund.objects.all().order_by("-date_entered")

        # Initialize filter form with GET data
        filter_form = RefundFilterForm(self.request.GET or None)
        
        if filter_form.is_valid():
            # Filter by sequence number
            if filter_form.cleaned_data.get("sequence_number"):
                refunds = refunds.filter(sequence_number=filter_form.cleaned_data["sequence_number"])

            # Filter by company (multiple values)
            if filter_form.cleaned_data.get("company"):
                refunds = refunds.filter(company__in=filter_form.cleaned_data["company"])

            # Filter by date range
            if filter_form.cleaned_data.get("date_entered_from"):
                refunds = refunds.filter(date_entered__date__gte=filter_form.cleaned_data["date_entered_from"])

            if filter_form.cleaned_data.get("date_entered_to"):
                refunds = refunds.filter(date_entered__date__lte=filter_form.cleaned_data["date_entered_to"])

            # Filter by department (multiple values)
            if filter_form.cleaned_data.get("department"):
                refunds = refunds.filter(from_dept__in=filter_form.cleaned_data["department"])

            # Filter by from_user (multiple values)
            if filter_form.cleaned_data.get("from_user"):
                refunds = refunds.filter(from_user__in=filter_form.cleaned_data["from_user"])

            # Filter by to_user (multiple values)
            if filter_form.cleaned_data.get("to_user"):
                refunds = refunds.filter(route_to_user__in=filter_form.cleaned_data["to_user"])

            # Filter by amount range
            if filter_form.cleaned_data.get("amount_from"):
                refunds = refunds.filter(total_amount_of_refund__gte=filter_form.cleaned_data["amount_from"])

            if filter_form.cleaned_data.get("amount_to"):
                refunds = refunds.filter(total_amount_of_refund__lte=filter_form.cleaned_data["amount_to"])

        paginator = Paginator(refunds, self.paginate_by)
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            "page_obj": page_obj,
            "filter_form": filter_form,
        })
        return context


refund_list = RefundListView.as_view()


class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = "analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected = self.request.GET.get("railroad-filter", "all")
        companies = Company.objects.all()
        final_companies = [{"company_id": "all", "short_name": "ALL"}, *list(companies)]

        # Base queryset - filter by railroad if selected
        base_qs = Refund.objects.all()
        if selected != "all":
            try:
                selected = int(selected)
                base_qs = base_qs.filter(company_id=selected)
            except (ValueError, TypeError):
                selected = "all"

        # Total refunds and amount
        totals = base_qs.aggregate(
            total_refunds=Count("id"),
            total_amount=Coalesce(Sum("total_amount_of_refund"), Decimal("0.00")),
        )
        total_refunds = totals["total_refunds"] or 0
        total_amount = totals["total_amount"] or Decimal("0.00")

        # Status counts - using current_status relationship
        status_counts_qs = (
            base_qs.values("current_status__description")
            .annotate(count=Count("id"))
            .order_by("current_status__description")
        )
        status_counts = {}
        for item in status_counts_qs:
            status_name = item["current_status__description"] or "Unknown"
            status_counts[status_name.lower()] = item["count"]

        # Department counts - using from_dept relationship
        dept_counts_qs = (
            base_qs.values("from_dept__description")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        dept_counts = {}
        for item in dept_counts_qs:
            dept_name = item["from_dept__description"] or "Unknown"
            dept_counts[dept_name] = item["count"]

        # Railroad counts - using company relationship
        railroad_counts_qs = (
            Refund.objects.values("company__short_name")
            .annotate(count=Count("id"), amount=Coalesce(Sum("total_amount_of_refund"), Decimal("0.00")))
            .order_by("company__short_name")
        )
        railroad_counts = {}
        railroad_stats = {}
        for item in railroad_counts_qs:
            railroad_name = item["company__short_name"] or "Unknown"
            railroad_counts[railroad_name.lower()] = item["count"]
            railroad_stats[railroad_name.lower()] = {
                "count": item["count"],
                "amount": float(item["amount"]),
            }

        # Get specific railroad stats for MNR and LIRR
        mnr_stats = railroad_stats.get("mnr", {"count": 0, "amount": 0.0})
        lirr_stats = railroad_stats.get("lirr", {"count": 0, "amount": 0.0})

        context.update({
            "companies": final_companies,
            "selected": selected,
            "total_refunds": total_refunds,
            "total_amount": total_amount,
            "status_counts": status_counts,
            "dept_counts": dept_counts,
            "railroad_counts": railroad_counts,
            "mnr_stats": mnr_stats,
            "lirr_stats": lirr_stats,
        })
        return context


analytics = AnalyticsView.as_view()


class RefundCreateView(LoginRequiredMixin, CreateView):
    model = Refund
    form_class = RefundForm
    template_name = "add.html"
    success_url = reverse_lazy("refunds:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            ticket_form_set = inlineformset_factory(
                Refund, RefundTicket, form=RefundTicketForm, extra=0, can_delete=True
            )
            context["ticket_formset"] = ticket_form_set(self.request.POST)
        else:
            ticket_form_set = inlineformset_factory(
                Refund, RefundTicket, form=RefundTicketForm, extra=0, can_delete=True
            )
            context["ticket_formset"] = ticket_form_set()

        context["transaction_lookup_form"] = TransactionLookUpForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ticket_formset = context["ticket_formset"]

        if ticket_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                ticket_formset.instance = self.object
                ticket_formset.save()
            messages.success(self.request, "Refund created successfully")
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


refund_create = RefundCreateView.as_view()


class RefundEditView(LoginRequiredMixin, UpdateView):
    model = Refund
    form_class = RefundForm
    template_name = "edit.html"
    success_url = reverse_lazy("refunds:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_form_set = inlineformset_factory(
            Refund, RefundTicket, form=RefundTicketForm, extra=0, can_delete=True
        )

        if self.request.POST:
            context["ticket_formset"] = ticket_form_set(self.request.POST, instance=self.object)
        else:
            context["ticket_formset"] = ticket_form_set(instance=self.object)

        context["transaction_lookup_form"] = TransactionLookUpForm()
        context["denial_email_form"] = DenialEmailForm(
            initial={
                "email": self.object.email,
                "body": create_denial_body(self.object),
            }
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ticket_formset = context["ticket_formset"]

        if ticket_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                ticket_formset.instance = self.object
                ticket_formset.save()
            messages.success(self.request, "Refund updated successfully")
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


refund_edit = RefundEditView.as_view()

class DenialMailView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        denial_email_form = DenialEmailForm(request.POST)
        # TODO : send email
        return redirect(denial_email_form.data.get("next"))


denial_mail = DenialMailView.as_view()


class DenialLetterPDFView(LoginRequiredMixin, View):
    """Generate and return a PDF of the denial letter for a specific refund."""

    def get(self, request, pk, *args, **kwargs):
        refund = get_object_or_404(Refund, pk=pk)

        # Render the PDF template with refund context
        html_string = render_to_string("letter-panel-pdf.html", {"refund": refund})

        # Generate PDF
        pdf_file = BytesIO()
        HTML(string=html_string).write_pdf(pdf_file)
        pdf_file.seek(0)

        # Create response
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="denial_letter_{refund.sequence_number}.pdf"'

        return response


generate_denial_letter_pdf = DenialLetterPDFView.as_view()

class DenialJustificationAutoCompleteView(AutocompleteModelView):
    model = RefundJustification
    search_lookups = ['denial_description__icontains',"description__icontains"]
    value_fields = ['id', 'denial_description', "description"]

denial_justification_autocomplete_view = DenialJustificationAutoCompleteView.as_view()


class RefundReasonAutoCompleteView(AutocompleteModelView):
    model = RefundReason
    search_lookups = ['description__icontains']
    value_fields = ['id', 'description']

refund_reason_autocomplete_view = RefundReasonAutoCompleteView.as_view()


class NotifiedByAutoCompleteView(AutocompleteModelView):
    model = NotifiedBy
    search_lookups = ['description__icontains']
    value_fields = ['id', 'description']

notified_by_autocomplete_view = NotifiedByAutoCompleteView.as_view()


class CustomerNotifiedByAutoCompleteView(AutocompleteModelView):
    model = CustomerNotifiedBy
    search_lookups = ['description__icontains']
    value_fields = ['id', 'description']

customer_notified_by_autocomplete_view = CustomerNotifiedByAutoCompleteView.as_view()

class RoutingStatusAutoCompleteView(AutocompleteIterablesView):
    iterable = RoutingStatusChoices
    page_size = 10

routing_status_autocomplete_view = RoutingStatusAutoCompleteView.as_view()

class PurchaseTypeAutoCompleteView(AutocompleteIterablesView):
    iterable = PurchaseTypeChoices
    page_size = 10

purchase_type_autocomplete_view = PurchaseTypeAutoCompleteView.as_view()

class SentForProcessingAutoCompleteView(AutocompleteIterablesView):
    iterable = SentForProcessingChoices
    page_size = 10

sent_for_processing_autocomplete_view = SentForProcessingAutoCompleteView.as_view()

class RefundPayTypeAutoCompleteView(AutocompleteIterablesView):
    iterable = RefundPayTypes
    page_size = 10

refund_pay_type_autocomplete_view = RefundPayTypeAutoCompleteView.as_view()

def create_denial_body(refund:Refund):
    return f"""{refund.date_entered} Reference # {refund.sequence_number}

{refund.first_name} {refund.last_name}
{refund.address_1}
{refund.city}, {refund.state} {refund.zip_code}
Email: {refund.email}
Dear {refund.first_name} {refund.last_name},
Upon receipt and review of your application, it was determined that your
application for a refund has been Denied for the following reason(s):
{refund.denial_justification}
The {refund.company.short_name} is a state agency that must comply with regulated tariffs that govern the
pricing of tickets and the issuance of refunds. The decision was rendered based
on these regulations in order for the {refund.company.short_name} to remain in compliance. Additional
information regarding the {refund.company.short_name}'s fare structure and refund policy may be obtained
via our website ( https://mta.info/fares-tolls/lirr-metro-north)
Although we are unable to fulfill your request, we appreciate your patronage.
This email notification is generated automatically and cannot accept responses. If
you need additional assistance, please contact us via the MTA's online reporting
system (https://contact.mta.info/s/customer-feedback) or call (718)217-5477.
Please include the reference number you received in this letter in your
correspondence or have it available to provide to an agent if contacting us by
phone.
Respectfully,
{refund.company.short_name} Refund Department

MTA {refund.company.name} is an agency of the Metropolitan Transportation
Authority, State of New York, Janno Lieber,Chairman & CEO
"""

