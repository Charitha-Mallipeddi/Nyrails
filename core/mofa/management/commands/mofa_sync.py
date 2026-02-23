import logging
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.general import models as general_models
from core.mofa import models as mofa_models
from core.tariff import models as tariff_models
from core.users.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sync all lookup tables from mofa into CORE"

    def handle(self, *args, **kwargs):
        self.current_tzinfo = timezone.get_current_timezone()
        (self.user, _) = User.objects.get_or_create(
            username="farego",
            defaults={
                "email": "farego-core@mtahq.org",
                "is_active": True,
                "is_staff": False,
                "name": "FareGo MOFA",
            },
        )
        self.sync_company()
        self.sync_tariffversions()
        self.sync_routes()
        self.sync_device_class()
        self.sync_tvm_station()
        self.sync_by_versions()

    def _fix_timezeon(self, date_time: datetime | None = None):
        if date_time:
            date_time = date_time.replace(tzinfo=self.current_tzinfo)
        return date_time

    def sync_by_versions(self):
        versions = general_models.TariffVersions.objects.values("version_id").order_by(
            "-version_id"
        )
        for version in versions.iterator():
            logger.info("Version %s", version)
            logger.info("-" * 100)
            self.sync_zone_station(version_id=version["version_id"])
            self.sync_ticket_type(version_id=version["version_id"])
            self.sync_sales_packets(version_id=version["version_id"])
            self.sync_device_class_group(version_id=version["version_id"])
            self.sync_sales_packets_group(version_id=version["version_id"])
            self.sync_sales_station_group(version_id=version["version_id"])
            self.sync_ticket_type_group(version_id=version["version_id"])
            self.sync_time_lock(version_id=version["version_id"])
            self.sync_time_lock_group(version_id=version["version_id"])
            self.sync_validity(version_id=version["version_id"])

    def sync_company(self):
        items = mofa_models.Company.objects.values(
            "companyid", "name", "shortname", "timechange", "timenew"
        )
        totals = {"created": 0, "updated": 0, "total": items.count()}

        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])

            (_, _created) = general_models.Company.objects.update_or_create(
                company_id=item["companyid"],
                defaults={
                    "name": item["name"],
                    "short_name": item["shortname"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("Company: %s", totals)

    def sync_device_class(self):
        items = mofa_models.DeviceClass.objects.values()
        totals = {"created": 0, "updated": 0, "total": items.count()}

        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])

            (_, _created) = general_models.DeviceClass.objects.update_or_create(
                device_class_id=item["deviceclassid"],
                defaults={
                    "description": item["description"],
                    "device_class_type": item["deviceclasstype"],
                    "parameter_group_id": item["parametergroupid"],
                    "test_flag": item["testflag"],
                    "time_change": item["timechange"],
                    "tvm_apl_tar_version_group_id": item["tvmapltarversiongroupid"],
                    "tvm_sw_version_group_id": item["tvmswversiongroupid"],
                    "tvm_tech_version_group_id": item["tvmtechversiongroupid"],
                    "type_of_tariff_download_data": item["typeoftariffdownloaddata"],
                    "user_new": self.user,
                    "time_new": item["timenew"],
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("DeviceClass: %s", totals)

    def sync_tvm_station(self):
        items = mofa_models.TVMStation.objects.values()
        totals = {"created": 0, "updated": 0, "total": items.count()}

        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])

            (_, _created) = general_models.TVMStation.objects.update_or_create(
                station_id=item["stationid"],
                defaults={
                    "company_id": item["company_id"],
                    "graphic_key": item["graphickey"],
                    "name": item["name"],
                    "name_long": item["namelong"],
                    "name_short": item["nameshort"],
                    "station_type": item["stationtype"],
                    "tariff_property": item["tariffproperty"],
                    "tariff_zone": item["tariffzone"],
                    "town": item["town"],
                    "user_new": self.user,
                    "time_new": item["timenew"],
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("TVMStation: %s", totals)

    def sync_routes(self):
        items = mofa_models.Routes.objects.values(
            "routeid", "description", "timechange", "timenew"
        )
        totals = {"created": 0, "updated": 0, "total": items.count()}

        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])

            (_, _created) = general_models.Routes.objects.update_or_create(
                route_id=item["routeid"],
                defaults={
                    "description": item["description"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("Routes: %s", totals)

    def sync_tariffversions(self):
        items = mofa_models.TariffVersions.objects.values(
            "versionid",
            "type",
            "rail_road_id",
            "description",
            "status",
            "theovertakerflag",
            "timechange",
            "timenew",
            "validitystarttime",
            "validityendtime",
        )
        totals = {"created": 0, "updated": 0, "total": items.count()}

        for item in items.iterator():
            for _field in (
                "timechange",
                "timenew",
                "validitystarttime",
                "validityendtime",
            ):
                item[_field] = self._fix_timezeon(item[_field])

            (_, _created) = general_models.TariffVersions.objects.update_or_create(
                version_id=item["versionid"],
                defaults={
                    "description": item["description"],
                    "type": item["type"],
                    "status": item["status"],
                    "the_overtaker_flag": item["theovertakerflag"],
                    "validity_start_time": item["validitystarttime"],
                    "validity_end_time": item["validityendtime"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "rail_road_id": item["rail_road_id"],
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("TariffVersions: %s", totals)

    def sync_zone_station(self, version_id: int):
        items = mofa_models.ZoneStation.objects.values(
            "zonestationid",
            "type",
            "version_id",
            "description",
            "zoneid",
            "typezone",
            "timechange",
            "timenew",
        ).filter(version_id=version_id)
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = general_models.ZoneStation.objects.update_or_create(
                zone_station_id=item["zonestationid"],
                type=item["type"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "zoneid": item["zoneid"],
                    "typezone": item["typezone"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("ZoneStation: %s", totals)

    def sync_ticket_type(self, version_id: int):
        items = mofa_models.TicketType.objects.values(
            "tickettypeid",
            "version_id",
            "description",
            "serviceproviderid",
            "timechange",
            "timenew",
            "validityid",
        ).filter(version_id=version_id)
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = tariff_models.TicketType.objects.update_or_create(
                ticket_type_id=item["tickettypeid"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "company_id": item["serviceproviderid"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                    "validity_id": item["validityid"],
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("TicketType: %s", totals)

    def sync_device_class_group(self, version_id: int):
        items = mofa_models.DeviceClassGroup.objects.values().filter(
            version_id=version_id
        )
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = general_models.DeviceClassGroup.objects.update_or_create(
                device_class_group_id=item["deviceclassgroupid"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("DeviceClassGroup: %s", totals)

    def sync_sales_packets(self, version_id: int):
        items = mofa_models.SalesPackets.objects.values().filter(version_id=version_id)
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = tariff_models.SalesPackets.objects.update_or_create(
                packet_id=item["packetid"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "dest_station_group_id": item["deststationgroupid"],
                    "device_class_group_id": item["deviceclassgroupid"],
                    "external_id": item["externalid"],
                    "group_fare_id": item["groupfareid"],
                    "multimedia_group_id": item["multimediagroupid"],
                    "packet_type": item["packettype"],
                    "pay_accept_group_id": item["payacceptgroupid"],
                    "plus_group_id": item["plusgroupid"],
                    "sales_station_group_id": item["salesstationgroupid"],
                    "send_on_levt": item["sendonlevt"],
                    "start_station_group_id": item["startstationgroupid"],
                    "time_lock_group_id": item["timelockgroupid"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("SalesPackets: %s", totals)

    def sync_sales_packets_group(self, version_id: int):
        items = mofa_models.SalesPacketsGroup.objects.values().filter(
            version_id=version_id
        )
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = tariff_models.SalesPacketsGroup.objects.update_or_create(
                packet_group_id=item["packetgroupid"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "multimedia_group_id": item["multimediagroupid"],
                    "packet_group_type": item["packetgrouptype"],
                    "sort_order": item["sortorder"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("SalesPacketsGroup: %s", totals)

    def sync_sales_station_group(self, version_id: int):
        items = mofa_models.StationGroup.objects.values().filter(version_id=version_id)
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = general_models.StationGroup.objects.update_or_create(
                station_group_id=item["stationgroupid"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "group_type": item["grouptype"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("StationGroup: %s", totals)

    def sync_ticket_type_group(self, version_id: int):
        items = mofa_models.TicketTypeGroup.objects.values().filter(
            version_id=version_id
        )
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = tariff_models.TicketTypeGroup.objects.update_or_create(
                ticket_type_group_id=item["tickettypegroupid"],
                ticket_type_group_type=item["tickettypegrouptype"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "abbreviation": item["abbreviation"],
                    "multimedia_group_id": item["multimediagroupid"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("TicketTypeGroup: %s", totals)

    def sync_time_lock(self, version_id: int):
        items = mofa_models.TimeLock.objects.values().filter(version_id=version_id)
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = general_models.TimeLock.objects.update_or_create(
                time_lock_id=item["timelockid"],
                device_class_group_id=item["deviceclassgroupid"],
                version_id=item["version_id"],
                defaults={
                    "pre_sale_entry": item["presaleentry"],
                    "lock_flag": item["lockflag"],
                    "holiday_lock": item["holidaylock"],
                    "days_of_week": item["daysofweek"],
                    "days_of_month": item["daysofmonth"],
                    "valid_from": item["validfrom"],
                    "valid_to": item["validto"],
                    "priority": item["priority"],
                    "description": item["description"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("TicketTypeGroup: %s", totals)

    def sync_time_lock_group(self, version_id: int):
        items = mofa_models.TimeLockGroup.objects.values().filter(version_id=version_id)
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = general_models.TimeLockGroup.objects.update_or_create(
                time_lock_group_id=item["timelockgroupid"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "lock_flag": item["lockflag"],
                    "multimedia_group_id": item["multimediagroupid"],
                    "time_lock": item["timelock"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("TimeLockGroup: %s", totals)

    def sync_validity(self, version_id: int):
        items = mofa_models.Validity.objects.values().filter(version_id=version_id)
        totals = {"created": 0, "updated": 0, "total": items.count()}
        for item in items.iterator():
            for _field in ("timechange", "timenew"):
                item[_field] = self._fix_timezeon(item[_field])
            (_, _created) = general_models.Validity.objects.update_or_create(
                validity_id=item["validityid"],
                version_id=item["version_id"],
                defaults={
                    "description": item["description"],
                    "duration_type": item["durationtype"],
                    "duration_value": item["durationvalue"],
                    "end_def": item["enddef"],
                    "end_rel_dayofmonth_next": item["endreldayofmonthnext"],
                    "end_rel_dayofmonth_used": item["endreldayofmonthused"],
                    "end_rel_dayofmonth_value": item["endreldayofmonthvalue"],
                    "end_rel_dayofweek_next": item["endreldayofweeknext"],
                    "end_rel_dayofweek_used": item["endreldayofweekused"],
                    "end_rel_dayofweek_value": item["endreldayofweekvalue"],
                    "end_rel_hour_next": item["endrelhournext"],
                    "end_rel_hour_used": item["endrelhourused"],
                    "end_rel_hour_value": item["endrelhourvalue"],
                    "end_rel_minute_next": item["endrelminutenext"],
                    "end_rel_minute_used": item["endrelminuteused"],
                    "end_rel_minute_value": item["endrelminutevalue"],
                    "end_rel_month_next": item["endrelmonthnext"],
                    "end_rel_month_used": item["endrelmonthused"],
                    "end_rel_month_value": item["endrelmonthvalue"],
                    "end_rel_week_next": item["endrelweeknext"],
                    "end_rel_week_used": item["endrelweekused"],
                    "end_rel_week_value": item["endrelweekvalue"],
                    "multimedia_group_id": item["multimediagroupid"],
                    "start_def": item["startdef"],
                    "start_rel_dayofmonth_next": item["startreldayofmonthnext"],
                    "start_rel_dayofmonth_used": item["startreldayofmonthused"],
                    "start_rel_dayofmonth_value": item["startreldayofmonthvalue"],
                    "start_rel_dayofweek_next": item["startreldayofweeknext"],
                    "start_rel_dayofweek_used": item["startreldayofweekused"],
                    "start_rel_dayofweek_value": item["startreldayofweekvalue"],
                    "start_rel_hour_next": item["startrelhournext"],
                    "start_rel_hour_used": item["startrelhourused"],
                    "start_rel_hour_value": item["startrelhourvalue"],
                    "start_rel_minute_next": item["startrelminutenext"],
                    "start_rel_minute_used": item["startrelminuteused"],
                    "start_rel_minute_value": item["startrelminutevalue"],
                    "start_rel_month_next": item["startrelmonthnext"],
                    "start_rel_month_used": item["startrelmonthused"],
                    "start_rel_month_value": item["startrelmonthvalue"],
                    "start_rel_week_next": item["startrelweeknext"],
                    "start_rel_week_used": item["startrelweekused"],
                    "start_rel_week_value": item["startrelweekvalue"],
                    "validity_type": item["validitytype"],
                    "time_change": item["timechange"],
                    "time_new": item["timenew"],
                    "user_new": self.user,
                },
            )
            if _created:
                totals["created"] += 1
            else:
                totals["updated"] += 1
        logger.info("Validity: %s", totals)
