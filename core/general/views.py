from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django_tomselect.autocompletes import AutocompleteModelView
from core.general.models import Company, Department, Country, ZoneStation, Status, ConnectingService


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"

home_view = HomeView.as_view()

class CompanyAutoCompleteView(AutocompleteModelView):
    model = Company
    search_lookups = ['name__icontains', 'short_name__icontains']
    value_fields = ['company_id', 'name', 'short_name']


company_autocomplete_view = CompanyAutoCompleteView.as_view()


class DepartmentAutoCompleteView(AutocompleteModelView):
    model = Department
    search_lookups = ['description__icontains']
    value_fields = ['id', 'description']


department_autocomplete_view = DepartmentAutoCompleteView.as_view()


class CountryAutoCompleteView(AutocompleteModelView):
    model = Country
    search_lookups = ['description__icontains', 'code__icontains']
    value_fields = ['id', 'description', 'code']


country_autocomplete_view = CountryAutoCompleteView.as_view()


class StationAutoCompleteView(AutocompleteModelView):
    model = ZoneStation
    search_lookups = ['description__icontains']
    value_fields = ['version_id', 'zone_station_id', 'type']


station_autocomplete_view = StationAutoCompleteView.as_view()


class StatusAutoCompleteView(AutocompleteModelView):
    model = Status
    search_lookups = ['description__icontains']
    value_fields = ['id', 'description']


status_autocomplete_view = StatusAutoCompleteView.as_view()


class ConnectingServiceAutoCompleteView(AutocompleteModelView):
    model = ConnectingService
    search_lookups = ['description__icontains']
    value_fields = ['id', 'description']


connecting_service_autocomplete_view = ConnectingServiceAutoCompleteView.as_view()


class ZoneStationAutoCompleteView(AutocompleteModelView):
    queryset = ZoneStation.objects.all()
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET.get('query'):
            qs = qs.filter(description__icontains=self.request.GET['query'])
        return qs


zone_station_autocomplete_view = ZoneStationAutoCompleteView.as_view()