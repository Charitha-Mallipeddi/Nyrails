import logging
import re
from collections import OrderedDict

import boto3
from django.core.validators import RegexValidator
from rest_framework.decorators import action
from rest_framework.response import Response

from core.dynamodb.rest_framework.viewsets import DynamoDbViewSet

logger = logging.getLogger(__name__)


class DynamoDBRecordViewSet(DynamoDbViewSet):
    table_name: str

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, table_name: str):
        self.table_name = table_name
        return super().list(request)

    @action(detail=False, methods=["get"], url_path="datatable/config")
    def datatable_config(self, request, table_name: str):  # noqa: C901
        table_name_validator = RegexValidator(
            regex=r"^[a-zA-Z0-9_.-]+$",
            message="Invalid table name",
            code="invalid_table_name",
        )
        table_name_validator(table_name)
        client = boto3.client("dynamodb")
        table_info = client.describe_table(TableName=table_name)
        table_data = client.scan(TableName=table_name, Limit=10)
        columns = OrderedDict()
        renderers = {
            "string": "renderer_str",
            "date": "mta.datatable.renderer.date_time",
        }
        for row in table_data["Items"]:
            for column in row:
                if column in columns:
                    continue
                column_type = "string"
                if "N" in row[column]:
                    column_type = "num"
                elif "S" in row[column]:
                    if re.match(
                        r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,}))?(Z|[+-]\d{2}:\d{2})?$",
                        row[column]["S"],
                    ):
                        column_type = "date"
                columns[column] = {
                    "data": column,
                    "type": column_type,
                    "title": column,
                    "defaultContent": "",
                }
                if column_type in renderers:
                    columns[column]["render"] = renderers[column_type]

        column_list = []
        column_schema_list = []
        table_columns = []
        table_order = []
        for key_schema in table_info["Table"]["KeySchema"]:
            if key_schema["AttributeName"] in columns:
                column_list.append(key_schema["AttributeName"])
                column_schema_list.append(key_schema["AttributeName"])
                table_columns.append(columns[key_schema["AttributeName"]])

        for column in columns.values():
            if column["data"] in column_list:
                continue
            table_columns.append(column)
            column_list.append(column["data"])

        for schema_key in column_schema_list:
            column_index = column_list.index(schema_key)
            table_order.append([column_index, "asc"])

        rtn = {
            "table": {
                "ajax": "/api/dynamodb/scan-event/?format=datatables",
                "processing": True,
                "serverSide": True,
                "columns": table_columns,
                "order": table_order,
            },
        }
        logger.debug(table_data)
        return Response(rtn)
