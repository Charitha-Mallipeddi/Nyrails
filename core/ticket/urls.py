from django.urls import path

from .views import (
    ticket_detail_modal_view,
    ticket_scan_dashboard_view,
    ticket_scan_detail_view,
)

app_name = "ticket"
urlpatterns = [
    path("scan/", view=ticket_scan_dashboard_view, name="scan_dashboard"),
    path("scan/detail/", view=ticket_scan_detail_view, name="scan_detail"),
    path("<pk>/modal", view=ticket_detail_modal_view, name="modal"),
]
