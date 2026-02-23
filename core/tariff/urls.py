from django.urls import path
from core.tariff import views

app_name = "tariff"

urlpatterns = [
    path("sales-packet/autocomplete/", views.SalesPacketAutoCompleteView.as_view(), name="sales-packet-autocomplete"),
]