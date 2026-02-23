from calendar import monthrange
from decimal import Decimal
from typing import Any

import pytest
from dateutil import relativedelta
from django.utils import timezone
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient, APIRequestFactory

from core.general.models import Agency, Station, Version
from core.ticket.models import Ticket, TicketScan, TicketType
from core.users.models import User


@pytest.mark.django_db
class TestTicketViewSet:
    def setup_method(self):
        self.agencies = ["1", "2"]
        self.now = timezone.now()
        self.this_first_dom = self.now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        _, this_num_days = monthrange(
            self.this_first_dom.year,
            self.this_first_dom.month,
        )
        self.this_last_dom = self.this_first_dom.replace(
            day=this_num_days,
            hour=23,
            minute=59,
            second=59,
            microsecond=999,
        )

        self.last_now = self.now - relativedelta.relativedelta(months=1)
        self.last_first_dom = self.last_now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        ).date()
        _, last_num_days = monthrange(
            self.last_first_dom.year,
            self.last_first_dom.month,
        )
        self.last_last_dom = self.last_first_dom.replace(day=last_num_days)

        user = User.objects.create(username="test")

        agency = Agency.objects.filter(code=1).first()

        if not agency:
            return

        version = Version.objects.create(
            effective_date=self.this_first_dom,
            description="Test Version",
            created_on=self.now,
            created_by=user,
        )

        station = Station.objects.create(
            name="Test Station",
            code=1234,
            created_by=user,
            created_on=self.now,
            agency=agency,
        )

        ticket_type = TicketType.objects.create(
            description="Test Ticket Type",
            code=5678,
            created_on=self.now,
            created_by=user,
            version=version,
        )

        ticket = Ticket.objects.create(
            ticket_type=ticket_type,
            form="paperticket",
            number="0901111990710250684",
            amount=9.99,
            from_station=station,
            to_station=station,
            valid_from=self.this_first_dom,
            valid_to=self.this_last_dom,
            created_by=user,
            created_on=self.now,
        )

        TicketScan.objects.create(
            ticket=ticket,
            scanned_on=self.now,
            conductor_id="1111",
            train_id="2222",
            tour_id="3333",
            agency=agency,
            created_on=self.now,
        )

        TicketScan.objects.create(
            ticket=ticket,
            scanned_on=self.last_now,
            conductor_id="1111",
            train_id="2222",
            tour_id="3333",
            agency=agency,
            created_on=self.last_now,
        )

    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    @pytest.fixture
    def api_client(self) -> APIClient:
        return APIClient()

    def test_get_ticket_scan(self, user: User, api_client: APIClient):
        api_client.force_authenticate(user=user)
        response = api_client.get(
            "/api/ticket/scan/",
            data={
                "conductor_id": "1234",
                "train_id": "1234",
                "tour_id": "1234",
                "start_date": "2025-01-01",
                "end_date": "2025-01-31",
            },
            format="json",
        )
        assert response.status_code == HTTP_200_OK
        assert response.data == {
            "count": 0,
            "next": None,
            "previous": None,
            "results": [],
        }

    def test_get_ticket_scan_datatable(self, user: User, api_client: APIClient):
        api_client.force_authenticate(user=user)
        response = api_client.get(
            "/api/ticket/scan/?format=datatables&draw=1&columns%5B0%5D%5Bdata%5D=train_id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=conductor_id&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=tour_id&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=scanned_on&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=source.name&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=ticket.ticket_type.description&columns%5B5%5D%5Bname%5D=ticket__ticket_type__description&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=ticket.number&columns%5B6%5D%5Bname%5D=ticket__number&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=ticket.amount&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=ticket.count&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=ticket.from_station&columns%5B9%5D%5Bname%5D=ticket__from_station__name&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=ticket.to_station&columns%5B10%5D%5Bname%5D=ticket__to_station__name&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=ticket.valid_from&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=ticket.valid_to&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=3&order%5B0%5D%5Bdir%5D=desc&order%5B0%5D%5Bname%5D=&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&start_date=2025-11-26&end_date=2025-12-03&train_id=&tour_id=&conductor_id=&_=1764787882772",
            format="json",
        )
        assert response.status_code == HTTP_200_OK

    def test_get_ticket_scan_card_agency_line(
        self,
        user: User,
        api_client: APIClient,
    ):
        api_client.force_authenticate(user=user)
        query_params = {
            "start_date": self.this_first_dom.date().isoformat(),
            "end_date": self.this_last_dom.date().isoformat(),
        }
        response = api_client.get(
            "/api/ticket/scan/dashboard/card_agency_line/",
            query_params=query_params,
            format="json",
        )
        tz_est = timezone.get_current_timezone()

        assert response.status_code == HTTP_200_OK
        assert "chart" in response.data
        assert "diff" in response.data
        assert isinstance(response.data["diff"], (int, Decimal))
        assert "diff_percent" in response.data
        assert "last" in response.data
        assert "start" in response.data["last"]
        assert "end" in response.data["last"]
        assert "last_month" in response.data
        assert isinstance(response.data["last_month"], (int, Decimal))
        assert "this" in response.data
        assert "this_month" in response.data
        assert isinstance(response.data["this_month"], (int, Decimal))
        for key1 in ["this", "last"]:
            for key2 in ["start", "end"]:
                assert response.data[key1][key2].tzinfo == tz_est

    def test_get_ticket_scan_card_agency_heatmap(
        self,
        user: User,
        api_client: APIClient,
    ):
        api_client.force_authenticate(user=user)
        query_params = {
            "start_date": self.this_first_dom.date().isoformat(),
            "end_date": self.this_last_dom.date().isoformat(),
        }
        response = api_client.get(
            "/api/ticket/scan/dashboard/card_agency_heatmap/",
            query_params=query_params,
            format="json",
        )

        tz_est = timezone.get_current_timezone()

        assert response.status_code == HTTP_200_OK
        assert "chart" in response.data
        assert "labels" in response.data["chart"]
        assert "series" in response.data["chart"]
        assert "start_date" in response.data
        assert "end_date" in response.data
        for key1 in ["start_date", "end_date"]:
            assert response.data[key1].tzinfo == tz_est

    def test_get_ticket_scan_card_type_pie(
        self,
        user: User,
        api_client: APIClient,
    ):
        api_client.force_authenticate(user=user)
        attempts: list[dict[str, Any]] = [
            {"agency_id": "1", "is_live": True},
            {"agency_id": "2", "is_live": False},
        ]
        for attempt in attempts:
            query_params = {
                "start_date": self.this_first_dom.date().isoformat(),
                "end_date": self.this_last_dom.date().isoformat(),
            }
            query_params.update(attempt)

            response = api_client.get(
                "/api/ticket/scan/dashboard/card_type_pie/",
                query_params=query_params,
                format="json",
            )

            tz_est = timezone.get_current_timezone()

            assert response.status_code == HTTP_200_OK
            assert "chart" in response.data
            assert "labels" in response.data["chart"]
            assert "series" in response.data["chart"]
            assert "start_date" in response.data
            assert "end_date" in response.data
            for key1 in ["start_date", "end_date"]:
                assert response.data[key1].tzinfo == tz_est

    def test_get_ticket_scan_card_conductor_table(
        self,
        user: User,
        api_client: APIClient,
    ):
        api_client.force_authenticate(user=user)
        query_params = {
            "start_date": self.this_first_dom.date().isoformat(),
            "end_date": self.this_last_dom.date().isoformat(),
            "agency_id": "1",
        }
        response = api_client.get(
            "/api/ticket/scan/dashboard/card_conductor_table/",
            query_params=query_params,
            format="json",
        )

        assert response.status_code == HTTP_200_OK

    def test_get_ticket_scan_card_scan_table(
        self,
        user: User,
        api_client: APIClient,
    ):
        api_client.force_authenticate(user=user)

        response = api_client.get(
            "/api/ticket/scan/dashboard/card_scan_table/",
            format="json",
        )

        assert response.status_code == HTTP_200_OK

    def test_get_ticket_scan_card_train_table(
        self,
        user: User,
        api_client: APIClient,
    ):
        api_client.force_authenticate(user=user)
        query_params = {
            "start_date": self.this_first_dom.date().isoformat(),
            "end_date": self.this_last_dom.date().isoformat(),
            "agency_id": "1",
        }
        response = api_client.get(
            "/api/ticket/scan/dashboard/card_train_table/",
            query_params=query_params,
            format="json",
        )

        assert response.status_code == HTTP_200_OK

    def test_get_ticket_scan_card_time_response_line(
        self,
        user: User,
        api_client: APIClient,
    ):
        api_client.force_authenticate(user=user)
        query_params = {
            "start_date": self.this_first_dom.date().isoformat(),
            "end_date": self.this_last_dom.date().isoformat(),
            "agency_id": "1",
        }
        response = api_client.get(
            "/api/ticket/scan/dashboard/card_time_response_line/",
            query_params=query_params,
            format="json",
        )

        assert response.status_code == HTTP_200_OK

    def test_get_ticket_scan_card_time_response_pie(
        self,
        user: User,
        api_client: APIClient,
    ):
        api_client.force_authenticate(user=user)
        for agency in self.agencies:
            query_params = {
                "start_date": self.this_first_dom.date().isoformat(),
                "end_date": self.this_last_dom.date().isoformat(),
                "agency_id": agency,
            }
            response = api_client.get(
                "/api/ticket/scan/dashboard/card_time_response_pie/",
                query_params=query_params,
                format="json",
            )

            assert response.status_code == HTTP_200_OK
