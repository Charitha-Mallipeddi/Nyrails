from calendar import monthrange
from datetime import UTC, date

import pytest
from dateutil import relativedelta
from django.test import RequestFactory
from django.utils import timezone

from core.general.models import Agency, Station, Version
from core.ticket.models import Ticket, TicketType
from core.ticket.views import (
    TicketDetailModalView,
    TicketScanDashboardView,
    TicketScanDetailView,
)
from core.users.models import User


@pytest.fixture
def ticket():
    now = timezone.now()
    this_first_dom = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    _, this_num_days = monthrange(this_first_dom.year, this_first_dom.month)
    this_last_dom = this_first_dom.replace(
        day=this_num_days, hour=23, minute=59, second=59, microsecond=999
    )

    user = User.objects.create(username="test")

    agency = Agency.objects.filter(code=1).first()
    if not agency:
        agency = Agency.objects.create(code=1, name="Test Agency", abbr="TEST")

    version = Version.objects.create(
        effective_date=this_first_dom,
        description="Test Version",
        created_on=now,
        created_by=user,
    )

    station = Station.objects.create(
        name="Test Station",
        code=1234,
        created_by=user,
        created_on=now,
        agency=agency,
    )

    ticket_type = TicketType.objects.create(
        description="Test Ticket Type",
        code=5678,
        created_on=now,
        created_by=user,
        version=version,
    )

    return Ticket.objects.create(
        ticket_type=ticket_type,
        form="paperticket",
        number="0901111990710250684",
        amount=9.99,
        from_station=station,
        to_station=station,
        valid_from=this_first_dom,
        valid_to=this_last_dom,
        created_by=user,
        created_on=now,
    )


class TestBaseView:
    def setup_method(self):
        self.agencies = ["1", "2"]
        self.now = timezone.now()
        self.this_first_dom = self.now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        _, this_num_days = monthrange(
            self.this_first_dom.year, self.this_first_dom.month
        )
        self.this_last_dom = self.this_first_dom.replace(
            day=this_num_days, hour=23, minute=59, second=59, microsecond=999
        )

        self.last_now = self.now - relativedelta.relativedelta(months=1)
        self.last_first_dom = self.last_now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        ).date()
        _, last_num_days = monthrange(
            self.last_first_dom.year, self.last_first_dom.month
        )
        self.last_last_dom = self.last_first_dom.replace(day=last_num_days)


class TestTicketScanDashboardView(TestBaseView):
    def test_get_context_data(self, user: User, rf: RequestFactory):
        view = TicketScanDashboardView()
        query_params = {
            "start_date": self.this_first_dom.date().isoformat(),
            "end_date": self.this_last_dom.date().isoformat(),
        }
        request = rf.get("/fake-url/", query_params=query_params)
        request.user = user

        view.request = request
        context = view.get_context_data()
        assert "start_date" in context
        assert "start_date_time" in context
        assert context["start_date_time"].tzinfo == UTC
        assert "end_date" in context
        assert "end_date_time" in context


class TestTicketScanDetailView(TestBaseView):
    def test_get_context_data(self, user: User, rf: RequestFactory):
        view = TicketScanDetailView()
        train_id = str(99999)
        tour_id = str(88888)
        query_params = {
            "start_date": self.this_first_dom.date().isoformat(),
            "end_date": self.this_last_dom.date().isoformat(),
            "train_id": train_id,
            "tour_id": tour_id,
        }
        request = rf.get("/fake-url/", query_params=query_params)
        request.user = user

        view.request = request
        context = view.get_context_data()
        assert "start_date" in context
        assert isinstance(context["start_date"], date)
        assert "end_date" in context
        assert isinstance(context["end_date"], date)
        assert context["conductor_id"] is None
        assert context["train_id"] == train_id
        assert context["tour_id"] == tour_id


@pytest.mark.django_db
class TestTicketDetailModalView(TestBaseView):
    def test_get_context_data(self, user: User, rf: RequestFactory, ticket: Ticket):
        view = TicketDetailModalView()
        request = rf.get("/fake-url/")
        request.user = user
        view.request = request
        view.kwargs = {
            "pk": ticket.pk,
        }
        view.object = view.get_object()
        context = view.get_context_data()
        assert "top_logo" in context
        assert "images/" in context["top_logo"]
