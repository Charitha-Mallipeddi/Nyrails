from django.db import models

from core.contrib.db.constraints import ForeignReferencesConstraint

from .model_types import ZoneStationType


class BaseAuditModel(models.Model):
    """Audit class for storing the common created,updated information"""

    time_new = models.DateTimeField(
        db_column="timenew", blank=True, null=True, auto_now_add=True
    )
    time_change = models.DateTimeField(
        db_column="timechange", blank=True, null=True, auto_now=True
    )
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_changed",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
    )

    class Meta:
        abstract = True


class BaseValidModel(models.Model):
    valid = models.BooleanField(default=True, verbose_name="Is Valid?")

    class Meta:
        abstract = True


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True, db_column="companyid")
    name = models.CharField(max_length=50)
    short_name = models.CharField(db_column="shortname", max_length=8, unique=True)
    time_change = models.DateTimeField(
        db_column="timechange", null=True, blank=True, auto_now=True
    )
    time_new = models.DateTimeField(db_column="timenew", null=True, blank=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "company"

    def __str__(self):
        return f"{self.name}[{self.company_id}]"


class Routes(models.Model):
    """
    This table describes a Line or a Branch. With the 'StationRouteElements' table one
    or more stations can be linked to one or more routes.
    """

    route_id = models.IntegerField(
        db_column="routeid", primary_key=True, help_text="Unique ID of Route"
    )
    description = models.CharField(max_length=128, help_text="Describes the route")
    class_name = models.CharField(
        db_column="classname", max_length=128, blank=True, default=""
    )
    time_change = models.DateTimeField(
        db_column="timechange", null=True, blank=True, auto_now=True
    )
    time_new = models.DateTimeField(db_column="timenew", null=True, blank=True)

    class Meta:
        db_table = "routes"
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def __str__(self):
        return f"{self.description}[{self.route_id}]"


class TariffVersions(models.Model):
    """
    Here you can set a start and end date-time for the validity of the tariff version.
    On CSS level the status flag indicates if tariff version is still in a working
    process or if it is finished (downloaded to the TSMs).
    The version number increments automatically.
    """

    class STATUSES(models.IntegerChoices):
        NEW_EDIT = (0, "new/edit")
        DONE_MDB = (1, "finalized (downloaded / ready for download) mdb file")
        DONE_TBL = (2, "finalized (downloaded / ready for download) tbl file")
        DONE_BOTH = (3, "both 1 and 2 (handheld devices)")

    class TYPES(models.IntegerChoices):
        NULL = (0, "Tariff data")
        ADDITIONAL = (1, "Additional tariff data")
        __empty__ = "Tariff data"

    version_id = models.IntegerField(
        primary_key=True, db_column="versionid", help_text="ID of tariff version"
    )
    type = models.SmallIntegerField(
        db_column="type",
        null=True,
        help_text="Type of station profiling",
        choices=TYPES,
    )

    description = models.CharField(
        db_column="description",
        max_length=50,
        blank=True,
        help_text="Tariff description",
    )
    rail_road = models.ForeignKey(
        Company,
        db_column="railroadid",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Company specific tariff parameter",
    )
    status = models.SmallIntegerField(
        null=True, blank=True, help_text="State of this version", choices=STATUSES
    )
    the_overtaker_flag = models.BooleanField(
        db_column="theovertakerflag",
        default=False,
        help_text="Is tariff version overtaken to "
        "version administration (table VERSIONS)",
    )

    time_new = models.DateTimeField(db_column="timenew", auto_created=True)
    time_change = models.DateTimeField(db_column="timechange", auto_now=True, null=True)

    validity_start_time = models.DateTimeField(
        db_column="validitystarttime", help_text="Start time/date of Validity"
    )
    validity_end_time = models.DateTimeField(
        db_column="validityendtime", help_text="End time/date of Validity"
    )

    class Meta:
        db_table = "tariffversions"
        verbose_name = "Tariff Version"
        verbose_name_plural = "Tariff Versions"

    def __str__(self):
        return "{} [{}]".format(
            self.description,
            self.validity_start_time.strftime("%Y-%m-%d %H:%M:%S"),
        )


class ZoneStation(models.Model):
    """
    This table holds all the Tariff Stations and the Zone information.
    A station is linked to a Zone (which is also defined in this table)
    by the field ZoneID and TypeZone.

    There might be different ID's for the zone calculation
    and the zone that is printed on the ticket. This print information
    is a station dependent text (comes with MultimediaGroup).
    It also holds connections (connection services). They are interpreted
    like stations outside of the system (not selectable by start or destination input).

    To distinguish between this different information's the 'Type' field is used.
    """

    pk = models.CompositePrimaryKey("version", "zone_station_id", "type")
    version = models.ForeignKey(
        "TariffVersions",
        models.CASCADE,
        db_column="versionid",
        related_name="zone_stations",
    )
    zone_station_id = models.IntegerField(db_column="zonestationid")
    type = models.IntegerField(choices=ZoneStationType, default=ZoneStationType.STATION)
    description = models.CharField(max_length=50, blank=True)
    zone_id = models.IntegerField(blank=True, null=True, db_column="zoneid")
    type_zone = models.IntegerField(
        blank=True, null=True, db_column="typezone", choices=ZoneStationType
    )
    zone = models.ForeignObject(
        "self",
        models.SET_NULL,
        from_fields=("version", "zone_id", "type_zone"),
        to_fields=("version", "zone_station_id", "type"),
        blank=True,
        null=True,
        serialize=False,
        related_name="children",
    )
    time_new = models.DateTimeField(db_column="timenew", auto_created=True)
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        on_delete=models.PROTECT,
        related_name="zone_station_user_new",
    )
    time_change = models.DateTimeField(db_column="timechange", auto_now=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="zone_station_user_change",
    )

    class Meta:
        db_table = "zonestation"
        constraints = [
            ForeignReferencesConstraint(
                "general.ZoneStation",
                name="r_275",
                from_fields=(
                    "version",
                    "zone_id",
                    "type_zone",
                ),
                to_fields=("version", "zone_station_id", "type"),
            ),
        ]

    def __str__(self):
        return f"{self.description}[{self.pk}]"


