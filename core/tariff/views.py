from core.tariff.models import SalesPackets
from django_tomselect.autocompletes import AutocompleteModelView

class SalesPacketAutoCompleteView(AutocompleteModelView):
    queryset = SalesPackets.objects.all()
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET.get('query'):
            qs = qs.filter(description__icontains=self.request.GET['query'])
        return qs

sales_packet_autocomplete_view = SalesPacketAutoCompleteView.as_view()