"""Django Command file to import different types of data from CSV"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pytz
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from tablib import Dataset

from core.general.models import ServiceProvider
from core.ticket.models import TicketType, Tour


class Command(BaseCommand):
    help = "Import all ticket legacy data"

    def add_arguments(self, parser):
        parser.add_argument("--source", "-s", default="legacy")
        parser.add_argument("--type", "-t", type=str)
        parser.add_argument("--file", "-f", type=str)

    def handle(self, *args, **options):
        _type = slugify(options["type"])
        _function_name = "parse_{}_{}".format(options["source"], _type)

        if hasattr(self, _function_name):
            getattr(self, _function_name)(Path(options["file"]))

    def parse_legacy_tickettype(self, file: Path):
        data = Dataset().load(file.open(encoding="utf-8", errors="ignore").read())

        import_id_fields = ("code",)
        col_map = {
            "VERSIONID": "version_id",
            "TICKETTYPEID": "code",
            "DESCRIPTION": "description",
            "SERVICEPROVIDERID": "service_provider_id",
        }
        _headers: list[str] = [str(x) for x in data.headers] if data.headers else []
        for _row in data:
            _row_data = {}
            _defaults = {
                "created_on": timezone.now(),
                "created_by_id": 1,
                "service_provider_id": 0,
            }
            for _header in enumerate(_headers):
                _row_data[_header[1]] = _row[_header[0]]
            for _map in col_map.items():
                if _map[0] in _row_data:
                    _defaults[_map[1]] = _row_data[_map[0]]
            if _defaults.get("service_provider_id"):
                _service_provider = ServiceProvider.objects.filter(
                    code=str(_defaults["service_provider_id"]),
                ).first()
                if _service_provider is not None:
                    _defaults["service_provider"] = _service_provider
                    _defaults["service_provider_id"] = _service_provider.pk
                else:
                    _defaults["service_provider_id"] = None

            _create_update_kwargs: dict[str, Any] = {}

            for _field in import_id_fields:
                _create_update_kwargs[_field] = _defaults[_field]
                del _defaults[_field]
            _create_update_kwargs["defaults"] = _defaults

            if _create_update_kwargs["code"]:
                TicketType.objects.update_or_create(**_create_update_kwargs)

    def parse_obtims_tour(self, file: Path):
        data = Dataset().load(file.open(encoding="utf-8", errors="ignore").read())
        import_id_fields = ("code",)
        col_map = {
            "TOUR_ID": "code",
            "\ufeffTOUR_ID": "code",
            "TOUR_BEGIN_DATE": "begin_date",
            "CONDUCTOR_ID": "conductor_id",
            "TRAIN_NO": "train_no",
        }

        _headers: list[str] = (
            [str(x.strip()) for x in data.headers] if data.headers else []
        )
        for _row in data:
            _row_data = {}
            _defaults = {}
            for _header in enumerate(_headers):
                _row_data[_header[1]] = _row[_header[0]]

            for _map in col_map.items():
                if _map[0] in _row_data:
                    _defaults[_map[1]] = _row_data[_map[0]]

            _create_update_kwargs = {}
            for _field in import_id_fields:
                _create_update_kwargs[_field] = _defaults[_field]
                del _defaults[_field]
            _create_update_kwargs["defaults"] = _defaults

            _create_update_kwargs["code"] = _create_update_kwargs["code"].replace(
                ",",
                "",
            )
            if _create_update_kwargs["code"]:
                if re.match(
                    r"^\d{2}\/\d{2}\/20\d{2}\s+([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
                    _create_update_kwargs["defaults"]["begin_date"],
                ):
                    _create_update_kwargs["defaults"]["begin_date"] = datetime.strptime(
                        _create_update_kwargs["defaults"]["begin_date"],
                        "%m/%d/%Y %H:%M:%S",
                    ).replace(
                        tzinfo=pytz.UTC,
                    )
                Tour.objects.update_or_create(**_create_update_kwargs)
