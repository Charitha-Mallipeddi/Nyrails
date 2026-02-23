from http import HTTPStatus

import pytest
from django.test import Client, TestCase
from django.urls import reverse

from core.ticket.admin import AdminTicketTypeModelResource
from core.users.models import User


@pytest.mark.django_db
class TestTicketAdmin(TestCase):
    fixtures = [
        "core/users/fixtures.json",
        "core/general/fixtures.json.gz",
        "core/ticket/fixtures.json.gz",
    ]

    def setUp(self):
        self.admin_user = User.objects.get(pk=1)
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_scan_random_data(self):
        url = reverse("admin:ticket_ticketscan_random_data")
        response = self.client.get(url)
        assert response.status_code == HTTPStatus.OK

        response = self.client.post(
            url,
            data={
                "date": "2021-01-01",
                "days": 1,
                "count": 1,
                "ticket_form": "paperticket",
                "is_dynamodb": False,
            },
        )
        assert response.status_code == HTTPStatus.FOUND

    def test_type_after_init_instance(self):
        resource = AdminTicketTypeModelResource()
        ticket_type = resource._meta.model.objects.get(code="999995")  # pyright: ignore[reportAttributeAccessIssue] # noqa: SLF001
        ticket_type.created_on = None
        resource.after_init_instance(
            instance=ticket_type,
            new=False,
            row={
                "service_provider": 1,
                "code": "999995",
                "description": "Test Ticket Type",
            },
            user=self.admin_user,
        )
