import csv
import gzip
import json
import logging
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load AWS CSV dump unto DynamoDB table"
    dynamodb = None
    dynamodb_client = None
    verbosity = 0

    def add_arguments(self, parser):
        parser.add_argument(
            "args",
            metavar="fixture",
            nargs="+",
            help="Fixture labels.",
        )
        parser.add_argument(
            "--table",
            type=str,
            required=True,
            help="Nominates a specific table to load fixtures into.",
        )

    def handle(self, *fixture_labels, **options):
        self.table_name = options.get("table")
        if options.get("verbosity"):
            self.verbosity = int(options["verbosity"])

        self.loaddata(fixture_labels)

    def loaddata(self, fixture_labels):
        self.dynamodb = boto3.resource("dynamodb")
        self.dynamodb_client = boto3.client("dynamodb")

        try:
            # Check if the table exists
            self.dynamodb_client.describe_table(TableName=self.table_name)
            logger.info("Table '%s' already exists.", self.table_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                logger.exception("Table '%s' does not exist.", self.table_name)
                return

        table = self.dynamodb.Table(self.table_name)

        for fixture_label in fixture_labels:
            with gzip.open(fixture_label, "rt") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    item = {k: v for k, v in row.items() if v}
                    if "TicketDetail" in item:
                        ticket_detail = json.loads(item["TicketDetail"])
                        if isinstance(ticket_detail, dict):
                            for key, value in ticket_detail.items():
                                if "S" in value:
                                    ticket_detail[key] = str(value["S"])
                                elif "NULL" in value:
                                    ticket_detail[key] = None
                                elif "N" in value:
                                    ticket_detail[key] = Decimal(value["N"])
                            item["TicketDetail"] = ticket_detail
                    table.put_item(Item=item)
                    if self.verbosity and self.verbosity >= 1:
                        print(".", end="", flush=True)
