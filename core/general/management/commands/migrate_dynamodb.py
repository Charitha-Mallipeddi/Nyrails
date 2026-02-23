import logging
from typing import TYPE_CHECKING

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
    from mypy_boto3_dynamodb.client import DynamoDBClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Apply DynamoDB migrations"
    # dynamodb
    # dynamodb_client

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dynamodb = boto3.resource("dynamodb")
        self.dynamodb_client = boto3.client("dynamodb")

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.check_table(settings.DYNAMODB_TABLE_ETICKET)
        self.check_table(settings.DYNAMODB_TABLE_PPTICKET)

    def check_table(self, table_name):
        try:
            # Check if the table exists
            self.dynamodb_client.describe_table(TableName=table_name)
            logger.info("Table '%s' already exists.", table_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                logger.warning(
                    "Table '%s' does not exist. Creating table...",
                    table_name,
                )
                table = self.dynamodb.create_table(
                    KeySchema=[
                        {
                            "AttributeName": "ticket-number",
                            "KeyType": "HASH",
                        },
                        {
                            "AttributeName": "ticket-scan-timestamp",
                            "KeyType": "RANGE",
                        },
                    ],
                    AttributeDefinitions=[
                        {
                            "AttributeName": "ticket-number",
                            "AttributeType": "S",
                        },
                        {
                            "AttributeName": "ticket-scan-timestamp",
                            "AttributeType": "S",
                        },
                        {
                            "AttributeName": "tour",
                            "AttributeType": "S",
                        },
                        {
                            "AttributeName": "conductor-id",
                            "AttributeType": "S",
                        },
                        {
                            "AttributeName": "tkt-type-id",
                            "AttributeType": "S",
                        },
                    ],
                    GlobalSecondaryIndexes=[
                        {
                            "IndexName": "gsi-tour",
                            "KeySchema": [
                                {
                                    "AttributeName": "tour",
                                    "KeyType": "HASH",
                                },
                                {
                                    "AttributeName": "ticket-scan-timestamp",
                                    "KeyType": "RANGE",
                                },
                            ],
                            "Projection": {
                                "ProjectionType": "INCLUDE",
                                "NonKeyAttributes": [
                                    "conductor-id",
                                    "tkt-type-id",
                                ],
                            },
                        },
                        {
                            "IndexName": "gsi-conductor-id",
                            "KeySchema": [
                                {
                                    "AttributeName": "conductor-id",
                                    "KeyType": "HASH",
                                },
                                {
                                    "AttributeName": "ticket-scan-timestamp",
                                    "KeyType": "RANGE",
                                },
                            ],
                            "Projection": {
                                "ProjectionType": "ALL",
                            },
                        },
                        {
                            "IndexName": "gsi-tkt-type-id",
                            "KeySchema": [
                                {
                                    "AttributeName": "tkt-type-id",
                                    "KeyType": "HASH",
                                },
                                {
                                    "AttributeName": "ticket-scan-timestamp",
                                    "KeyType": "RANGE",
                                },
                            ],
                            "Projection": {
                                "ProjectionType": "KEYS_ONLY",
                            },
                        },
                    ],
                    BillingMode="PAY_PER_REQUEST",
                    TableName=table_name,
                )
                table.wait_until_exists()
                logger.info("Table '%s' created successfully.", table_name)
            else:
                logger.exception("Error checking for table '%s'", table_name)
