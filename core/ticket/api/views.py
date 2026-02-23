import logging
from datetime import datetime, time, timedelta
from decimal import Decimal
from typing import Any

from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.db.models import (
    Avg,
    Count,
    F,
    Q,
)
from django.db.models.functions import Round, Trunc
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.ticket.api.serializers import TicketScanSerializer
from core.ticket.model_types import TicketFormType

logger = logging.getLogger(__name__)

MNR_ID = 1
LIRR_ID = 2


class TicketScanViewSet(ReadOnlyModelViewSet):
    serializer_class = TicketScanSerializer

    def get_queryset(self) -> QuerySet:
        filters = {}
        conductor_id = self.request.GET.get("conductor_id", None)
        train_id = self.request.GET.get("train_id", None)
        tour_id = self.request.GET.get("tour_id", None)
        start_date_str = self.request.GET.get("start_date", None)
        end_date_str = self.request.GET.get("end_date", None)
        if conductor_id:
            filters["conductor_id"] = conductor_id
        if train_id:
            filters["train_id"] = train_id
        if tour_id:
            filters["tour_id"] = tour_id
        _current_timezone = timezone.get_current_timezone()
        if start_date_str:
            _sd = parse_date(start_date_str)
            if _sd:
                filters["scanned_on__gte"] = datetime.combine(
                    _sd,
                    time.min,
                    tzinfo=_current_timezone,
                )  # type: ignore[assignment]
        if end_date_str:
            _ed = parse_date(end_date_str)
            if _ed:
                filters["scanned_on__lte"] = datetime.combine(
                    _ed,
                    time.max,
                    tzinfo=_current_timezone,
                )  # type: ignore[assignment]
        TicketScan = apps.get_model("ticket", "TicketScan")
        return TicketScan.objects.filter(**filters)

    @action(detail=False, methods=["get"], url_path="dashboard/card_agency_line")
    def card_agency_line(self, request, *args, **kwargs):  # noqa: C901
        TicketScan = apps.get_model("ticket", "TicketScan")
        end_date = timezone.now()
        start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if request.query_params.get("start_date"):
            _sd = parse_date(request.query_params["start_date"])
            if _sd:
                start_date = datetime.combine(
                    _sd,
                    time.min,
                    tzinfo=timezone.get_current_timezone(),
                )
        if request.query_params.get("end_date"):
            _ed = parse_date(request.query_params["end_date"])
            if _ed:
                end_date = datetime.combine(
                    _ed,
                    time.max,
                    tzinfo=timezone.get_current_timezone(),
                )
        labels = []
        items = (
            TicketScan.objects.filter(
                scanned_on__range=[start_date, end_date],
            )
            .values("company_id", "company__name")
            .annotate(
                scanned_on=Trunc("scanned_on", "day"),
                total=Count("id"),
            )
            .order_by("scanned_on")
        )
        series: dict[str, dict] = {}
        for item in items.iterator():
            if item["company_id"] not in series:
                series[item["company_id"]] = {
                    "name": item["company__name"]
                    if len(item["company__name"]) > 0
                    else "N/A",
                    "data": [],
                }
            agency_series = series[item["company_id"]]
            agency_series["data"].append(item["total"])
            scanned_on = item["scanned_on"].strftime("%Y-%m-%d")
            if scanned_on not in labels:
                labels.append(scanned_on)

        this_month_total = TicketScan.objects.filter(
            scanned_on__range=[start_date, end_date],
        ).aggregate(
            total=Count("id"),
        )

        last_start_date = start_date - relativedelta(months=1)
        last_end_date = end_date - relativedelta(months=1)

        last_month_total = TicketScan.objects.filter(
            scanned_on__range=[last_start_date, last_end_date],
        ).aggregate(
            total=Count("id"),
        )
        rtn = {
            "this_month": Decimal("0"),
            "last_month": Decimal("0"),
            "diff": Decimal("0"),
            "diff_percent": Decimal("0"),
            "chart": {
                "labels": labels,
                "series": list(series.values()),
            },
            "this": {
                "start": start_date,
                "end": end_date,
            },
            "last": {
                "start": last_start_date,
                "end": last_end_date,
            },
        }
        if last_month_total["total"]:
            rtn["last_month"] = Decimal(str(last_month_total["total"]))
        if this_month_total["total"]:
            rtn["this_month"] = Decimal(str(this_month_total["total"]))

        rtn["diff"] = Decimal(str(rtn["this_month"])) - Decimal(str(rtn["last_month"]))
        if rtn["diff"] and rtn["this_month"]:
            rtn["diff_percent"] = Decimal(
                round(
                    (Decimal(str(rtn["diff"])) / Decimal(str(rtn["this_month"])))
                    * 10000,
                )
                / 100,
            )

        return Response(rtn)

    @action(detail=False, methods=["get"], url_path="dashboard/card_agency_heatmap")
    def card_agency_heatmap(self, request, *args, **kwargs):
        TicketScan = apps.get_model("ticket", "TicketScan")

        end_date = timezone.now()
        start_date = end_date - timedelta(days=15)
        if request.query_params.get("start_date"):
            _sd = parse_date(request.query_params["start_date"])
            if _sd:
                start_date = datetime.combine(
                    _sd,
                    time.min,
                    tzinfo=timezone.get_current_timezone(),
                )
        if request.query_params.get("end_date"):
            _ed = parse_date(request.query_params["end_date"])
            if _ed:
                end_date = datetime.combine(
                    _ed,
                    time.max,
                    tzinfo=timezone.get_current_timezone(),
                )

        items = (
            TicketScan.objects.filter(
                scanned_on__range=[start_date, end_date],
            )
            .values(
                date_hr=Trunc(
                    "scanned_on",
                    "hour",
                    tzinfo=timezone.get_current_timezone(),
                ),
            )
            .annotate(
                total_sum=Count("id"),
                mnr_total=Count("id", filter=Q(company_id=1)),
                lirr_total=Count("id", filter=Q(company_id=2)),
            )
            .order_by("date_hr")
        )
        series = {}

        for item in items.iterator():
            series_key = item["date_hr"].strftime("%b-%d")
            if series_key not in series:
                series[series_key] = {
                    "name": series_key,
                    "data": [],
                    "color": "#2fb344"
                    if item["date_hr"].weekday() in (5, 6)
                    else "#4299e1",
                }

            series_item = series[series_key]
            _label = item["date_hr"].strftime("%H")
            series_item["data"].append(
                {
                    "y": item["total_sum"],
                    "mnr": item["mnr_total"],
                    "lirr": item["lirr_total"],
                    "x": _label,
                },
            )

        full_labels = [f"{x:02d}" for x in range(24)]
        for _key in series.items():
            _labels = [_d["x"] for _d in _key[1]["data"] if _d["x"]]
            _diff_labels = list(set(full_labels) - set(_labels))
            logger.info(_diff_labels)
            for _missing_label in _diff_labels:
                _key[1]["data"].append(
                    {
                        "y": 0,
                        "mnr": 0,
                        "lirr": 0,
                        "x": _missing_label,
                    },
                )
            _key[1]["data"] = sorted(_key[1]["data"], key=lambda x: x["x"])

        rtn = {
            "chart": {
                "labels": full_labels,
                "series": [series[x] for x in sorted(series.keys(), reverse=True)],
            },
            "start_date": start_date,
            "end_date": end_date,
        }
        return Response(rtn)

    @action(detail=False, methods=["get"], url_path="dashboard/card_type_pie")
    def card_type_pie(self, request, *args, **kwargs):  # noqa: C901
        TicketScan = apps.get_model("ticket", "TicketScan")

        end_date = timezone.now()
        company_id = request.query_params.get("agency_id", None)
        is_live = bool(request.query_params.get("live", None))

        if request.query_params.get("end_date"):
            _ed = parse_date(request.query_params["end_date"])
            if _ed:
                if is_live:
                    end_date = datetime.combine(_ed, end_date.time(), end_date.tzinfo)
                else:
                    end_date = datetime.combine(
                        _ed,
                        time.max,
                        timezone.get_current_timezone(),
                    )

        start_date = end_date - timedelta(days=1)
        if request.query_params.get("start_date"):
            _ed = parse_date(request.query_params["start_date"])
            if _ed:
                if is_live:
                    start_date = datetime.combine(
                        _ed,
                        start_date.time(),
                        start_date.tzinfo,
                    )
                else:
                    start_date = datetime.combine(
                        _ed,
                        time.min,
                        timezone.get_current_timezone(),
                    )
        filters = {"scanned_on__range": [start_date, end_date]}
        colors = [
            "#74b81699",
            "#4299e199",
            "#4263eb99",
            "#ae3ec999",
            "#d6336c99",
            "#d6393999",
            "#f7670799",
            "#17a2b899",
        ]
        if company_id:
            filters["ticket__scans__company_id"] = company_id
            if company_id == "1":
                colors = [
                    "#0039A6ff",
                    "#009B3Aff",
                    "#EE0034ff",
                    "#8E258Dff",
                    "#FF7900ff",
                    "#d63939ff",
                    "#0039A677",
                    "#009B3A77",
                ]
            elif company_id == "2":
                colors = [
                    "#00985fff",
                    "#4d5357ff",
                    "#6e3219ff",
                    "#ce8e00ff",
                    "#ff6319ff",
                    "#006983ff",
                    "#00a1deff",
                    "#a626aaff",
                ]

        labels = []

        items = (
            TicketScan.objects.filter(
                **filters,
            )
            .values(
                sales_packet_id=F("ticket__sales_packet__packet_id"),
                sales_packet_description=F("ticket__sales_packet__description"),
            )
            .annotate(
                total=Count("id"),
            )
            .order_by("-total", "sales_packet_description")[:8]
        )
        series = []
        for item in items.iterator():
            series.append(item["total"])
            labels.append(item["sales_packet_description"])
        rtn = {
            "chart": {
                "labels": labels,
                "series": series,
                "colors": colors,
            },
            "start_date": start_date,
            "end_date": end_date,
        }
        return Response(rtn)

    @action(detail=False, methods=["get"], url_path="dashboard/card_conductor_table")
    def card_conductor_table(self, request, *args, **kwargs):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=15)
        limit = int(request.query_params.get("limit", 15))
        if request.query_params.get("start_date"):
            _sd = parse_date(request.query_params["start_date"])
            if _sd:
                start_date = datetime.combine(
                    _sd,
                    time.min,
                    tzinfo=timezone.get_current_timezone(),
                )
        if request.query_params.get("end_date"):
            _ed = parse_date(request.query_params["end_date"])
            if _ed:
                end_date = datetime.combine(
                    _ed,
                    time.max,
                    tzinfo=timezone.get_current_timezone(),
                )
        company_id = int(request.query_params.get("agency_id", "0"))

        TicketScan = apps.get_model("ticket", "TicketScan")
        items = (
            TicketScan.objects.filter(
                scanned_on__range=[start_date, end_date],
                company_id=company_id,
            )
            .values(
                "conductor_id",
            )
            .annotate(
                total=Count("id"),
            )
            .order_by("-total")[:limit]
        )
        rtn = {
            "items": items,
            "start_date": start_date,
            "end_date": end_date,
        }

        return Response(rtn)

    @action(detail=False, methods=["get"], url_path="dashboard/card_train_table")
    def card_train_table(self, request, *args, **kwargs):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=15)
        limit = int(request.query_params.get("limit", 15))
        if request.query_params.get("start_date"):
            _sd = parse_date(request.query_params["start_date"])
            if _sd:
                start_date = datetime.combine(
                    _sd,
                    time.min,
                    tzinfo=timezone.get_current_timezone(),
                )
        if request.query_params.get("end_date"):
            _ed = parse_date(request.query_params["end_date"])
            if _ed:
                end_date = datetime.combine(
                    _ed,
                    time.max,
                    tzinfo=timezone.get_current_timezone(),
                )

        company_id = int(request.query_params.get("agency_id", "0"))

        TicketScan = apps.get_model("ticket", "TicketScan")
        items = (
            TicketScan.objects.filter(
                scanned_on__range=[start_date, end_date],
                company_id=company_id,
            )
            .values(
                "train_id",
            )
            .annotate(
                total=Count("id"),
            )
            .order_by("-total")[:limit]
        )

        rtn = {
            "items": items,
            "start_date": start_date,
            "end_date": end_date,
        }

        return Response(rtn)

    @action(detail=False, methods=["get"], url_path="dashboard/card_scan_table")
    def card_scan_table(self, request, *args, **kwargs):
        TicketScan = apps.get_model("ticket", "TicketScan")

        end_date = timezone.now()
        start_date = end_date - timedelta(hours=12)
        try:
            TicketScan.objects.sync_with_dynamodb_pptix(start_date, end_date)
            TicketScan.objects.sync_with_dynamodb_etix(start_date, end_date)
        except Exception:
            logger.exception("Dynaodb Sync Error")

        items = (
            TicketScan.objects.all()
            .values(
                "id",
                "tour_id",
                "conductor_id",
                "train_id",
                "scanned_on",
                "ticket__number",
                "company__short_name",
                "ticket__form",
                "ticket__amount",
                "ticket__sales_packet__description",
            )
            .order_by("-scanned_on")[:15]
        )
        for item in items:
            form = TicketFormType(item["ticket__form"])
            item["ticket__form"] = form.label

        return Response(items)

    @action(detail=False, methods=["get"], url_path="dashboard/card_time_response_line")
    def card_time_response_line(self, request, *args, **kwargs):
        TicketScan = apps.get_model("ticket", "TicketScan")

        end_date = timezone.now()
        start_date = end_date - timedelta(days=15)
        if request.query_params.get("start_date"):
            _sd = parse_date(request.query_params["start_date"])
            if _sd:
                start_date = datetime.combine(
                    _sd,
                    time.min,
                    tzinfo=timezone.get_current_timezone(),
                )
        if request.query_params.get("end_date"):
            _ed = parse_date(request.query_params["end_date"])
            if _ed:
                end_date = datetime.combine(
                    _ed,
                    time.max,
                    tzinfo=timezone.get_current_timezone(),
                )

        company_id = int(request.query_params.get("agency_id", "0"))

        items = (
            TicketScan.objects.filter(
                scanned_on__range=[start_date, end_date],
                company_id=company_id,
            )
            .annotate(
                date=Trunc(
                    "time_new",
                    "second",
                    tzinfo=timezone.get_current_timezone(),
                ),
            )
            .values(
                "date",
            )
            .annotate(
                seconds=Avg("scan_sync_time"),
                count=Count("id"),
            )
            .order_by("date", "seconds")
        )

        _data: list[dict[str, Any]] = []
        for _item in items:
            _new_item = {
                "x": _item["date"],
                "y": _item["seconds"],
                "count": _item["count"],
            }
            _data.append(_new_item)
        rtn = {
            "chart": {
                "series": [{"name": "Processing Time", "data": _data}],
            },
        }
        return Response(rtn)

    @action(detail=False, methods=["get"], url_path="dashboard/card_time_response_pie")
    def card_time_response_pie(self, request, *args, **kwargs):
        TicketScan = apps.get_model("ticket", "TicketScan")

        end_date = timezone.now()
        start_date = end_date - timedelta(days=15)
        if request.query_params.get("start_date"):
            _sd = parse_date(request.query_params["start_date"])
            if _sd:
                start_date = datetime.combine(
                    _sd,
                    time.min,
                    tzinfo=timezone.get_current_timezone(),
                )
        if request.query_params.get("end_date"):
            _ed = parse_date(request.query_params["end_date"])
            if _ed:
                end_date = datetime.combine(
                    _ed,
                    time.max,
                    tzinfo=timezone.get_current_timezone(),
                )

        company_id = int(request.query_params.get("agency_id", "0"))
        colors = []
        if company_id == MNR_ID:
            colors = [
                "#0039A6ff",
                "#009B3Aff",
                "#EE0034ff",
                "#8E258Dff",
                "#FF7900ff",
                "#d63939ff",
                "#0039A677",
                "#009B3A77",
            ]
        elif company_id == LIRR_ID:
            colors = [
                "#00985fff",
                "#4d5357ff",
                "#6e3219ff",
                "#ce8e00ff",
                "#ff6319ff",
                "#006983ff",
                "#00a1deff",
                "#a626aaff",
            ]

        items = (
            TicketScan.objects.filter(
                scanned_on__range=[start_date, end_date],
                company_id=company_id,
                scan_sync_time__gte=500,
            )
            .annotate(
                seconds=Round(F("scan_sync_time") / 100) * 100,
            )
            .values(
                "seconds",
            )
            .annotate(
                count=Count("id"),
            )
            .order_by("seconds")
        )

        rtn = {
            "chart": {
                "series": [item["count"] for item in items],
                "labels": [item["seconds"] for item in items],
                "colors": colors,
            },
            "start_date": start_date,
            "end_date": end_date,
        }

        return Response(rtn)
