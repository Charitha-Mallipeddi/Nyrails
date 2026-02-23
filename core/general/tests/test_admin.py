from http import HTTPStatus

import pytest
from django.test import Client, TestCase
from django.urls import reverse

from core.general.admin import AdminStationModelResource
from core.general.models import Company
from core.mofa.models import ZoneStation
from core.users.models import User


@pytest.mark.django_db
class TestGeneralAdmin(TestCase):
    fixtures = ["core/users/fixtures.json", "core/general/fixtures.json.gz"]

    def setUp(self):
        self.admin_user = User.objects.get(pk=1)
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_station_save_model(self):
        url = reverse("admin:general_station_add")
        agency = Company.objects.filter(company_id=1).first()
        response = self.client.post(
            url,
            {
                "agency": agency.pk if agency else None,
                "code": "9999",
                "name": "TestStation",
                "name_short": "TestStation",
                "name_long": "TestStation",
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        station = ZoneStation.objects.filter(zonestationid="9999").first()
        if station:
            url = reverse("admin:general_station_change", args=[station.pk])
            response = self.client.post(
                url,
                {
                    "agency": agency.pk if agency else None,
                    "code": "9999",
                    "name": "TestStationEdit",
                    "name_short": "TestStationEdit",
                    "name_long": "TestStationEdit",
                },
            )
            assert response.status_code == HTTPStatus.FOUND
            resource = AdminStationModelResource()
            delattr(station, "timenew")
            resource.after_init_instance(
                instance=station, new=False, row={}, user=self.admin_user
            )
            assert station.timenew is not None
            assert station.usernew == self.admin_user
            assert station.timechange is not None
            assert station.timenew == self.admin_user
