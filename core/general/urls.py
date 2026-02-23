from django.urls import path
from core.general import views

app_name = "general"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("company/autocomplete/", views.company_autocomplete_view, name="company-autocomplete"),
    path("department/autocomplete/", views.department_autocomplete_view, name="department-autocomplete"),
    path("country/autocomplete/", views.country_autocomplete_view, name="country-autocomplete"),
    path("station/autocomplete/", views.station_autocomplete_view, name="station-autocomplete"),
    path("status/autocomplete/", views.status_autocomplete_view, name="status-autocomplete"),
    path("connecting-service/autocomplete/", views.connecting_service_autocomplete_view, name="connecting-service-autocomplete"),
    path("zone-station/autocomplete/", views.zone_station_autocomplete_view, name="zone-station-autocomplete"),
]
