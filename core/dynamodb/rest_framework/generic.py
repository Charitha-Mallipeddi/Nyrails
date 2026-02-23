from typing import override

import boto3
from rest_framework.viewsets import GenericViewSet

from core.dynamodb.rest_framework.filters import DynamoDbDatatablesBaseFilterBackend
from core.dynamodb.rest_framework.serializer import DynamoDbSerializer


class GenericDynamoDbViewSet(GenericViewSet):
    table_name: str
    serializer_class = DynamoDbSerializer
    filter_backends = [DynamoDbDatatablesBaseFilterBackend]

    def get_table_name(self) -> str:
        return self.table_name

    @override
    def get_queryset(self) -> list[dict]:  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
        client = boto3.client("dynamodb")
        paginator = client.get_paginator("scan")
        params = {"TableName": self.get_table_name()}
        items = []
        for page in paginator.paginate(**params):
            items.extend(page["Items"])
        self._datatables_filtered_count = len(items)
        self._datatables_total_count = self._datatables_filtered_count
        return items
