import json
import logging
import re
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import boto3
import pytz
from boto3.dynamodb.conditions import Attr
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.utils import IntegrityError
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from core.general.models import TariffVersions

logger = logging.getLogger(__name__)

ITEM_LIMIT_AMOUNT_TO_DECIMAL = 1000


class TicketScanManager(models.Manager):
    def sync_with_dynamodb_pptix(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
    ):
        user = get_user_model()
        created_by = user.objects.filter(id=1).first()

        dynamodb = boto3.resource("dynamodb")
        logger.debug("DYNAMODB_TABLE_PPTICKET: %s", settings.DYNAMODB_TABLE_PPTICKET)
        ddbt_scan_event = dynamodb.Table(settings.DYNAMODB_TABLE_PPTICKET)
        response = ddbt_scan_event.scan(
            FilterExpression=Attr("ticket-scan-timestamp").between(
                start_date.isoformat(),
                end_date.isoformat(),
            ),
        )
        items = response.get("Items", [])

        latest_version = TariffVersions.objects.order_by("-pk").first()
        for item in items:
            item_ticket = {}
            try:
                logger.info(item)
                item_ticket_response = ddbt_scan_event.get_item(
                    Key={
                        "ticket-number": item["ticket-number"],
                        "ticket-scan-timestamp": "DATA",
                    },
                )
                item_ticket = item_ticket_response.get("Item", {}).get(
                    "TicketDetail",
                    {},
                )
                scanned_on = parse_datetime(item["ticket-scan-timestamp"])
                if scanned_on and not timezone.is_aware(scanned_on):
                    scanned_on = timezone.make_aware(scanned_on, timezone=pytz.UTC)
                created_at = parse_datetime(item["createdAt"])
                if created_at and not timezone.is_aware(created_at):
                    created_at = timezone.make_aware(created_at, timezone=pytz.UTC)

                (ticket, _) = self.parse_pptix_detail(
                    item=item,
                    item_ticket=item_ticket,
                    created_at=created_at,
                    created_by=created_by,
                    version=latest_version,
                )
                logger.info(item_ticket)
                self.parse_pptix_scan(
                    item=item,
                    ticket=ticket,
                    scanned_on=scanned_on,
                    created_at=created_at,
                    version=latest_version,
                )
            except Exception:
                logger.exception("Error processing item:")
                logger.debug(item)
                logger.debug(item_ticket)

    def sync_with_dynamodb_etix(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
    ):
        user = get_user_model()
        created_by = user.objects.filter(id=1).first()

        dynamodb = boto3.resource("dynamodb")
        logger.info("DYNAMODB_TABLE_ETICKET: %s", settings.DYNAMODB_TABLE_ETICKET)
        ddbt_scan_event = dynamodb.Table(settings.DYNAMODB_TABLE_ETICKET)
        response = ddbt_scan_event.scan(
            FilterExpression=Attr("ticket-scan-timestamp").between(
                start_date.isoformat(),
                end_date.isoformat(),
            ),
        )
        items = response.get("Items", [])
        for item in items:
            item_ticket_response = ddbt_scan_event.get_item(
                Key={
                    "ticket-number": item["ticket-number"],
                    "ticket-scan-timestamp": "DATA",
                },
            )
            item_ticket = item_ticket_response.get("Item", {}).get(
                "TicketDetail",
                {},
            )
            scanned_on = parse_datetime(item["ticket-scan-timestamp"])
            (ticket, _) = self.parse_etix_detail(
                item=item,
                item_ticket=item_ticket,
                created_by=created_by,
            )
            if ticket:
                logger.debug(item_ticket)
                self.parse_etix_scan(
                    item=item,
                    ticket=ticket,
                    scanned_on=scanned_on,
                )

    def parse_etix_detail(self, item, item_ticket, created_by):
        logger.info(json.dumps(item, cls=DjangoJSONEncoder))
        logger.info(json.dumps(item_ticket, cls=DjangoJSONEncoder))
        ETixTicket = apps.get_model("ticket", "ETixTicket")
        Ticket = apps.get_model("ticket", "Ticket")
        Station = apps.get_model("general", "Station")

        ticket_form = item.get("ticketForm", "eticket")
        ticket = Ticket.objects.filter(number=item["ticket-number"]).first()
        e_ticket = ETixTicket.objects.filter(ticket=ticket).first()

        from_station = Station.objects.filter(
            code=item_ticket["fromStation"],
        ).first()
        to_station = Station.objects.filter(
            code=item_ticket["toStation"],
        ).first()

        if not ticket:
            ticket_values = {
                "form": ticket_form,
                "number": item_ticket["eTicketNo"],
                "amount": item_ticket["price"],
                "valid_from": item_ticket["activateStart"],
                "valid_to": item_ticket["activateStart"],
                "from_station": from_station,
                "to_station": to_station,
                "created_by": created_by,
                "created_on": item_ticket["deviceUtc"],
            }
            ticket = Ticket.objects.create(**ticket_values)
        if not e_ticket:
            e_ticket_values = {
                "ticket": ticket,
                "e_ticket_no": item_ticket["eTicketNo"],
                "price": item_ticket["price"],
                "discount_code": item_ticket["discountCode"],
                "product_id": item_ticket["productId"],
                "activate_start": item_ticket["activateStart"],
                "device_utc": item_ticket["deviceUtc"],
                "from_station": from_station,
                "to_station": to_station,
                "parent_product_id": item_ticket["parentProductId"],
                "line": item_ticket["line"],
                "abi": item_ticket["ABI"],
                "act": item_ticket["Act"],
                "tkt_oc": item_ticket["TktOC"],
            }
            e_ticket = ETixTicket.objects.create(**e_ticket_values)

        return (ticket, e_ticket)

    def parse_etix_scan(self, item, ticket, scanned_on=None):
        TicketSource = apps.get_model("ticket", "TicketSource")
        Company = apps.get_model("general", "Company")
        ticket_source = TicketSource.objects.filter(
            code=item.get("source", None),
        ).first()
        company = Company.objects.filter(code=item.get("company", None)).first()
        if scanned_on is None:
            scanned_on = parse_datetime(item["ticket-scan-timestamp"])
        scan_values = {
            "ticket": ticket,
            "tour_id": item["tourId"],
            "conductor_id": item["conductorId"],
            "train_id": item["trainId"],
            "scanned_on": scanned_on,
            "created_on": item["createdAt"],
            "company": company,
            "source": ticket_source,
        }
        (_scan, _created) = self.update_or_create(
            ticket=ticket,
            scanned_on=scan_values["scanned_on"],
            defaults=scan_values,
        )

    def parse_pptix_detail(  # noqa: C901, PLR0912, PLR0915
        self, item, item_ticket, created_by, created_at=None, version=None
    ):
        logger.debug(json.dumps(item, cls=DjangoJSONEncoder))
        logger.debug(json.dumps(item_ticket, cls=DjangoJSONEncoder))
        _now = timezone.now()
        SalesPackets = apps.get_model("tariff", "SalesPackets")
        PaperTicket = apps.get_model("ticket", "PaperTicket")
        Ticket = apps.get_model("ticket", "Ticket")

        ZoneStation = apps.get_model("general", "ZoneStation")
        if not created_at:
            created_at = parse_datetime(item["createdAt"])
            if created_at and not timezone.is_aware(created_at):
                created_at = timezone.make_aware(created_at, timezone=pytz.UTC)

        ticket_form = item.get("ticketForm", "paperticket")
        if not re.match(r"^\d+$", item["ticket-number"]):
            return (None, False)

        ticket_breakdown = PaperTicket.objects.decode_number(
            item["ticket-number"],
        )
        _sales_detail_ev_sequ_no = str(round(_now.timestamp() * 1000))[-10:]
        ticket = Ticket.objects.filter(number=item["ticket-number"]).first()
        paper_ticket = PaperTicket.objects.filter(ticket=ticket).first()

        if isinstance(item_ticket["valid_from"], str):
            item_ticket["valid_from"] = parse_datetime(
                item_ticket["valid_from"],
            )
        if not timezone.is_aware(item_ticket["valid_from"]):
            item_ticket["valid_from"] = timezone.make_aware(
                item_ticket["valid_from"],
                timezone=pytz.UTC,
            )
        if isinstance(item_ticket["valid_to"], str):
            item_ticket["valid_to"] = parse_datetime(
                item_ticket["valid_to"],
            )
        if not timezone.is_aware(item_ticket["valid_to"]):
            item_ticket["valid_to"] = timezone.make_aware(
                item_ticket["valid_to"],
                timezone=pytz.UTC,
            )

        sales_packet = SalesPackets.objects.filter(
            packet_id=int(item_ticket["ticket_type"]),
            version=version,
        ).first()
        from_station = ZoneStation.objects.filter(
            zone_station_id=item_ticket["from"], version=version
        ).first()
        to_station = ZoneStation.objects.filter(
            zone_station_id=item_ticket["to"], version=version
        ).first()
        if from_station is None or to_station is None:
            return (None, False)
        via_station = ZoneStation.objects.filter(
            zone_station_id=item_ticket.get("via", None),
            version=version,
        ).first()
        from_return = ZoneStation.objects.filter(
            zone_station_id=item_ticket["from_return"],
            version=version,
        ).first()
        to_return = ZoneStation.objects.filter(
            zone_station_id=item_ticket["to_return"],
            version=version,
        ).first()
        via_return = ZoneStation.objects.filter(
            zone_station_id=item_ticket["via_return"],
            version=version,
        ).first()
        if isinstance(item_ticket["amount"], str):
            if "." in item_ticket["amount"]:
                item_ticket["amount"] = Decimal(item_ticket["amount"])
            else:
                item_ticket["amount"] = Decimal(int(item_ticket["amount"]) / 100)
        elif (
            isinstance(item_ticket["amount"], Decimal)
            and item_ticket["amount"].as_integer_ratio()[1] == 1
            # and item_ticket["amount"] > ITEM_LIMIT_AMOUNT_TO_DECIMAL
        ):
            item_ticket["amount"] = Decimal(int(item_ticket["amount"]) / 100)
        ticket_values = {
            "form": ticket_form,
            "sales_packet": sales_packet,
            "number": item_ticket["ticket_number"],
            "amount": item_ticket["amount"],
            "valid_from": item_ticket["valid_from"],
            "valid_to": item_ticket["valid_to"],
            "from_station": from_station,
            "to_station": to_station,
            "user_new": created_by,
            "time_new": created_at,
            "device_id": ticket_breakdown["device"]["id"],
            "device_class_id": ticket_breakdown["device"]["class_id"],
            "sales_transaction_no": ticket_breakdown["trans_seq"],
            "sales_detail_ev_sequ_no": _sales_detail_ev_sequ_no,
            "version": version,
        }
        if not ticket:
            logger.info(ticket_values)
            try:
                ticket = Ticket.objects.create(**ticket_values)
            except IntegrityError:
                logger.exception("Error creating ticket:")
                logger.debug(ticket_values)
                return (None, False)
        if not paper_ticket:
            paper_ticket_values = {
                "ticket": ticket,
                "sales_packet": sales_packet,
                "number": item_ticket["ticket_number"],
                "amount": item_ticket["amount"],
                "valid_from": item_ticket["valid_from"],
                "valid_to": item_ticket["valid_to"],
                "from_station_id": from_station.zone_station_id,
                "from_type": from_station.type,
                "to_station_id": to_station.zone_station_id,
                "to_type": to_station.type,
                "via_station_id": via_station.zone_station_id if via_station else None,
                "via_type": via_station.type if via_station else None,
                "from_return_id": from_return.zone_station_id if from_return else None,
                "from_return_type": from_return.type if from_return else None,
                "to_return_id": to_return.zone_station_id if to_return else None,
                "to_return_type": to_return.type if to_return else None,
                "via_return_id": via_return.zone_station_id if via_return else None,
                "via_return_type": via_return.type if via_return else None,
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
                "version_id": 22,
            }
            paper_ticket = PaperTicket.objects.create(**paper_ticket_values)
        return (ticket, paper_ticket)

    def parse_pptix_scan(
        self, item, ticket, scanned_on=None, created_at=None, version=None
    ):
        if ticket is None:
            return
        TicketSource = apps.get_model("ticket", "TicketSource")
        Company = apps.get_model("general", "Company")

        if not scanned_on:
            scanned_on = parse_datetime(item["ticket-scan-timestamp"])
            if scanned_on and not timezone.is_aware(scanned_on):
                scanned_on = timezone.make_aware(scanned_on, timezone=pytz.UTC)
        if not created_at:
            created_at = parse_datetime(item["createdAt"])
            if created_at and not timezone.is_aware(created_at):
                created_at = timezone.make_aware(created_at, timezone=pytz.UTC)

        ticket_source = TicketSource.objects.filter(
            code=item.get("source", None),
        ).first()
        company_id = item.get("agency", None)
        if re.match(r"^\d+$", item["ticket-number"]):
            PaperTicket = apps.get_model("ticket", "PaperTicket")
            ticket_breakdown = PaperTicket.objects.decode_number(
                item["ticket-number"],
            )
            if company_id is None:
                company_id = ticket_breakdown["device"]["company"]

        company = Company.objects.filter(pk=company_id).first()
        if isinstance(item["conductorId"], str) and re.match(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
            item["conductorId"],
        ):
            conductor_uuid = UUID(item["conductorId"])
            item["conductorId"] = conductor_uuid.int & 0xFFFFFFFF  # pyright: ignore[reportOperatorIssue]

        scan_values = {
            "ticket_id": ticket.pk,
            "tour_id": int(item["tourId"]),
            "conductor_id": int(item["conductorId"]),
            "train_id": int(item["trainId"]),
            "scanned_on": scanned_on,
            "time_new": created_at,
            "company_id": company.pk if company else None,
            "source": ticket_source,
        }

        (_scan, _created) = self.get_or_create(
            ticket=ticket,
            scanned_on=scan_values["scanned_on"],
            defaults=scan_values,
        )


