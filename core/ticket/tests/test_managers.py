import json
from pathlib import Path

import pytest
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from core.ticket.models import PaperTicket, TicketScan
from core.users.models import User


class TestPaperTicketManger(TestCase):
    def test_decode_number(self):
        number = "0700011991906250022"
        rtn = PaperTicket.objects.decode_number(number)

        assert rtn["place_holder"] == "0"
        assert rtn["device"]["station"] == "7000"
        assert rtn["device"]["agency"] == 1
        assert rtn["device"]["class"] == 1
        assert rtn["device"]["no"] == "99"


@pytest.mark.django_db
class TestTicketScanManager(TestCase):
    fixtures = [
        "core/users/fixtures.json",
        "core/general/fixtures.json.gz",
        "core/ticket/fixtures.json.gz",
    ]

    def test_parse_pptix(self):
        created_by = User.objects.filter(id=1).first()
        if created_by is None:
            created_by = User.objects.create(username="test")
        dynamodb_data_path = Path("core/ticket/tests/dynamodb_data.json")

        dynamodb_data = json.loads(dynamodb_data_path.read_text(encoding="utf-8"))
        for data in dynamodb_data["paperticket"]:
            item = data[0]
            item_ticket = data[1]
            (ticket, _) = TicketScan.objects.parse_pptix_detail(
                item=item,
                item_ticket=item_ticket,
                created_by=created_by,
            )
            TicketScan.objects.parse_pptix_scan(item=item, ticket=ticket)
        for data in dynamodb_data["etix"]:
            item = data[0]
            item_ticket = data[1]
            (ticket, _) = TicketScan.objects.parse_etix_detail(
                item=item,
                item_ticket=item_ticket,
                created_by=created_by,
            )
            TicketScan.objects.parse_etix_scan(item=item, ticket=ticket)

    @pytest.mark.django_db
    def test_ticket_random_scans_command(self):
        now = timezone.now().date()
        command_result = call_command(
            "ticket_random_scans",
            count=1,
            days=0,
            date=now.isoformat(),
            ticket_form="etix",
        )
        assert command_result is None