class StationGroup(models.Model):
    """
    Together with the table StationGroupElements you can define a group of stations
    for sales limitation rules.
    This table contains only the ID and description of a station group. This maybe
    useful for Special Events, which will be sold-valid only at some stations.
    """

    pk = models.CompositePrimaryKey("version", "station_group_id")
    group_type = models.IntegerField(
        db_column="grouptype",
        blank=True,
        null=True,
        help_text="Determines the type of the group",
    )
    station_group_id = models.IntegerField(
        db_column="stationgroupid",
        help_text="Unique identification of this station group",
    )
    description = models.CharField(
        max_length=50, blank=True, help_text="describes the intention of list"
    )
    time_change = models.DateTimeField(
        db_column="timechange", blank=True, null=True, auto_now=True
    )
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_station_group_set",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_station_grooup_set",
    )
    version = models.ForeignKey(
        "TariffVersions",
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="station_groups",
    )

    class Meta:
        db_table = "stationgroup"

    def __str__(self):
        return self.description


class StationGroupElements(models.Model):
    """
    List of all stations grouped into a station group.
    """

    pk = models.CompositePrimaryKey(
        "version",
        "station_type",
        "station_id",
        "station_group_id",
    )
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="station_group_elements",
    )
    station_type = models.IntegerField(db_column="stationtype")
    station_id = models.IntegerField(
        db_column="stationid", help_text="ID of Zone,Station or Connection"
    )
    station_group_id = models.IntegerField(
        db_column="stationgroupid", help_text="Unique identification of a station group"
    )

    station_group = models.ForeignObject(
        StationGroup,
        on_delete=models.DO_NOTHING,
        from_fields=("version", "station_group_id"),
        to_fields=("version", "station_group_id"),
        related_name="station_group_elements",
    )
    station = models.ForeignObject(
        ZoneStation,
        models.DO_NOTHING,
        from_fields=("version", "station_id", "station_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="station_group_elements",
    )

    class Meta:
        db_table = "stationgroupelements"
        constraints = [
            ForeignReferencesConstraint(
                "general.ZoneStation",
                name="r_184",
                from_fields=(
                    "version",
                    "station_id",
                    "station_type",
                ),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                "general.StationGroup",
                name="r_185",
                from_fields=("version", "station_group_id"),
                to_fields=("version", "station_group_id"),
            ),
        ]

    def __str__(self):
        return "StationGroupElements: {},{},{},{}".format(  # noqa: UP032
            self.version,
            self.station_type,
            self.station_id,
            self.station_group_id,
        )


class StationRouteElements(models.Model):
    """
    This table links several stations to one line-branch and several lines-branches
    to one station.
    """

    pk = models.CompositePrimaryKey("version", "station_id", "station_type", "route_id")
    version = models.ForeignKey(
        "TariffVersions",
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="station_route_elements",
    )
    station_id = models.IntegerField(
        db_column="stationid", help_text="ID of Zone,Station or Connection"
    )
    route_id = models.ForeignKey(
        Routes,
        models.CASCADE,
        db_column="routeid",
        help_text="Unique ID of Route",
        related_name="station_route_elements",
    )
    station_type = models.IntegerField(db_column="stationtype", choices=ZoneStationType)
    zone_station = models.ForeignObject(
        "ZoneStation",
        models.CASCADE,
        from_fields=("version", "station_id", "station_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="station_route_elements",
    )
    station_index = models.IntegerField(
        db_column="stationindex",
        blank=True,
        null=True,
        help_text="ID to set up a station order on this line (route)",
    )
    description = models.CharField(max_length=50, blank=True, help_text="Description")
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    time_change = models.DateTimeField(
        db_column="timechange", blank=True, null=True, auto_now=True
    )
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_station_route_elements",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_station_route_elements",
    )

    class Meta:
        db_table = "stationrouteelements"
        constraints = [
            ForeignReferencesConstraint(
                "general.ZoneStation",
                name="r_173",
                from_fields=(
                    "version",
                    "station_id",
                    "station_type",
                ),
                to_fields=("version", "zone_station_id", "type"),
            ),
        ]

    def __str__(self):
        return self.description


class DeviceClassType(models.IntegerChoices):
    TVM = (1, "TVM")
    TOM = (2, "TOM")
    HCR = (3, "HCR")
    GATE = (4, "GATE")


class DeviceClassTestFlag(models.IntegerChoices):
    NORMAL = (0, "normal device class")
    TEST = (1, "test device class")


class TypeOfTariffDownloadData(models.IntegerChoices):
    MDB = (0, "database (mdb)")
    TBL = (1, "compact binary (tbl)")


class DeviceClass(models.Model):
    device_class_id = models.IntegerField(
        db_column="deviceclassid",
        primary_key=True,
        help_text="Unique identifier of DeviceClass",
    )
    description = models.CharField(
        unique=True,
        max_length=30,
        blank=True,
        null=True,
        help_text="description of device class",
    )
    device_class_type = models.IntegerField(
        db_column="deviceclasstype", choices=DeviceClassType, blank=True, null=True
    )
    parameter_group_id = models.IntegerField(
        db_column="parametergroupid", blank=True, null=True
    )
    test_flag = models.BooleanField(
        db_column="testflag", default=False, choices=DeviceClassTestFlag
    )
    time_change = models.DateTimeField(
        db_column="timechange", blank=True, null=True, auto_now=True
    )
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    tvm_apl_tar_version_group_id = models.IntegerField(
        db_column="tvmapltarversiongroupid", blank=True, null=True
    )
    tvm_sw_version_group_id = models.IntegerField(
        db_column="tvmswversiongroupid", blank=True, null=True
    )
    tvm_tech_version_group_id = models.IntegerField(
        db_column="tvmtechversiongroupid", blank=True, null=True
    )
    type_of_tariff_download_data = models.IntegerField(
        help_text="Data type of tariff download data",
        db_column="typeoftariffdownloaddata",
        default=TypeOfTariffDownloadData.MDB,
        choices=TypeOfTariffDownloadData,
    )
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_device_class_set",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_device_class_set",
    )

    class Meta:
        db_table = "deviceclass"
        verbose_name = "Device Class"
        verbose_name_plural = "Device Classes"

    def __str__(self):
        return self.description


