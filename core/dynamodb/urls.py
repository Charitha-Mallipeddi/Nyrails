from django.urls import path

from .views import (
    dynamodb_tables_view,
    dynamodb_records_view
)

app_name = "dynamodb"
urlpatterns = [
    path("", view=dynamodb_tables_view, name="tables"),
    path("<str:table_name>", view=dynamodb_records_view, name="records"),
]
