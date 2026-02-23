from django import forms

from core.contrib.forms.fields import CompositeKeyModelChoiceField
from core.general.models import ZoneStation
from core.tariff.models import SalesPackets

from .models import Ctp


class CtpForm(forms.ModelForm):
    ticket_type = CompositeKeyModelChoiceField(
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
        model = Ctp
        fields = (
            "open_date",
            "routing_status",
            "from_dept",
            "route_to_dept",
            "dob",
            "invoice_date",
            "letter_sent_date",
            "letter_generated_date",
            "balance",
            "date_of_payment",
        )
        widgets = {
            "open_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "routing_status": forms.RadioSelect(),
            "from_dept": forms.Select(),
            "route_to_dept": forms.Select(),
            "dob": forms.DateInput(attrs={"type": "date"}),
            "invoice_date": forms.DateInput(attrs={"type": "date"}),
            "letter_sent_date": forms.DateInput(attrs={"type": "date"}),
            "letter_generated_date": forms.DateInput(attrs={"type": "date"}),
            "balance": forms.TextInput(attrs={"readonly": "true"}),
            "date_of_payment": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-populate composite key fields if instance exists
        if self.instance and self.instance.pk:
            # Load ticket_type
            if self.instance.version_id and self.instance.packet_id:
                try:
                    ticket_type_obj = SalesPackets.objects.get(
                        version_id=self.instance.version_id,
                        packet_id=self.instance.packet_id,
                    )
                    self.fields["ticket_type"].initial = ticket_type_obj
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
        self.fields["ticket_type"].widget.choices = self.fields["ticket_type"].choices
        self.fields["from_station"].widget.choices = self.fields["from_station"].choices
        self.fields["to_station"].widget.choices = self.fields["to_station"].choices

    def save(self, commit=True):  # noqa: FBT002
        instance = super().save(commit=False)

        # Set composite key fields from ticket_type
        ticket_type = self.cleaned_data.get("ticket_type")
        if ticket_type:
            instance.version = ticket_type.version
            instance.packet_id = ticket_type.packet_id

        # Set composite key fields from from_station
        from_station = self.cleaned_data.get("from_station")
        if from_station:
            instance.from_station_id = from_station.zone_station_id
            instance.from_station_type = from_station.type
            # Only set version if not already set by ticket_type
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