class DeviceClassGroup(models.Model):
    """
    The 'DeviceClassGroup' has a link to tariff tables for which we have
    to state different definitions or restrictions based on a group of devices.

    A group of devices could be all TOMs, all TSMs for example.
    """

    pk = models.CompositePrimaryKey("version", "device_class_group_id")
    device_class_group_id = models.IntegerField(
        db_column="deviceclassgroupid",
        help_text="Unique identification of a device class group",
    )
    version = models.ForeignKey(
        "TariffVersions",
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="device_class_groups",
    )
    description = models.CharField(
        max_length=50,
        blank=True,
        help_text="description: example: 'only TSM', 'TSM and TOM'",
    )
    time_change = models.DateTimeField(
        db_column="timechange", blank=True, null=True, auto_now=True
    )
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_device_class_group_set",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_device_class_group_set",
    )

    class Meta:
        db_table = "deviceclassgroup"

    def __str__(self):
        return self.description


class DeviceClassGroupElements(models.Model):
    """
    This table is used for grouping single device classes into a 'DeviceClassGroup'.
    """

    pk = models.CompositePrimaryKey("device_class_group_id", "version", "device_class")
    device_class_group_id = models.IntegerField(db_column="deviceclassgroupid")

    version = models.ForeignKey(
        "TariffVersions",
        on_delete=models.CASCADE,
        db_column="versionid",
        related_name="device_class_group_elements",
        help_text="ID of tariff version",
    )
    device_class_group = models.ForeignObject(
        "DeviceClassGroup",
        on_delete=models.CASCADE,
        from_fields=("version", "device_class_group_id"),
        to_fields=("version", "device_class_group_id"),
        serialize=False,
        editable=False,
    )
    device_class = models.ForeignKey(
        "DeviceClass",
        models.CASCADE,
        db_column="deviceclassid",
        related_name="device_class_group_elements",
    )

    class Meta:
        db_table = "deviceclassgroupelements"
        constraints = [
            ForeignReferencesConstraint(
                "general.DeviceClassGroup",
                name="r_190",
                from_fields=("version", "device_class_group_id"),
                to_fields=("version", "device_class_group_id"),
            )
        ]

    def __str__(self):
        return (
            "DeviceClassGroupElements:"
            f"{self.device_class_group_id},{self.version},{self.device_class}"
        )


