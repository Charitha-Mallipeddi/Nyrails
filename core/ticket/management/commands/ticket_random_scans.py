# ruff: noqa: S311,T201

import datetime
import json
import logging
from pathlib import Path
from random import choice, choices, randrange

import boto3
import boto3.dynamodb
import boto3.dynamodb.table
import boto3.resources.base
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.general.models import Company, DeviceClass, TariffVersions, TVMStation
from core.tariff.models import SalesPackets
from core.ticket.model_types import TicketFormType
from core.ticket.models import (
    ETixTicket,
    PaperTicket,
    Ticket,
    TicketScan,
    TicketSource,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate Random Scan Test Data"
    dynamodb: boto3.resources.base.ServiceResource
    ddbt_scan_event: boto3.dynamodb.table.TableResource
    ddbt_etix_event: boto3.dynamodb.table.TableResource

    def add_arguments(self, parser):
        parser.add_argument("--count", "-c", type=int, default=1000)
        parser.add_argument("--days", "-d", type=int, default=15)
        parser.add_argument("--date", "-D", type=str)
        parser.add_argument("--dynamodb", action="store_true", default=False)
        parser.add_argument("--ticket-form", type=str)
        parser.add_argument("--truncate", action="store_true", default=False)

    def handle(self, *args, **options):  # noqa: C901, PLR0912, PLR0915
        print("Generating random scan test data")
        _static = json.loads(
            Path(__file__).resolve().parent.joinpath("static_data.json").read_text(),
        )
        latest_version = TariffVersions.objects.order_by("-pk").first()
        user = get_user_model()
        created_by = user.objects.filter(id=1).first()
        global_now = timezone.localtime(timezone.now())
        hour_choices = [
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            0,
            1,
        ]
        hour_weights = [3, 7, 7, 7, 6, 6, 3, 3, 3, 3, 3, 8, 7, 7, 6, 6, 3, 3, 3, 3, 3]
        if options.get("date"):
            _date = (
                datetime.datetime.strptime(options["date"], "%Y-%m-%d")
                .astimezone()
                .date()
            )
            global_now = global_now.replace(
                year=_date.year,
                month=_date.month,
                day=_date.day,
            )

        ticket_form_list = [TicketFormType.PAPER, TicketFormType.ETIX]
        if options["ticket_form"] and options["ticket_form"] in ticket_form_list:
            ticket_form_list = [options["ticket_form"]]

        if options["dynamodb"]:
            self.dynamodb = boto3.resource("dynamodb")
            print(self.dynamodb)
            self.ddbt_scan_event = self.dynamodb.Table(settings.DYNAMODB_TABLE_PPTICKET)
            self.ddbt_etix_event = self.dynamodb.Table(settings.DYNAMODB_TABLE_ETICKET)
            if options["truncate"]:
                logger.info("Truncating tables")
                self.truncate_dynamodb_table(self.ddbt_scan_event)
                self.truncate_dynamodb_table(self.ddbt_etix_event)

        for _x in range(options["count"]):
            # Select a random date between the global_now and
            # the days selected attribute
            if options["days"]:
                (dt_start, dt_end) = self.random_datetime(global_now, options["days"])

            else:
                dt_end = global_now
                dt_start = dt_end - datetime.timedelta(seconds=1)
            dt_delta = dt_end - dt_start
            dt_total_seconds = int(dt_delta.total_seconds())
            valid_from = dt_end - datetime.timedelta(
                milliseconds=randrange(dt_total_seconds * 1000),
            )
            valid_from = valid_from.replace(
                hour=choices(hour_choices, weights=hour_weights, k=1)[0]
            )
            valid_from = min(valid_from, global_now)
            valid_to = valid_from + datetime.timedelta(hours=24)

            company = Company.objects.filter(pk__in=[1, 2]).order_by("?").first()
            if company is None:
                continue
            sales_packet = (
                SalesPackets.objects.filter(packet_type=1, version=latest_version)
                .order_by("?")
                .first()
            )

            from_station = (
                TVMStation.objects.filter(company=company).order_by("?").first()
            )
            if from_station is None:
                continue
            to_station = (
                TVMStation.objects.filter(company=company)
                .exclude(pk=from_station.pk if from_station else 0)
                .order_by("?")
                .first()
            )
            if to_station is None:
                continue
            ticket_source = TicketSource.objects.order_by("?").first()
            device_class = (
                DeviceClass.objects.filter(
                    device_class_id__range=[company.pk * 100, (company.pk * 100) + 99]
                )
                .order_by("?")
                .first()
            )

            created_on = valid_from
            ticket_form = choice(ticket_form_list)
            ticket_number = PaperTicket.objects.encode_number(
                station=from_station.station_id,
                device_class=device_class.pk,
                company=company.pk,
                no=randrange(0, 99),
                issue_date=created_on.date(),
                trans_sec=str(int(valid_from.timestamp() * 1000))[-4:],
            )

            ticket_values = {
                "sales_packet": sales_packet,
                "form": ticket_form,
                "number": ticket_number,
                "amount": (randrange(10, 100) // 5) * 50,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "from_station": from_station,
                "to_station": to_station,
                "count": 1,
                "created_by": created_by,
                "created_on": created_on,
            }

            scan_values = {
                "tour_id": randrange(1000, 10000),
                "conductor_id": randrange(100000, 100400),
                "train_id": choice(_static["TRAINS"][str(company.pk)]),
                "scanned_on": created_on
                - datetime.timedelta(milliseconds=randrange(200, 1000)),
                "created_on": created_on,
                "company": company,
                "source": ticket_source,
            }

            etix_values = {
                "price": ticket_values["amount"],
                "e_ticket_no": "9"
                + hex(int(valid_from.strftime("%Y%m%d%H%M")))[2:].upper(),
                "discount_code": "",
                "product_id": randrange(4001, 5001),
                "activate_start": valid_from,
                "device_utc": created_on,
                "from_station": from_station,
                "to_station": to_station,
                "parent_product_id": "",
                "line": "",
                "abi": "com.masabi.ticketcheck.store.UAT",
                "act": ETixTicket.ActionCodes.OKAY,
                "tkt_oc": 0,
            }

            paper_ticket_values = {
                "sales_packet": sales_packet,
                "number": ticket_values["number"],
                "amount": ticket_values["amount"],
                "from_station": from_station,
                "to_station": to_station,
                "via_station": None,
                "from_return": None,
                "to_return": None,
                "via_return": None,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "count_passenger_category_1": ticket_values["count"],
                "start_connection_service": 0,
                "end_connection_service": 0,
            }

            if ticket_form == TicketFormType.ETIX:
                ticket_values["number"] = etix_values["e_ticket_no"]
                ticket_values["valid_to"] = etix_values[
                    "activate_start"
                ] + datetime.timedelta(hours=2)

            if options["dynamodb"]:
                self.write_to_dynamodb(
                    ticket_scan=scan_values,
                    ticket_form=ticket_form,
                    etix_values=etix_values,
                    paper_ticket_values=paper_ticket_values,
                )

            else:
                print(ticket_values)
                instance, _ = Ticket.objects.get_or_create(
                    number=ticket_values["number"],
                    defaults=ticket_values,
                )
                scan_values["ticket"] = instance
                etix_values["ticket"] = instance
                paper_ticket_values["ticket"] = instance
                if ticket_form == TicketFormType.ETIX:
                    ETixTicket.objects.get_or_create(
                        e_ticket_no=etix_values["e_ticket_no"],
                        defaults=etix_values,
                    )
                else:
                    PaperTicket.objects.get_or_create(
                        number=paper_ticket_values["number"],
                        defaults=paper_ticket_values,
                    )

                TicketScan.objects.create(**scan_values)

    def random_datetime(self, now, days):
        dt_now = now - datetime.timedelta(
            days=randrange(0, days),
        )
        dt_start = dt_now.replace(hour=5, minute=0, second=0, microsecond=0)
        dt_end = dt_start + datetime.timedelta(hours=20)

        return (dt_start, dt_end)

    def write_to_dynamodb(
        self,
        ticket_scan,
        ticket_form,
        etix_values,
        paper_ticket_values,
    ):
        if self.ddbt_scan_event is None and self.ddbt_etix_event:
            return
        scan_item = {
            "ticket-scan-timestamp": ticket_scan["scanned_on"].isoformat(),
            "conductorId": int(ticket_scan["conductor_id"]),
            "tourId": int(ticket_scan["tour_id"]),
            "trainId": int(ticket_scan["train_id"]),
            "createdAt": ticket_scan["created_on"].isoformat(),
        }
        scan_item_data = {
            "ticket-scan-timestamp": "DATA",
            "TicketBarCode": "FAKEDATA",
        }
        print("----", ticket_form, "----")
        if ticket_form == TicketFormType.ETIX:
            # TODO: Waiting on Chris Baca to complete the eTix table schema.
            scan_item["ticket-number"] = etix_values["e_ticket_no"]
            scan_item_data["ticket-number"] = etix_values["e_ticket_no"]
            _etix = self.etix_dict_to_representation(etix_values)

            scan_item_data["TicketDetail"] = _etix
            self.ddbt_etix_event.put_item(Item=scan_item)
            self.ddbt_etix_event.put_item(Item=scan_item_data)
        else:
            scan_item["ticket-number"] = paper_ticket_values["number"]
            scan_item_data["ticket-number"] = paper_ticket_values["number"]
            _paper_ticket = self.pptix_dict_to_representation(paper_ticket_values)
            print("-" * 100)
            print(_paper_ticket)

            scan_item_data["TicketDetail"] = _paper_ticket
            self.ddbt_scan_event.put_item(Item=scan_item)
            self.ddbt_scan_event.put_item(Item=scan_item_data)

    def pptix_dict_to_representation(self, data):
        _paper_ticket = data.copy()
        print(data)
        _paper_ticket.update(
            {
                "ticket_type": data["sales_packet"].packet_id,
                "ticket_number": data["number"],
                "from": data["from_station"].pk,
                "to": data["to_station"].pk,
                "via": data["via_station"].pk if data["via_station"] else None,
                "from_return": data["from_return"].pk if data["from_return"] else None,
                "to_return": data["to_return"].pk if data["to_return"] else None,
                "via_return": data["via_return"].pk if data["via_return"] else None,
                "valid_from": data["valid_from"].isoformat(),
                "valid_to": data["valid_to"].isoformat(),
                "ticket": None,
            },
        )
        del _paper_ticket["sales_packet"]
        del _paper_ticket["number"]
        del _paper_ticket["ticket"]
        del _paper_ticket["from_station"]
        del _paper_ticket["to_station"]
        del _paper_ticket["via_station"]
        return _paper_ticket

    def etix_dict_to_representation(self, data):
        return {
            "price": data["price"],
            "eTicketNo": data["e_ticket_no"],
            "discountCode": data["discount_code"],
            "productId": data["product_id"],
            "activateStart": data["activate_start"].isoformat(),
            "deviceUtc": data["device_utc"].isoformat(),
            "fromStation": data["from_station"].code,
            "toStation": data["to_station"].code,
            "parentProductId": data["parent_product_id"],
            "line": data["line"],
            "ABI": data["abi"],
            "Act": data["act"],
            "TktOC": data["tkt_oc"],
        }

    def truncate_dynamodb_table(self, dynamodb_table):
        response = dynamodb_table.scan()
        for item in response["Items"]:
            dynamodb_table.delete_item(
                Key={
                    "ticket-number": item["ticket-number"],
                    "ticket-scan-timestamp": item["ticket-scan-timestamp"],
                }
            )
