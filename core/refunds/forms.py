from django import forms

from core.contrib.forms.fields import CompositeKeyModelChoiceField
from core.general.models import ZoneStation
from core.tariff.models import SalesPackets
from django_tomselect.widgets import TomSelectModelWidget
from django_tomselect.forms import TomSelectModelMultipleChoiceField,TomSelectIterablesWidget
from hugerte.widgets import HugeRTE
from core.refunds.models import Refund, RefundTicket
from django_tomselect.app_settings import TomSelectConfig,PluginRemoveButton

class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund

        routing_fields = (
            "company",
            "open_date",
            "routing_status",
            "from_dept",
            "from_user",
            "route_to_dept",
            "route_to_user",
        )
        customer_fields = (
            "first_name",
            "last_name",
            "email",
            "day_phone",
            "address_1",
            "zip_code",
            "city",
            "state",
            "country",
            "extension",
        )
        reason_status_fields = (
            "current_status",
            "notified_by",
            "cust_notified_by",
            "form_number",
            "status_changed_by",
            "status_date",
            "refund_reason",
            "reason_text",
            "approval_justification",
            "denial_justification",
        )
        ticket_info_fields = (
            "purchased_date_time",
            "loose_ticket",
        )
        auth_info_fields = (
            "date_recorded_by_station",
            "sent_for_processing",
            "remarks",
            "paid_date",
            "check_number",
            "total_amount_of_refund",
            "fee",
            "final_refund",
        )

        purchase_fields = (
            "exp_year",
            "exp_month",
            "purchase_type",
            "card_type",
            "card_number",
            "transaction_reference",
            "payment_reference",
            "order_reference",
            "merchant_order_id",
            "token",
        )
        fields = (
            routing_fields
            + customer_fields
            + reason_status_fields
            + ticket_info_fields
            + auth_info_fields
            + purchase_fields
        )
        widgets = {
            "open_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "status_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "purchased_date_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "date_recorded_by_station": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "paid_date": forms.DateInput(attrs={"type": "date"}),
            "refund_reason": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="refunds:refund-reason-autocomplete",
                    value_field="id",
                    label_field="description",
                    placeholder="Select a refund reason",
                    preload="focus",
                    highlight=True,
                )
            ),
            "reason_text": HugeRTE(
                rte_attrs={"height": 200},
                attrs={
                    "rows": 3,
                    "placeholder": "Provide a detailed explaation...",
                    "auto_size": True,
                },
            ),
            "remarks": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Internal notes..."}
            ),
            "routing_status": TomSelectIterablesWidget(
                config=TomSelectConfig(
                    url="refunds:routing-status-autocomplete",
                    placeholder="Select routing status",
                    value_field="value",
                    label_field="label",
                    preload="focus",
                    highlight=True,
                )
            ),
            "exp_year": forms.NumberInput(),
            "exp_month": forms.NumberInput(),
            "purchase_type": TomSelectIterablesWidget(
                config=TomSelectConfig(
                    url="refunds:purchase-type-autocomplete",
                    placeholder="Select purchase type",
                    value_field="value",
                    label_field="label",
                    preload="focus",
                    highlight=True,
                    attrs={"id": "purchase_type"},
                ),
            ),
            "total_amount_of_refund": forms.NumberInput(
                attrs={"readonly": "true", "type": "number"}
            ),
            "fee": forms.NumberInput(attrs={"type": "number"}),
            "company": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="general:company-autocomplete",
                    value_field="company_id",
                    label_field="name",
                    placeholder="Select a company",
                    preload="focus",
                    highlight=True,
                )
            ),
            "from_dept": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="general:department-autocomplete",
                    value_field="id",
                    label_field="description",
                    placeholder="Select a department",
                    preload="focus",
                    highlight=True,
                )
            ),
            "route_to_dept": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="general:department-autocomplete",
                    value_field="id",
                    label_field="description",
                    placeholder="Select a department",
                    preload="focus",
                    highlight=True,
                )
            ),
            "country": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="general:country-autocomplete",
                    value_field="id",
                    label_field="description",
                    placeholder="Select a country",
                    preload="focus",
                    highlight=True,
                )
            ),
            "from_user": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="users:autocomplete",
                    value_field="id",
                    label_field="username",
                    placeholder="Select a user",
                    preload="focus",
                    highlight=True,
                )
            ),
            "route_to_user": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="users:autocomplete",
                    value_field="id",
                    label_field="username",
                    placeholder="Select a user",
                    preload="focus",
                    highlight=True,
                )
            ),
            "approval_justification": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="refunds:justification-autocomplete",
                    value_field="id",
                    label_field="description",
                    placeholder="Select an approval justification",
                    preload="focus",
                    highlight=True,
                )
            ),
            "denial_justification": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="refunds:justification-autocomplete",
                    value_field="id",
                    label_field="denial_description",
                    placeholder="Select a denial justification",
                    preload="focus",
                    highlight=True,
                )
            ),
            "current_status": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="general:status-autocomplete",
                    value_field="id",
                    label_field="description",
                    placeholder="Select a status",
                    preload="focus",
                    highlight=True,
                )
            ),
            "notified_by": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="refunds:notified-by-autocomplete",
                    value_field="id",
                    label_field="description",
                    placeholder="Select notification method",
                    preload="focus",
                    highlight=True,
                )
            ),
            "cust_notified_by": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="refunds:customer-notified-by-autocomplete",
                    value_field="id",
                    label_field="description",
                    placeholder="Select customer notification method",
                    preload="focus",
                    highlight=True,
                )
            ),
            "status_changed_by": TomSelectModelWidget(
                config=TomSelectConfig(
                    url="users:autocomplete",
                    value_field="id",
                    label_field="username",
                    placeholder="Select a user",
                    preload="focus",
                    highlight=True,
                )
            ),
            "sent_for_processing": TomSelectIterablesWidget(
                config=TomSelectConfig(
                    url="refunds:sent-for-processing-autocomplete",
                    placeholder="Select sent for processing",
                    value_field="value",
                    label_field="label",
                    preload="focus",
                    highlight=True,
                )
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "refund_amount":
                field.widget.attrs["class"] = "refund_amount"

        self.fields["approval_justification"].label_from_instance = (
            lambda obj: obj.description
        )
        self.fields["denial_justification"].label_from_instance = (
            lambda obj: obj.denial_description
        )
        self.fields["company"].label_from_instance = lambda obj: obj.name


class TransactionLookUpForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(), required=True)
    to_date = forms.DateField(widget=forms.DateInput(), required=True)
    transaction_num = forms.IntegerField(widget=forms.NumberInput(), required=True)

    serial_num = forms.IntegerField(widget=forms.NumberInput())
    selling_station = forms.CharField(widget=forms.TextInput())
    selling_device = forms.CharField(widget=forms.TextInput())


class DenialEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"disabled": "true"}))
    subject = forms.CharField(widget=forms.TextInput())
    body = forms.CharField(widget=HugeRTE(
                rte_attrs={"height": 200},
                attrs={
                    "rows": 3,
                    "placeholder": "Enter email body...",
                    "auto_size": True,
                },
            ),)
    next = forms.CharField(widget=forms.TextInput())

class RefundTicketForm(forms.ModelForm):
    sales_packet = CompositeKeyModelChoiceField(
        queryset=SalesPackets.objects.all(),
        required=False,
        widget=forms.Select(),
        label="Ticket Type",
        label_from_instance=lambda obj: obj.description,
    )

    from_station = CompositeKeyModelChoiceField(
        queryset=ZoneStation.objects.all(),
        required=False,
        widget=forms.Select(),
        label="From Station",
        label_from_instance=lambda obj: obj.description,
    )

    to_station = CompositeKeyModelChoiceField(
        queryset=ZoneStation.objects.all(),
        required=False,
        widget=forms.Select(),
        label="To Station",
        label_from_instance=lambda obj: obj.description,
    )

    class Meta:
        model = RefundTicket
        fields = [
            "sales_packet",
            "article_no",
            "quantity",
            "fare",
            "refund_amount",
            "pay_type_1",
            "amount",
        ]
        widgets = {
            "sales_packet": forms.TextInput(),
            "article_no": forms.TextInput(),
            "quantity": forms.NumberInput(),
            "fare": forms.NumberInput(attrs={"placeholder": "0.00", "step": "0.01"}),
            "refund_amount": forms.NumberInput(attrs={"placeholder": "0.00", "step": "0.01", "class": "refund-amount"}),
            # "pay_type_1": TomSelectIterablesWidget(
            #     config=TomSelectConfig(
            #         url="refunds:refund-pay-type-autocomplete",
            #         placeholder="Select refund pay type",
            #         value_field="value",
            #         label_field="label",
            #         preload="focus",
            #         highlight=True,
            #     )
            # ), TODO : check why this is not working
            "pay_type_1": forms.Select(),
            "amount": forms.NumberInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-populate composite key fields if instance exists
        if self.instance and self.instance.pk:
            # Load sales_packet
            if self.instance.version_id and self.instance.packet_id:
                try:
                    sales_packet_obj = SalesPackets.objects.get(
                        version_id=self.instance.version_id,
                        packet_id=self.instance.packet_id,
                    )
                    self.fields["sales_packet"].initial = sales_packet_obj
                except SalesPackets.DoesNotExist:
                    pass

            # Load from_station
            if (
                self.instance.version_id
                and self.instance.from_station_id
                and self.instance.from_station_type
            ):
                try:
                    from_station_obj = ZoneStation.objects.get(
                        version_id=self.instance.version_id,
                        zone_station_id=self.instance.from_station_id,
                        type=self.instance.from_station_type,
                    )
                    self.fields["from_station"].initial = from_station_obj
                except ZoneStation.DoesNotExist:
                    pass

            # Load to_station
            if (
                self.instance.version_id
                and self.instance.to_station_id
                and self.instance.to_station_type
            ):
                try:
                    to_station_obj = ZoneStation.objects.get(
                        version_id=self.instance.version_id,
                        zone_station_id=self.instance.to_station_id,
                        type=self.instance.to_station_type,
                    )
                    self.fields["to_station"].initial = to_station_obj
                except ZoneStation.DoesNotExist:
                    pass

        # Update widget choices for composite key fields
        self.fields["sales_packet"].widget.choices = self.fields["sales_packet"].choices
        self.fields["from_station"].widget.choices = self.fields["from_station"].choices
        self.fields["to_station"].widget.choices = self.fields["to_station"].choices

        # Apply styling to all fields
        for name, field in self.fields.items():
            if name == "refund_amount":
                field.widget.attrs["class"] = "refund_amount"

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)

        # Set composite key fields from sales_packet
        sales_packet = self.cleaned_data.get("sales_packet")
        if sales_packet:
            instance.version = sales_packet.version
            instance.packet_id = sales_packet.packet_id

        # Set composite key fields from from_station
        from_station = self.cleaned_data.get("from_station")
        if from_station:
            instance.from_station_id = from_station.zone_station_id
            instance.from_station_type = from_station.type
            # Only set version if not already set by sales_packet
            if not instance.version_id:
                instance.version = from_station.version

        # Set composite key fields from to_station
        to_station = self.cleaned_data.get("to_station")
        if to_station:
            instance.to_station_id = to_station.zone_station_id
            instance.to_station_type = to_station.type
            # Only set version if not already set
            if not instance.version_id:
                instance.version = to_station.version

        if commit:
            instance.save()

        return instance