class TimeLock(models.Model):
    """
    This table will give you the possibility to set up exceptions based on
    time and-or date.
    It is used for every time-date related restrictions (also for presales).
    If the holiday flag is set, the application will also lock into the holiday table.
    """

    class PRIORITIES(models.IntegerChoices):
        LOW = (0, "low")
        NORMAL = (1, "normal")
        HIGH = (2, "high")

    pk = models.CompositePrimaryKey("version", "time_lock_id", "device_class_group_id")
    version = models.ForeignKey(
        TariffVersions,
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="time_locks",
    )
    time_lock_id = models.IntegerField(
        db_column="timelockid", help_text="Unique id of timelock entry"
    )
    device_class_group_id = models.IntegerField(
        db_column="deviceclassgroupid",
        help_text="Unique identification of a device class group",
    )
    device_class_group = models.ForeignObject(
        DeviceClassGroup,
        models.CASCADE,
        from_fields=("version", "device_class_group_id"),
        to_fields=("version", "device_class_group_id"),
        serialize=False,
    )
    pre_sale_entry = models.IntegerField(
        db_column="presaleentry",
        blank=True,
        null=True,
        help_text="0 - no presale entry / 1 - entry defines a presale",
    )
    lock_flag = models.IntegerField(
        db_column="lockflag",
        blank=True,
        null=True,
        help_text="0 - Entry locks for the time definition / "
        "1 - enables for the time definition",
    )
    holiday_lock = models.IntegerField(
        db_column="holidaylock",
        blank=True,
        null=True,
        help_text="0 - holidays are excluded/1 - holidays are included",
    )
    days_of_week = models.IntegerField(
        db_column="daysofweek",
        blank=True,
        null=True,
        help_text="Field could be used to define days of the week for restrictions",
    )
    days_of_month = models.IntegerField(
        db_column="daysofmonth",
        blank=True,
        null=True,
        help_text="Field could be used to define days of the month for restrictions",
    )
    valid_from = models.DateField(db_column="validfrom", blank=True, null=True)
    valid_to = models.DateField(db_column="validto", blank=True, null=True)
    priority = models.IntegerField(
        db_column="priority", blank=True, null=True, choices=PRIORITIES
    )
    description = models.CharField(db_column="description", max_length=30, blank=True)
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    time_change = models.DateTimeField(
        db_column="timechange", blank=True, null=True, auto_now=True
    )
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_time_lock",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_time_lock",
    )

    class Meta:
        db_table = "timelock"

    def __str__(self):
        return self.description


