from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from core.dynamodb.api.urls import dynamodb_router
from core.refunds.api.urls import router as refunds_router
from core.ticket.api.urls import ticket_router
from core.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.registry.extend(ticket_router.registry)
router.registry.extend(dynamodb_router.registry)
router.registry.extend(refunds_router.registry)


app_name = "api"
urlpatterns = router.urls
