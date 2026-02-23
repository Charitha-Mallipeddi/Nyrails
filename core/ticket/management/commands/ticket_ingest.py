import logging
from datetime import datetime, timedelta

import boto3
from boto3.dynamodb.conditions import Attr
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_date

from core.general.models import Station
from core.ticket.models import Ticket, TicketScan, TicketSource, TicketType

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate Random Scan Test Data"

    def add_arguments(self, parser):
        parser.add_argument("--start-date", "-S", type=str)
        parser.add_argument("--end-date", "-E", type=str)

    def handle(self, *args, **options):
        logger.info("Gather Dynamodb data and normalize it")
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=1)
        if options.get("end_date"):
            pd = parse_date(options["end_date"])
            if pd:
                end_date = pd

        if options.get("start_date"):
            pd = parse_date(options["start_date"])
            if pd:
                start_date = pd

        user = get_user_model()
        created_by = user.objects.filter(id=1).first()
        ticket_source_id = TicketSource.TIMS

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(settings.DYNAMODB_TABLE_PPTICKET)
        response = table.scan(
            FilterExpression=Attr("ticket-scan-timestamp").between(
                start_date.isoformat(),
                end_date.isoformat(),
            ),
        )
        items = response.get("Items", [])
        for item in items:
            ticket_form = item.get("ticketForm", "paperticket")
            ticket = Ticket.objects.filter(number=item["ticket-number"]).first()
            if not ticket:
                item_ticket_response = table.get_item(
                    Key={
                        "ticket-number": item["ticket-number"],
                        "ticket-scan-timestamp": "DATA",
                    },
                )

                item_ticket = item_ticket_response.get("Item", {}).get(
                    "TicketDetail",
                    {},
                )
                ticket_type = TicketType.objects.filter(
                    code=item_ticket["ticket_type"],
                ).first()
                from_station = Station.objects.filter(code=item_ticket["from"]).first()
                to_station = Station.objects.filter(code=item_ticket["to"]).first()
                via_station = Station.objects.filter(code=item_ticket["via"]).first()
                from_return = Station.objects.filter(
                    code=item_ticket["from_return"],
                ).first()
                to_return = Station.objects.filter(
                    code=item_ticket["to_return"],
                ).first()
                via_return = Station.objects.filter(
                    code=item_ticket["via_return"],
                ).first()

                ticket_values = {
                    "ticket_type": ticket_type,
                    "source_id": ticket_source_id,
                    "number": item_ticket["ticket_number"],
                    "amount": item_ticket["amount"],
                    "valid_from": item_ticket["valid_from"],
                    "valid_to": item_ticket["valid_to"],
                    "from_station": from_station,
                    "to_station": to_station,
                    "via_station": via_station,
                    "from_return": from_return,
                    "to_return": to_return,
                    "via_return": via_return,
                    "count_passenger_category_1": item_ticket.get(
                        "count_passenger_category_1",
                        1,
                    ),
                    "start_connection_service": item_ticket.get(
                        "start_connection_service",
                        1,
                    ),
                    "end_connection_service": item_ticket.get(
                        "end_connection_service",
                        1,
                    ),
                    "created_by": created_by,
                    "created_on": item["createdAt"],
                }
                ticket = Ticket.objects.create(**ticket_values)
            scan_values = {
                "ticket": ticket,
                "ticket_form": ticket_form,
                "tour_id": item["tourId"],
                "conductor_id": item["conductorId"],
                "train_id": item["trainId"],
                "scanned_on": datetime.fromisoformat(item["ticket-scan-timestamp"]),
                "created_on": item["createdAt"],
            }
            (_scan, _created) = TicketScan.objects.update_or_create(
                ticket=ticket,
                scanned_on=scan_values["scanned_on"],
                defaults=scan_values,
            )