class TimeLockGroup(models.Model):
    """
    This is the description of a group of time lock definitions.
    A group may also contain only one restriction.
    """

    pk = models.CompositePrimaryKey("version", "time_lock_group_id")
    time_lock_group_id = models.IntegerField(
        db_column="timelockgroupid",
        help_text="Identifier for a specified Timelockgroup",
    )
    description = models.CharField(
        max_length=50,
        blank=True,
        help_text="Description for this, example: "
        "'on weekdays between 9:00 and 11:00 am', not on holidays",
    )
    lock_flag = models.IntegerField(
        db_column="lockflag",
        blank=True,
        null=True,
        help_text="Get customer specific value from Tariff_Defines.ini file",
    )
    multimedia_group_id = models.IntegerField(
        db_column="multimediagroupid",
        blank=True,
        null=True,
        help_text="Unique identification of a Multimedia Group",
    )
    time_change = models.DateTimeField(
        db_column="timechange", blank=True, null=True, auto_now=True
    )
    time_lock = models.IntegerField(
        db_column="timelock",
        blank=True,
        null=True,
        help_text="0 - Entry locks for the time definition / "
        "1 - enables for the time definition",
    )
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)

    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_time_lock_group",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_time_lock_group",
    )
    version = models.ForeignKey(
        TariffVersions,
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="time_lock_groups",
    )

    class Meta:
        db_table = "timelockgroup"

    def __str__(self):
        return self.description


class TimeLockGroupElements(models.Model):
    """This table binds one or more time lock definitions into one Group."""

    pk = models.CompositePrimaryKey(
        "version",
        "time_lock_group_id",
        "time_lock_id",
        "device_class_group_id",
    )
    version = models.ForeignKey(
        TariffVersions,
        models.CASCADE,
        db_column="versionid",
        related_name="time_lock_group_elements",
    )
    device_class_group_id = models.IntegerField(db_column="deviceclassgroupid")
    device_class_group = models.ForeignObject(
        DeviceClassGroup,
        models.CASCADE,
        from_fields=("version", "device_class_group_id"),
        to_fields=("version", "device_class_group_id"),
    )
    time_lock_group_id = models.IntegerField(db_column="timelockgroupid")
    time_lock_group = models.ForeignObject(
        TimeLockGroup,
        models.CASCADE,
        from_fields=("version", "time_lock_group_id"),
        to_fields=("version", "time_lock_group_id"),
    )
    time_lock_id = models.IntegerField(db_column="timelockid")
    time_lock = models.ForeignObject(
        TimeLock,
        models.CASCADE,
        from_fields=("version", "time_lock_id", "device_class_group_id"),
        to_fields=("version", "time_lock_id", "device_class_group_id"),
    )

    class Meta:
        db_table = "timelockgroupelements"
        constraints = [
            ForeignReferencesConstraint(
                "general.TimeLockGroup",
                name="r_179",
                from_fields=("version", "time_lock_group_id"),
                to_fields=("version", "time_lock_group_id"),
            ),
            ForeignReferencesConstraint(
                "general.TimeLock",
                name="r_180",
                from_fields=("version", "time_lock_id", "device_class_group_id"),
                to_fields=("version", "time_lock_id", "device_class_group_id"),
            ),
        ]

    def __str__(self):
        return "{},{},{},{}".format(  # noqa: UP032
            self.version,
            self.time_lock_group_id,
            self.time_lock_id,
            self.device_class_group_id,
        )