class PaperTicketManager(models.Manager):
    def decode_number(self, number: str):
        return {
            "place_holder": number[0],
            "device": {
                "id": number[1:9],
                "station": number[1:5],
                "company": int(number[5]),
                "class": int(number[6]),
                "class_id": (int(number[5]) * 100) + int(number[6]),
                "no": number[7:9],
            },
            "issue_date": datetime.strptime(number[9:15], r"%d%m%y").date(),  # noqa: DTZ007
            "trans_seq": number[15:19],
        }

    def encode_number(  # noqa: C901, PLR0913
        self,
        station: int,
        device_class: int,
        company: int,
        no: int,
        issue_date: date,
        trans_sec: int,
    ):
        _station_id = None
        _device_class_id = None
        _company_id = None
        if isinstance(station, str):
            _station_id = int(station)
        elif isinstance(station, int):
            _station_id = station
        elif isinstance(station, models.Model):
            _station_id = station.pk
        if isinstance(device_class, str):
            _device_class_id = int(device_class)
        elif isinstance(device_class, int):
            _device_class_id = device_class
        elif isinstance(device_class, models.Model):
            _device_class_id = device_class.pk
        if isinstance(company, str):
            _company_id = int(company)
        elif isinstance(company, int):
            _company_id = company
        elif isinstance(company, models.Model):
            _company_id = company.pk

        if _station_id > 9999:  # noqa: PLR2004
            msg = "Station ID must be less than 9999"
            raise ValueError(msg)
        if _device_class_id > 10:  # noqa: PLR2004
            class_number = str(_device_class_id)
            _company_id = int(class_number[0])
            _class = int(class_number[2])
        else:
            _class = int(_device_class_id)
        return (
            f"0{_station_id:04}{_company_id:1}{_class:1}"
            f"{no:02}{issue_date:%d%m%y}{trans_sec:04}"
        )
