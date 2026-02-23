import re

from django.test import TestCase
from django.utils import timezone

from core.ticket.model_types import TicketFormType
from core.ticket.models import (
    ETixTicket,
    PaperTicket,
    Ticket,
    TicketScan,
    TicketSource,
)


class TestTicketModels(TestCase):
    fixtures = [
        "core/users/fixtures.json",
        "core/general/fixtures.json.gz",
        "core/ticket/fixtures.json.gz",
    ]

    def test_source(self):
        source = TicketSource.objects.get(pk=1)
        assert source.name == str(source)

    def test_ticket(self):
        ticket = Ticket()
        ticket.number = "1234567890"
        ticket.form = TicketFormType.PAPER
        assert str(ticket) == f"{ticket.number}[{ticket.get_form_display()}]"

    def test_paper_ticket(self):
        tour = PaperTicket()
        tour.number = 9999
        assert str(tour) == str(tour.number)

    def test_e_ticket(self):
        tour = ETixTicket()
        tour.e_ticket_no = 9999
        assert str(tour) == str(tour.e_ticket_no)

    def test_scan(self):
        scan = TicketScan()
        scan.ticket = Ticket()
        scan.ticket.number = 9999
        scan.tour_id = 0
        scan.scanned_on = timezone.now()
        assert re.search(r"\d+-\d+-\d+", str(scan))