class Validity(models.Model):
    """Validity rules of appropriate ticket types"""

    class TYPES(models.IntegerChoices):
        ABSOLUTE = 1, "absolute start/end definition"
        RANGE = 2, "date/time of sale and duration"
        RELATIVE_DURATION = 3, "relative starting point and duration"
        RELATIVE = 4, "arelative starting point to relative ending point"

    class DURATIONTYPES(models.IntegerChoices):
        MINUTE = 1, "minute"
        HOUR = 2, "hour"
        DAY = 4, "day"
        WORKDAY = 5, "workday"
        CAL_DAY = 8, "calendar day"
        CAL_MONTH = 9, "calendar month"
        CAL_YEAR = 10, "calendar year"

    pk = models.CompositePrimaryKey("version", "validity_id")
    validity_id = models.IntegerField(db_column="validityid")
    validity_type = models.IntegerField(
        db_column="validitytype", blank=True, null=True, choices=TYPES
    )
    description = models.CharField(max_length=50, blank=True)
    duration_type = models.IntegerField(
        db_column="durationtype", blank=True, null=True, choices=DURATIONTYPES
    )
    duration_value = models.IntegerField(
        db_column="durationvalue",
        blank=True,
        null=True,
        help_text="number of units for duration type",
    )
    end_def = models.DateField(
        db_column="enddef", blank=True, null=True, help_text="absolute end definition"
    )
    end_rel_dayofmonth_next = models.BooleanField(
        db_column="endreldayofmonthnext", blank=True, null=True
    )
    end_rel_dayofmonth_used = models.BooleanField(
        db_column="endreldayofmonthused", blank=True, null=True
    )
    end_rel_dayofmonth_value = models.IntegerField(
        db_column="endreldayofmonthvalue", blank=True, null=True
    )
    end_rel_dayofweek_next = models.BooleanField(
        db_column="endreldayofweeknext", blank=True, null=True
    )
    end_rel_dayofweek_used = models.BooleanField(
        db_column="endreldayofweekused", blank=True, null=True
    )
    end_rel_dayofweek_value = models.IntegerField(
        db_column="endreldayofweekvalue", blank=True, null=True
    )
    end_rel_hour_next = models.BooleanField(
        db_column="endrelhournext", blank=True, null=True
    )
    end_rel_hour_used = models.BooleanField(
        db_column="endrelhourused", blank=True, null=True
    )
    end_rel_hour_value = models.IntegerField(
        db_column="endrelhourvalue", blank=True, null=True
    )
    end_rel_minute_next = models.BooleanField(
        db_column="endrelminutenext", blank=True, null=True
    )
    end_rel_minute_used = models.BooleanField(
        db_column="endrelminuteused", blank=True, null=True
    )
    end_rel_minute_value = models.IntegerField(
        db_column="endrelminutevalue", blank=True, null=True
    )
    end_rel_month_next = models.BooleanField(
        db_column="endrelmonthnext", blank=True, null=True
    )
    end_rel_month_used = models.BooleanField(
        db_column="endrelmonthused", blank=True, null=True
    )
    end_rel_month_value = models.IntegerField(
        db_column="endrelmonthvalue", blank=True, null=True
    )
    end_rel_week_next = models.BooleanField(
        db_column="endrelweeknext", blank=True, null=True
    )
    end_rel_week_used = models.BooleanField(
        db_column="endrelweekused", blank=True, null=True
    )
    end_rel_week_value = models.IntegerField(
        db_column="endrelweekvalue", blank=True, null=True
    )
    multimedia_group_id = models.IntegerField(
        db_column="multimediagroupid",
        blank=True,
        null=True,
        help_text="Unique identification of a Multimedia Group",
    )
    start_def = models.DateField(
        db_column="startdef",
        blank=True,
        null=True,
        help_text="absolute start definition",
    )
    start_rel_dayofmonth_next = models.BooleanField(
        db_column="startreldayofmonthnext", blank=True, null=True
    )
    start_rel_dayofmonth_used = models.BooleanField(
        db_column="startreldayofmonthused", blank=True, null=True
    )
    start_rel_dayofmonth_value = models.IntegerField(
        db_column="startreldayofmonthvalue", blank=True, null=True
    )
    start_rel_dayofweek_next = models.BooleanField(
        db_column="startreldayofweeknext", blank=True, null=True
    )
    start_rel_dayofweek_used = models.BooleanField(
        db_column="startreldayofweekused", blank=True, null=True
    )
    start_rel_dayofweek_value = models.IntegerField(
        db_column="startreldayofweekvalue", blank=True, null=True
    )
    start_rel_hour_next = models.BooleanField(
        db_column="startrelhournext", blank=True, null=True
    )
    start_rel_hour_used = models.BooleanField(
        db_column="startrelhourused", blank=True, null=True
    )
    start_rel_hour_value = models.IntegerField(
        db_column="startrelhourvalue",
        blank=True,
        null=True,
        help_text="value for start minute of a hour (0-59)",
    )
    start_rel_minute_next = models.BooleanField(
        db_column="startrelminutenext",
        blank=True,
        null=True,
        help_text="start for next full minute",
    )
    start_rel_minute_used = models.BooleanField(
        db_column="startrelminuteused",
        blank=True,
        null=True,
        help_text="minute field is used",
    )
    start_rel_minute_value = models.IntegerField(
        db_column="startrelminutevalue", blank=True, null=True
    )
    start_rel_month_next = models.BooleanField(
        db_column="startrelmonthnext", blank=True, null=True
    )
    start_rel_month_used = models.BooleanField(
        db_column="startrelmonthused", blank=True, null=True
    )
    start_rel_month_value = models.IntegerField(
        db_column="startrelmonthvalue", blank=True, null=True
    )
    start_rel_week_next = models.BooleanField(
        db_column="startrelweeknext", blank=True, null=True
    )
    start_rel_week_used = models.BooleanField(
        db_column="startrelweekused", blank=True, null=True
    )
    start_rel_week_value = models.IntegerField(
        db_column="startrelweekvalue", blank=True, null=True
    )
    time_change = models.DateTimeField(
        db_column="timechange", blank=True, null=True, auto_now=True
    )
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_validity",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_validity",
    )
    version = models.ForeignKey(
        TariffVersions, models.CASCADE, db_column="versionid", related_name="validities"
    )

    class Meta:
        db_table = "validity"
        verbose_name = "Validity"
        verbose_name_plural = "Validities"

    def __str__(self):
        return "{},{}".format(  # noqa: UP032
            self.version,
            self.validity_id,
        )