class RefundFilterForm(forms.Form):
    sequence_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by sequence number"}),
    )
    
    company = TomSelectModelMultipleChoiceField(
        required=False,
        config=TomSelectConfig(
            url="general:company-autocomplete",
            value_field="company_id",
            label_field="name",
            placeholder="Select companies",
            preload="focus",
            highlight=True,
            plugin_remove_button=PluginRemoveButton(),
        ),
    )
    
    date_entered_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date Entered From",
    )
    date_entered_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date Entered To",
    )
        
    department = TomSelectModelMultipleChoiceField(
        required=False,
        config=TomSelectConfig(
            url="general:department-autocomplete",
            value_field="id",
            label_field="description",
            placeholder="Select departments",
            preload="focus",
            highlight=True,
            plugin_remove_button=PluginRemoveButton(),
        ),
    )

    from_user = TomSelectModelMultipleChoiceField(
        required=False,
        config=TomSelectConfig(
            url="users:autocomplete",
            value_field="id",
            label_field="username",
            placeholder="Select from user",
            preload="focus",
            highlight=True,
            plugin_remove_button=PluginRemoveButton()
        ),
    )

    to_user = TomSelectModelMultipleChoiceField(
        required=False,
        config=TomSelectConfig(
            url="users:autocomplete",
            value_field="id",
            label_field="username",
            placeholder="Select to user",
            preload="focus",
            highlight=True,
            plugin_remove_button=PluginRemoveButton()
        ),
    )
    
    amount_from = forms.DecimalField(
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"placeholder": "Amount from", "step": "0.01"}),
    )
    amount_to = forms.DecimalField(
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"placeholder": "Amount to", "step": "0.01"}),
    )
