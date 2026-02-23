from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter


from .views import DynamoDBRecordViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register(r"dynamodb/(?P<table_name>[\w-]+)", DynamoDBRecordViewSet, basename="dynamodb_table_records")

app_name = "dynamodb"
dynamodb_router = router