class TVMStation(models.Model):
    """
    This table stores the stations (Haltestellen).
    Each TVM has to be assigned a correct station
    """

    class TYPES(models.IntegerChoices):
        GARAGE = 1, "Garage"
        __empty__ = "Station"

    station_id = models.IntegerField(
        primary_key=True,
        db_column="stationid",
        help_text="The station number of the station 1-9999",
    )
    station_type = models.IntegerField(db_column="stationtype", choices=TYPES)
    company = models.ForeignKey(
        Company,
        models.SET_NULL,
        db_column="companyid",
        blank=True,
        null=True,
        related_name="tvm_stations",
    )

    graphic_key = models.IntegerField(
        db_column="graphickey",
        blank=True,
        null=True,
        help_text="Foreign key to look for the graphic settings",
    )
    name = models.CharField(
        db_column="name",
        max_length=30,
        blank=True,
        help_text="The normal name of the station",
    )
    name_long = models.CharField(
        db_column="namelong",
        max_length=30,
        blank=True,
        help_text="The station name and the town's name",
    )
    name_short = models.CharField(
        db_column="nameshort",
        max_length=20,
        help_text="A short name that identifies the station",
    )
    town = models.CharField(
        db_column="town",
        max_length=20,
        blank=True,
        help_text="The name of the town where the station resides",
    )

    tariff_property = models.IntegerField(
        db_column="tariffproperty",
        blank=True,
        null=True,
        help_text="The tariff property is printed on the ticket",
    )
    tariff_zone = models.IntegerField(
        db_column="tariffzone",
        blank=True,
        null=True,
        help_text="This value is used to find the correct relation",
    )
    time_change = models.DateTimeField(
        db_column="timechange",
        blank=True,
        null=True,
        help_text="Date and time of changing entry",
        auto_now=True,
    )
    time_new = models.DateTimeField(
        db_column="timenew",
        blank=True,
        null=True,
        help_text="Date and time of creating entry",
    )
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_tvmstation",
        help_text="User Name of changing entry",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_tvmstation",
        help_text="User Name of creating entry",
    )

    class Meta:
        db_table = "tvmstation"
        verbose_name = "TVM Station"
        verbose_name_plural = "TVM Stations"

    def __str__(self):
        return self.name


class Country(BaseAuditModel, BaseValidModel):
    description = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = "countries"
        verbose_name = "Countries"

    def __str__(self):
        return self.description


class Department(BaseAuditModel, BaseValidModel):
    description = models.CharField(max_length=100)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = "departments"

    def __str__(self):
        return self.description


class Status(BaseAuditModel, BaseValidModel):
    description = models.CharField(max_length=100)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = "statues"
        verbose_name = "Statuses"

    def __str__(self):
        return self.description


class ConnectingService(BaseAuditModel, BaseValidModel):
    description = models.CharField(max_length=100)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = "connecting_services"

    def __str__(self):
        return self.description
