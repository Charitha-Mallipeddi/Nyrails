from multiprocessing import context
from typing import Any
import boto3
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.
class DynamoDBTablesView(LoginRequiredMixin, TemplateView):
    template_name = "dynamodb/tables.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        client = boto3.client("dynamodb")
        context["tables"] = client.list_tables()["TableNames"]

        return context

dynamodb_tables_view = DynamoDBTablesView.as_view()

# Create your views here.
class DynamoDBRecordsView(LoginRequiredMixin, TemplateView):
    template_name = "dynamodb/records.html"

dynamodb_records_view = DynamoDBRecordsView.as_view()
