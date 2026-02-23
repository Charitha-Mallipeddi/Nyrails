import logging

from django import forms
from django.utils import timezone

from core.ticket.model_types import TicketFormType

logger = logging.getLogger(__name__)


class TicketScanRandomDataForm(forms.Form):
    date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"}),
        initial=timezone.now().date(),
        help_text="This is the last date of the data ",
    )
    days = forms.IntegerField(
        min_value=0,
        max_value=60,
        initial=15,
        help_text="This is the number of days to generate data",
    )
    count = forms.IntegerField(
        min_value=1,
        max_value=10000,
        initial=1000,
        help_text="This is the number of records to generate",
    )
    ticket_form = forms.ChoiceField(
        choices=[
            ("", "Any"),
            (TicketFormType.PAPER, "Paper Ticket"),
            (TicketFormType.ETIX, "eTix"),
        ],
        initial="",
        required=False,
        help_text="This is the type of ticket to generate",
    )
    is_dynamodb = forms.BooleanField(
        label="DynamoDB Only",
        required=False,
        help_text="This is the flag to indicate if the data should "
        "be generated in DynamoDB (only)",
    )

