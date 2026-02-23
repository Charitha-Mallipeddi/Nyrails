import pytest

from core.general.models import Agency, Line, Station, Version, ServiceProvider
from django.utils import timezone


@pytest.mark.django_db
def test_agency_model():
    agency = Agency(name="Test Agency", code="1234", abbr="TEST")
    assert agency.name == "Test Agency"
    assert agency.code == "1234"
    assert agency.abbr == "TEST"
    assert str(agency) == "Test Agency[1234]"


@pytest.mark.django_db
def test_line_model():
    line = Line(name="Test Line", code="1234", is_valid=True, class_name="css_class")

    assert line.name == "Test Line"
    assert line.code == "1234"
    assert line.is_valid
    assert line.class_name == "css_class"
    assert str(line) == "Test Line[1234]"

@pytest.mark.django_db
def test_station_model():
    station = Station(name="Test Station", code="1234")
    assert station.name == "Test Station"
    assert str(station) == "Test Station[1234]"

@pytest.mark.django_db
def test_version_model():
    now = timezone.now()
    version = Version(description="Test Line", effective_date=now)

    assert version.description == "Test Line"
    assert str(version) == f"Test Line [{now.strftime('%Y-%m-%d %H:%M:%S')}]"

@pytest.mark.django_db
def test_service_provider_model():

    provider = ServiceProvider(code="1234", name="Test Service Provider", short_name="Test Srv Prov Short")

    assert provider.code == "1234"
    assert provider.name == "Test Service Provider"
    assert provider.short_name == "Test Srv Prov Short"
    assert str(provider) == "Test Service Provider[1234]"
