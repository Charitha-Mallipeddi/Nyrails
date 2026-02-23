from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from .views import TicketScanViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("ticket/scan", TicketScanViewSet, basename="ticket_scan")

app_name = "ticket"
ticket_router = router
