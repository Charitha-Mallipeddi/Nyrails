# ruff: noqa: DJ001
import os

from django.db import models

DATADUMP = bool(os.getenv("DATADUMP", "False"))


class Company(models.Model):
    adress1 = models.CharField(max_length=50, blank=True, null=True)
    adress2 = models.CharField(max_length=50, blank=True, null=True)
    bankaccountno1 = models.CharField(max_length=20, blank=True, null=True)
    bankaccountno2 = models.CharField(max_length=20, blank=True, null=True)
    bankidentno1 = models.CharField(max_length=20, blank=True, null=True)
    bankidentno2 = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    companyid = models.IntegerField(primary_key=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    costcenterid = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    ispreferredsalescontractor = models.BooleanField(blank=True, null=True)
    ispreferredsalespromoter = models.BooleanField(blank=True, null=True)
    isproductissuer = models.BooleanField(blank=True, null=True)
    issalescontractor = models.BooleanField(blank=True, null=True)
    issalespromoter = models.BooleanField(blank=True, null=True)
    memotext = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=50)
    parametergroupid = models.IntegerField(blank=True, null=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    picturemap = models.CharField(max_length=50, blank=True, null=True)
    postalcode = models.CharField(max_length=10, blank=True, null=True)
    shortname = models.CharField(unique=True, max_length=8)
    simfotoid = models.IntegerField(blank=True, null=True)
    stateprovince = models.CharField(max_length=50, blank=True, null=True)
    taxid = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    turnovertaxid = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    validflag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "company"

    def __str__(self):
        return self.name


class DeviceClass(models.Model):
    balancegroupid = models.IntegerField(blank=True, null=True)
    description = models.CharField(unique=True, max_length=30, blank=True, null=True)
    deviceclassid = models.IntegerField(primary_key=True)
    deviceclasstype = models.IntegerField(blank=True, null=True)
    parametergroupid = models.IntegerField(blank=True, null=True)
    ruleartifactid = models.CharField(max_length=50, blank=True, null=True)
    testflag = models.BooleanField()
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    tvmapltarversiongroupid = models.IntegerField(blank=True, null=True)
    tvmswversiongroupid = models.IntegerField(blank=True, null=True)
    tvmtarversiongroupid = models.IntegerField(blank=True, null=True)
    tvmtechversiongroupid = models.IntegerField(blank=True, null=True)
    typeoftariffdownloaddata = models.IntegerField()
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "deviceclass"

    def __str__(self):
        return self.description


class TariffVersions(models.Model):
    description = models.CharField(max_length=50, blank=True, null=True)
    rail_road = models.ForeignKey(
        Company,
        models.DO_NOTHING,
        db_column="railroadid",
        blank=True,
        null=True,
    )
    status = models.IntegerField(blank=True, null=True)
    theovertakerflag = models.BooleanField()
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    validityendtime = models.DateTimeField(blank=True, null=True)
    validitystarttime = models.DateTimeField(blank=True, null=True)
    versionid = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "tariffversions"

    def __str__(self):
        return self.description


class DeviceClassGroup(models.Model):
    pk = models.CompositePrimaryKey("version", "deviceclassgroupid")
    description = models.CharField(max_length=50, blank=True, null=True)
    deviceclassgroupid = models.IntegerField()
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )

    class Meta:
        managed = False
        db_table = "deviceclassgroup"

    def __str__(self):
        return self.description


class DeviceClassGroupElements(models.Model):
    pk = models.CompositePrimaryKey("deviceclassgroupid", "version", "deviceclassid")
    deviceclassgroupid = models.IntegerField()
    if not DATADUMP:
        device_class_group = models.ForeignObject(
            DeviceClassGroup,
            models.DO_NOTHING,
            from_fields=("version", "deviceclassgroupid"),
            to_fields=("version", "deviceclassgroupid"),
        )
    deviceclassid = models.ForeignKey(
        DeviceClass,
        models.DO_NOTHING,
        db_column="deviceclassid",
    )
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
        related_name="deviceclassgroupelements_version_set",
    )

    class Meta:
        managed = False
        db_table = "deviceclassgroupelements"

    def __str__(self):
        return "DeviceClassGroupElements:{},{},{}".format(  # noqa: UP032
            self.deviceclassgroupid,
            self.version.pk,
            self.deviceclassid,
        )


class ZoneStation(models.Model):
    pk = models.CompositePrimaryKey("version", "zonestationid", "type")
    description = models.CharField(max_length=50, blank=True, null=True)
    externalid = models.CharField(max_length=20, blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    parameter1 = models.IntegerField(blank=True, null=True)
    parameter2 = models.IntegerField(blank=True, null=True)
    parameter3 = models.IntegerField(blank=True, null=True)
    parameter4 = models.IntegerField(blank=True, null=True)
    parameter5 = models.IntegerField(blank=True, null=True)
    parameter6 = models.IntegerField(blank=True, null=True)
    parameter7 = models.IntegerField(blank=True, null=True)
    parameter8 = models.IntegerField(blank=True, null=True)
    parameter9 = models.IntegerField(blank=True, null=True)
    parameter10 = models.IntegerField(blank=True, null=True)
    parameter11 = models.CharField(max_length=50, blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(unique=True)
    typezone = models.IntegerField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
    )
    if not DATADUMP:
        zone = models.ForeignObject(
            "self",
            models.DO_NOTHING,
            from_fields=("version", "zoneid", "typezone"),
            to_fields=("version", "zonestationid", "type"),
        )
    zoneid = models.IntegerField(blank=True, null=True)
    zonestationid = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = "zonestation"
        ordering = ["-zoneid", "-typezone", "-zonestationid", "-typezone"]
        constraints = [
            models.UniqueConstraint(
                fields=["version", "zonestationid", "type"],
                name="xpkzonestation",
            ),
        ]

    def __str__(self):
        return self.description


class MainShift(models.Model):
    pk = models.CompositePrimaryKey("deviceclassid", "deviceid", "uniquemsid")
    deviceclassid = models.IntegerField()
    mainshiftno = models.IntegerField()
    deviceid = models.IntegerField()
    uniquemsid = models.IntegerField()
    startcreadate = models.DateField()
    starteventsequno = models.IntegerField(blank=True, null=True)
    endcreadate = models.DateField(blank=True, null=True)
    polldate = models.DateField(blank=True, null=True)
    endeventsequno = models.IntegerField(blank=True, null=True)
    proceedingtype = models.IntegerField(blank=True, null=True)
    dbwritecmddate = models.DateField(blank=True, null=True)
    vendorno = models.IntegerField(blank=True, null=True)
    modulno = models.IntegerField(blank=True, null=True)
    vehicleno = models.IntegerField(blank=True, null=True)
    modulusertype = models.IntegerField(blank=True, null=True)
    shiftminuspiece = models.IntegerField(blank=True, null=True)
    serviceno = models.IntegerField(blank=True, null=True)
    tariffversion = models.IntegerField(blank=True, null=True)
    shiftminusamount = models.IntegerField(blank=True, null=True)
    tarifflocationid = models.IntegerField(blank=True, null=True)
    routeno = models.IntegerField(blank=True, null=True)
    shifttype = models.IntegerField(blank=True, null=True)
    locationtype = models.IntegerField(blank=True, null=True)
    locationid = models.IntegerField(blank=True, null=True)
    sellingrrid = models.IntegerField(blank=True, null=True)
    shiftpiece = models.IntegerField(blank=True, null=True)
    tourno = models.IntegerField(blank=True, null=True)
    shiftoutamount = models.IntegerField(blank=True, null=True)
    cashless = models.IntegerField(blank=True, null=True)
    creditamount = models.IntegerField(blank=True, null=True)
    lastsalesshiftno = models.IntegerField(blank=True, null=True)
    mainshiftclosestatus = models.IntegerField(blank=True, null=True)
    jobid = models.CharField(max_length=24, blank=True, null=True)
    jobsequid = models.IntegerField(blank=True, null=True)
    bankcode = models.BigIntegerField(blank=True, null=True)
    bankaccount = models.BigIntegerField(blank=True, null=True)
    auditstatus = models.IntegerField(blank=True, null=True)
    insertdate = models.DateField(blank=True, null=True)
    testflag = models.BooleanField()
    auditorsystemid = models.CharField(max_length=20, blank=True, null=True)
    statusdatetime = models.DateField(blank=True, null=True)
    jobstate = models.IntegerField(blank=True, null=True)
    soldcurrency = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    shiftchangereasonstart = models.IntegerField(blank=True, null=True)
    shiftchangereasonend = models.IntegerField(blank=True, null=True)
    sbserialnumber = models.IntegerField(blank=True, null=True)
    baseplateid = models.CharField(max_length=12, blank=True, null=True)
    soldforcompany = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "mainshift"
        unique_together = (
            (
                "deviceclassid",
                "deviceid",
                "startcreadate",
                "endcreadate",
                "mainshiftno",
            ),
        )

    def __str__(self):
        return "MainShift: {},{},{}".format(  # noqa: UP032
            self.deviceclassid,
            self.deviceid,
            self.uniquemsid,
        )


class MainShiftGroup(models.Model):
    pk = models.CompositePrimaryKey("deviceclassid", "deviceid", "groupid")
    deviceclassid = models.IntegerField()
    groupid = models.IntegerField()
    startcreadate = models.DateField(blank=True, null=True)
    endcreadate = models.DateField(blank=True, null=True)
    starteventsequno = models.IntegerField(blank=True, null=True)
    endeventsequno = models.IntegerField(blank=True, null=True)
    startmainshiftno = models.IntegerField(blank=True, null=True)
    endmainshiftno = models.IntegerField(blank=True, null=True)
    startuniquemsid = models.IntegerField(blank=True, null=True)
    enduniquemsid = models.IntegerField(blank=True, null=True)
    flag_isbasegroup = models.BooleanField(blank=True, null=True)
    user_isbasegroup = models.CharField(max_length=50, blank=True, null=True)
    time_isbasegroup = models.DateField(blank=True, null=True)
    deviceid = models.IntegerField()

    class Meta:
        managed = False
        db_table = "mainshiftgroup"

    def __str__(self):
        return "MainShiftGroup: {},{},{}".format(  # noqa: UP032
            self.deviceclassid,
            self.deviceid,
            self.groupid,
        )


class MainShiftGroupElements(models.Model):
    pk = models.CompositePrimaryKey("deviceclassid", "deviceid", "uniquemsid")
    dbwritecmddate = models.DateField(blank=True, null=True)
    deviceclassid = models.IntegerField()
    deviceid = models.IntegerField()
    endcreadate = models.DateField(blank=True, null=True)
    endeventsequno = models.IntegerField(blank=True, null=True)
    groupid = models.IntegerField(blank=True, null=True)
    insertdate = models.DateField(blank=True, null=True)
    mainshiftno = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    startcreadate = models.DateField(blank=True, null=True)
    starteventsequno = models.IntegerField(blank=True, null=True)
    uniquemsid = models.IntegerField()

    class Meta:
        managed = False
        db_table = "mainshiftgroupelements"

    def __str__(self):
        return "MainShiftGroupElements: {},{},{}".format(  # noqa: UP032
            self.deviceclassid,
            self.deviceid,
            self.uniquemsid,
        )


class Routes(models.Model):
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )
    routeid = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    simfotoid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "routes"

    def __str__(self):
        return self.description


class TVMStation(models.Model):
    company = models.ForeignKey(
        Company,
        models.DO_NOTHING,
        db_column="companyid",
        blank=True,
        null=True,
    )
    externalid = models.CharField(max_length=20, blank=True, null=True)
    graphickey = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    namelong = models.CharField(max_length=30, blank=True, null=True)
    nameshort = models.CharField(max_length=20)
    simfotoid = models.IntegerField(blank=True, null=True)
    stationid = models.IntegerField(primary_key=True)
    stationtype = models.IntegerField()
    tariffproperty = models.IntegerField(blank=True, null=True)
    tariffzone = models.IntegerField(blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    town = models.CharField(max_length=20, blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "tvmstation"

    def __str__(self):
        return self.name


class StationGroup(models.Model):
    pk = models.CompositePrimaryKey("version", "stationgroupid")
    description = models.CharField(max_length=50, blank=True, null=True)
    grouptype = models.IntegerField(blank=True, null=True)
    stationgroupid = models.IntegerField()
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )

    class Meta:
        managed = False
        db_table = "stationgroup"
        constraints = [
            models.UniqueConstraint(
                fields=["versionid", "stationgroupid"],
                name="xpkstationgroup",
            ),
        ]

    def __str__(self):
        return self.description


class StationGroupElements(models.Model):
    pk = models.CompositePrimaryKey(
        "version",
        "stationtype",
        "stationid",
        "stationgroupid",
    )
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )
    stationtype = models.IntegerField()
    stationid = models.IntegerField()
    stationgroupid = models.IntegerField()
    if not DATADUMP:
        station_group = models.ForeignObject(
            StationGroup,
            on_delete=models.DO_NOTHING,
            from_fields=("version", "stationgroupid"),
            to_fields=("version", "stationgroupid"),
        )
        zone_station = models.ForeignObject(
            ZoneStation,
            models.DO_NOTHING,
            from_fields=("version", "stationid", "stationtype"),
            to_fields=("version", "zonestationid", "type"),
        )

    class Meta:
        managed = False
        db_table = "stationgroupelements"

    def __str__(self):
        return "StationGroupElements: {},{},{},{}".format(  # noqa: UP032
            self.version,
            self.stationtype,
            self.stationid,
            self.stationgroupid,
        )


class StationRouteElements(models.Model):
    pk = models.CompositePrimaryKey("version", "stationid", "stationtype", "routeid")
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )
    stationid = models.IntegerField()
    routeid = models.ForeignKey(Routes, models.DO_NOTHING, db_column="routeid")
    stationtype = models.IntegerField()
    if not DATADUMP:
        zone_station = models.ForeignObject(
            ZoneStation,
            models.DO_NOTHING,
            from_fields=("version", "stationid", "stationtype"),
            to_fields=("version", "zonestationid", "type"),
        )
    stationindex = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stationrouteelements"

    def __str__(self):
        return self.description


class Validity(models.Model):
    pk = models.CompositePrimaryKey("version", "validityid")
    description = models.CharField(max_length=50, blank=True, null=True)
    durationtype = models.IntegerField(blank=True, null=True)
    durationvalue = models.IntegerField(blank=True, null=True)
    enddef = models.DateField(blank=True, null=True)
    endreldayofmonthnext = models.BooleanField(blank=True, null=True)
    endreldayofmonthused = models.BooleanField(blank=True, null=True)
    endreldayofmonthvalue = models.IntegerField(blank=True, null=True)
    endreldayofweeknext = models.BooleanField(blank=True, null=True)
    endreldayofweekused = models.BooleanField(blank=True, null=True)
    endreldayofweekvalue = models.IntegerField(blank=True, null=True)
    endrelhournext = models.BooleanField(blank=True, null=True)
    endrelhourused = models.BooleanField(blank=True, null=True)
    endrelhourvalue = models.IntegerField(blank=True, null=True)
    endrelminutenext = models.BooleanField(blank=True, null=True)
    endrelminuteused = models.BooleanField(blank=True, null=True)
    endrelminutevalue = models.IntegerField(blank=True, null=True)
    endrelmonthnext = models.BooleanField(blank=True, null=True)
    endrelmonthused = models.BooleanField(blank=True, null=True)
    endrelmonthvalue = models.IntegerField(blank=True, null=True)
    endrelweeknext = models.BooleanField(blank=True, null=True)
    endrelweekused = models.BooleanField(blank=True, null=True)
    endrelweekvalue = models.IntegerField(blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    startdef = models.DateField(blank=True, null=True)
    startreldayofmonthnext = models.BooleanField(blank=True, null=True)
    startreldayofmonthused = models.BooleanField(blank=True, null=True)
    startreldayofmonthvalue = models.IntegerField(blank=True, null=True)
    startreldayofweeknext = models.BooleanField(blank=True, null=True)
    startreldayofweekused = models.BooleanField(blank=True, null=True)
    startreldayofweekvalue = models.IntegerField(blank=True, null=True)
    startrelhournext = models.BooleanField(blank=True, null=True)
    startrelhourused = models.BooleanField(blank=True, null=True)
    startrelhourvalue = models.IntegerField(blank=True, null=True)
    startrelminutenext = models.BooleanField(blank=True, null=True)
    startrelminuteused = models.BooleanField(blank=True, null=True)
    startrelminutevalue = models.IntegerField(blank=True, null=True)
    startrelmonthnext = models.BooleanField(blank=True, null=True)
    startrelmonthused = models.BooleanField(blank=True, null=True)
    startrelmonthvalue = models.IntegerField(blank=True, null=True)
    startrelweeknext = models.BooleanField(blank=True, null=True)
    startrelweekused = models.BooleanField(blank=True, null=True)
    startrelweekvalue = models.IntegerField(blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    validityid = models.IntegerField()
    validitytype = models.IntegerField(blank=True, null=True)
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
    )

    class Meta:
        managed = False
        db_table = "validity"

    def __str__(self):
        return "{},{}".format(  # noqa: UP032
            self.version,
            self.validityid,
        )


class TicketType(models.Model):
    pk = models.CompositePrimaryKey("version", "tickettypeid")
    amount = models.IntegerField(blank=True, null=True)
    balamount1 = models.IntegerField(blank=True, null=True)
    balamount2 = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    externalid = models.CharField(max_length=20, blank=True, null=True)
    farecalculationruleid = models.IntegerField(blank=True, null=True)
    genderinput = models.IntegerField(blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    parameter1 = models.IntegerField(blank=True, null=True)
    parameter10 = models.CharField(max_length=50, blank=True, null=True)
    parameter2 = models.IntegerField(blank=True, null=True)
    parameter3 = models.IntegerField(blank=True, null=True)
    parameter4 = models.IntegerField(blank=True, null=True)
    parameter5 = models.IntegerField(blank=True, null=True)
    parameter6 = models.IntegerField(blank=True, null=True)
    parameter7 = models.IntegerField(blank=True, null=True)
    parameter8 = models.IntegerField(blank=True, null=True)
    parameter9 = models.CharField(max_length=50, blank=True, null=True)
    sendonlevt = models.IntegerField(blank=True, null=True)
    serviceproviderid = models.ForeignKey(
        Company,
        models.DO_NOTHING,
        db_column="serviceproviderid",
        blank=True,
        null=True,
    )
    statetaxid = models.IntegerField(blank=True, null=True)
    summary = models.IntegerField(blank=True, null=True)
    ticketembgroupid = models.IntegerField(blank=True, null=True)
    tickettypeid = models.IntegerField()
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    validityid = models.IntegerField()
    if not DATADUMP:
        validity = models.ForeignObject(
            Validity,
            models.DO_NOTHING,
            from_fields=("validityid", "version"),
            to_fields=("validityid", "version"),
            auto_created=True,
        )
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )

    class Meta:
        managed = False
        db_table = "tickettype"

    def __str__(self):
        return self.description


class TicketTypeGroup(models.Model):
    pk = models.CompositePrimaryKey(
        "version",
        "tickettypegroupid",
        "tickettypegrouptype",
    )
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    tickettypegroupid = models.IntegerField()
    tickettypegrouptype = models.IntegerField()
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
    )

    class Meta:
        managed = False
        db_table = "tickettypegroup"

    def __str__(self):
        return self.description


class TicketTypeGroupElements(models.Model):
    pk = models.CompositePrimaryKey(
        "version",
        "tickettypeid",
        "tickettypegrouptype",
        "tickettypegroupid",
    )

    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )
    tickettypegroupid = models.IntegerField()
    tickettypeid = models.IntegerField()
    tickettypegrouptype = models.IntegerField()
    if not DATADUMP:
        ticket_type_group = models.ForeignObject(
            TicketTypeGroup,
            models.DO_NOTHING,
            from_fields=("version", "tickettypegroupid", "tickettypegrouptype"),
            to_fields=("version", "tickettypegroupid", "tickettypegrouptype"),
        )
        ticket_type = models.ForeignObject(
            TicketType,
            models.DO_NOTHING,
            from_fields=("version", "tickettypeid"),
            to_fields=("version", "tickettypeid"),
        )

    class Meta:
        managed = False
        db_table = "tickettypegroupelements"

    def __str__(self):
        return "{},{},{},{}".format(  # noqa: UP032
            self.version,
            self.tickettypeid,
            self.tickettypegrouptype,
            self.tickettypegroupid,
        )


class TimeLock(models.Model):
    pk = models.CompositePrimaryKey("version", "timelockid", "deviceclassgroupid")
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
    )
    timelockid = models.IntegerField()
    deviceclassgroupid = models.IntegerField()
    if not DATADUMP:
        device_class_group = models.ForeignObject(
            DeviceClassGroup,
            models.DO_NOTHING,
            from_fields=("version", "deviceclassgroupid"),
            to_fields=("version", "deviceclassgroupid"),
        )
    presaleentry = models.IntegerField(blank=True, null=True)
    lockflag = models.IntegerField(blank=True, null=True)
    holidaylock = models.IntegerField(blank=True, null=True)
    holidayclass = models.IntegerField(blank=True, null=True)
    daysofweek = models.IntegerField(blank=True, null=True)
    daysofmonth = models.IntegerField(blank=True, null=True)
    time1start = models.DateField(blank=True, null=True)
    time1end = models.DateField(blank=True, null=True)
    time2start = models.DateField(blank=True, null=True)
    time2end = models.DateField(blank=True, null=True)
    time3start = models.DateField(blank=True, null=True)
    time3end = models.DateField(blank=True, null=True)
    validfrom = models.DateField(blank=True, null=True)
    validto = models.DateField(blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "timelock"

    def __str__(self):
        return self.description


class TimeLockGroup(models.Model):
    pk = models.CompositePrimaryKey("version", "timelockgroupid")
    description = models.CharField(max_length=50, blank=True, null=True)
    lockflag = models.IntegerField(blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    timelock = models.IntegerField(blank=True, null=True)
    timelockgroupid = models.IntegerField()
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
    )

    class Meta:
        managed = False
        db_table = "timelockgroup"

    def __str__(self):
        return self.description


class TimeLockGroupElements(models.Model):
    pk = models.CompositePrimaryKey(
        "version",
        "timelockgroupid",
        "timelockid",
        "deviceclassgroupid",
    )
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
    )
    deviceclassgroupid = models.IntegerField()
    timelockgroupid = models.IntegerField()
    timelockid = models.IntegerField()
    if not DATADUMP:
        timelock_group = models.ForeignObject(
            TimeLockGroup,
            models.DO_NOTHING,
            from_fields=("version", "timelockgroupid"),
            to_fields=("version", "timelockgroupid"),
        )
        timelock = models.ForeignObject(
            TimeLock,
            models.DO_NOTHING,
            from_fields=("version", "timelockid", "deviceclassgroupid"),
            to_fields=("version", "timelockid", "deviceclassgroupid"),
        )

    class Meta:
        managed = False
        db_table = "timelockgroupelements"

    def __str__(self):
        return "{},{},{},{}".format(  # noqa: UP032
            self.version,
            self.timelockgroupid,
            self.timelockid,
            self.deviceclassgroupid,
        )


class SalesPackets(models.Model):
    pk = models.CompositePrimaryKey("version", "packetid")
    description = models.CharField(max_length=50, blank=True, null=True)
    deststationgroupid = models.IntegerField(blank=True, null=True)
    deviceclassgroupid = models.IntegerField(blank=True, null=True)

    externalid = models.CharField(max_length=20, blank=True, null=True)
    groupfareid = models.IntegerField(blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    packetid = models.IntegerField()
    packettype = models.IntegerField(blank=True, null=True)
    payacceptgroupid = models.IntegerField(blank=True, null=True)
    plusgroupid = models.IntegerField(blank=True, null=True)
    salesstationgroupid = models.IntegerField(blank=True, null=True)

    sendonlevt = models.IntegerField(blank=True, null=True)
    startstationgroupid = models.IntegerField(blank=True, null=True)

    timechange = models.DateTimeField(blank=True, null=True)
    timelockgroupid = models.IntegerField(blank=True, null=True)

    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    version = models.ForeignKey(
        "Tariffversions",
        models.DO_NOTHING,
        db_column="versionid",
    )

    if not DATADUMP:
        dest_station_group = models.ForeignObject(
            StationGroup,
            models.DO_NOTHING,
            from_fields=("version", "deststationgroupid"),
            to_fields=("version", "stationgroupid"),
            related_name="dest_stationgroup_set",
        )
        device_class_group = models.ForeignObject(
            DeviceClassGroup,
            models.DO_NOTHING,
            from_fields=("version", "deviceclassgroupid"),
            to_fields=("version", "deviceclassgroupid"),
        )
        sales_station_group = models.ForeignObject(
            StationGroup,
            models.DO_NOTHING,
            from_fields=("version", "salesstationgroupid"),
            to_fields=("version", "stationgroupid"),
            related_name="sales_stationgroup_set",
        )
        start_station_group = models.ForeignObject(
            StationGroup,
            models.DO_NOTHING,
            from_fields=("version", "startstationgroupid"),
            to_fields=("version", "stationgroupid"),
            related_name="start_stationgroup_set",
        )
        timelock_group = models.ForeignObject(
            TimeLockGroup,
            models.DO_NOTHING,
            from_fields=("version", "timelockgroupid"),
            to_fields=("version", "timelockgroupid"),
        )

    class Meta:
        managed = False
        db_table = "salespackets"

    def __str__(self):
        return self.description


class SalesPacketElements(models.Model):
    pk = models.CompositePrimaryKey("version", "packetid", "packagesortcount")
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
    )
    packetid = models.IntegerField()

    packagesortcount = models.IntegerField()
    productionid = models.IntegerField(blank=True, null=True)
    packagevariable = models.IntegerField(blank=True, null=True)
    tickettypeid = models.IntegerField(blank=True, null=True)

    startstationtype = (models.IntegerField(blank=True, null=True),)
    validityid = models.IntegerField(blank=True, null=True)

    startstationid = (models.IntegerField(blank=True, null=True),)

    deststationtype = (models.IntegerField(blank=True, null=True),)
    deststationid = (models.IntegerField(blank=True, null=True),)

    quantity = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    parentsalespacketid = models.IntegerField(blank=True, null=True)
    parentpackagesortcount = models.IntegerField(blank=True, null=True)

    salesparam1 = models.IntegerField(blank=True, null=True)
    salesparam2 = models.IntegerField(blank=True, null=True)
    salesparam3 = models.IntegerField(blank=True, null=True)
    salesparam4 = models.IntegerField(blank=True, null=True)
    salesparam5 = models.IntegerField(blank=True, null=True)
    salesparam6 = models.IntegerField(blank=True, null=True)
    salesparam7 = models.IntegerField(blank=True, null=True)
    salesparam8 = models.IntegerField(blank=True, null=True)
    salesparam9 = models.CharField(max_length=50, blank=True, null=True)
    salesparam10 = models.CharField(max_length=50, blank=True, null=True)
    if not DATADUMP:
        packet = models.ForeignObject(
            SalesPackets,
            models.DO_NOTHING,
            from_fields=("version", "packetid"),
            to_fields=("version", "packetid"),
        )
        ticket_type = models.ForeignObject(
            TicketType,
            models.DO_NOTHING,
            from_fields=("version", "tickettypeid"),
            to_fields=("version", "tickettypeid"),
        )
        validity = models.ForeignObject(
            Validity,
            models.DO_NOTHING,
            from_fields=("version", "validityid"),
            to_fields=("version", "validityid"),
        )
        start_station = models.ForeignObject(
            ZoneStation,
            models.DO_NOTHING,
            from_fields=("version", "startstationid", "startstationtype"),
            to_fields=("version", "zonestationid", "type"),
            related_name="start_zonestation_set",
        )
        dest_station = models.ForeignObject(
            ZoneStation,
            models.DO_NOTHING,
            from_fields=("version", "deststationid", "deststationtype"),
            to_fields=("version", "zonestationid", "type"),
            related_name="dest_zonestation_set",
        )
        parent_package = models.ForeignObject(
            "self",
            models.DO_NOTHING,
            from_fields=("version", "parentsalespacketid", "parentpackagesortcount"),
            to_fields=("version", "packetid", "packagesortcount"),
        )

    class Meta:
        managed = False
        db_table = "salespacketelements"

    def __str__(self):
        return self.description


class SalesPacketsGroup(models.Model):
    pk = models.CompositePrimaryKey("version", "packetgroupid")
    description = models.CharField(max_length=50, blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    packetgroupid = models.IntegerField()
    packetgrouptype = models.IntegerField(blank=True, null=True)
    sortorder = models.IntegerField(blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )

    class Meta:
        managed = False
        db_table = "salespacketsgroup"

    def __str__(self):
        return self.description


class SalesPacketsGroupElements(models.Model):
    pk = models.CompositePrimaryKey("version", "packetid", "packetgroupid")
    version = models.ForeignKey(
        TariffVersions,
        models.DO_NOTHING,
        db_column="versionid",
    )
    packetid = models.IntegerField()

    packetgroupid = models.IntegerField()

    sortorder = models.IntegerField(blank=True, null=True)
    discountpercentage = models.IntegerField(blank=True, null=True)
    parameter1 = models.IntegerField(blank=True, null=True)
    parameter2 = models.IntegerField(blank=True, null=True)
    parameter3 = models.IntegerField(blank=True, null=True)
    parameter4 = models.IntegerField(blank=True, null=True)
    parameter5 = models.IntegerField(blank=True, null=True)
    parameter6 = models.IntegerField(blank=True, null=True)
    parameter7 = models.IntegerField(blank=True, null=True)
    parameter8 = models.IntegerField(blank=True, null=True)
    parameter9 = models.CharField(max_length=50, blank=True, null=True)
    parameter10 = models.CharField(max_length=50, blank=True, null=True)
    if not DATADUMP:
        packet = models.ForeignObject(
            SalesPackets,
            models.DO_NOTHING,
            from_fields=("version", "packetid"),
            to_fields=("version", "packetid"),
        )
        packet_group = models.ForeignObject(
            SalesPacketsGroup,
            models.DO_NOTHING,
            from_fields=("version", "packetgroupid"),
            to_fields=("version", "packetgroupid"),
        )

    class Meta:
        managed = False
        db_table = "salespacketsgroupelements"

    def __str__(self):
        return "SalesPacketsGroupElements: {},{},{}".format(  # noqa: UP032
            self.version,
            self.packetid,
            self.packetgroupid,
        )


class SalesShift(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid",
        "deviceid",
        "uniquemsid",
        "salesshiftno",
    )
    deviceclassid = models.IntegerField()
    uniquemsid = models.IntegerField()
    deviceid = models.IntegerField()

    salesshiftno = models.IntegerField()
    startcreadate = models.DateField(blank=True, null=True)
    vendorno = models.IntegerField(blank=True, null=True)
    modulno = models.IntegerField(blank=True, null=True)
    modulusertype = models.IntegerField(blank=True, null=True)
    shiftminuspiece = models.IntegerField(blank=True, null=True)
    shiftminusamount = models.IntegerField(blank=True, null=True)
    shiftpiece = models.IntegerField(blank=True, null=True)
    shiftoutamount = models.IntegerField(blank=True, null=True)
    vehicleno = models.IntegerField(blank=True, null=True)
    serviceno = models.IntegerField(blank=True, null=True)
    tariffversion = models.IntegerField(blank=True, null=True)

    creditamountending = models.IntegerField(blank=True, null=True)
    tarifflocationid = models.IntegerField(blank=True, null=True)
    cashless = models.IntegerField(blank=True, null=True)
    shifttype = models.IntegerField(blank=True, null=True)
    locationtype = models.IntegerField(blank=True, null=True)
    routeno = models.IntegerField(blank=True, null=True)
    creditamountstart = models.IntegerField(blank=True, null=True)
    locationid = models.IntegerField(blank=True, null=True)
    endcreadate = models.DateField(blank=True, null=True)
    tourno = models.IntegerField(blank=True, null=True)
    starteventsequno = models.IntegerField(blank=True, null=True)
    endeventsequno = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    partitioningdate = models.DateField(blank=True, null=True)
    shiftchangereasonstart = models.IntegerField(blank=True, null=True)
    shiftchangereasonend = models.IntegerField(blank=True, null=True)
    cashperiodno = models.IntegerField(blank=True, null=True)
    cashperforcemodestart = models.IntegerField(blank=True, null=True)
    cashperforcemodeend = models.IntegerField(blank=True, null=True)
    cashpertriggersstart = models.IntegerField(blank=True, null=True)
    cashpertriggersend = models.IntegerField(blank=True, null=True)
    cashperconditionstart = models.IntegerField(blank=True, null=True)
    cashperconditionend = models.IntegerField(blank=True, null=True)
    cashperlastreceiptnostart = models.IntegerField(blank=True, null=True)
    cashperlastreceiptnoend = models.IntegerField(blank=True, null=True)
    cashsubperiodnostart = models.IntegerField(blank=True, null=True)
    cashsubperiodnoend = models.IntegerField(blank=True, null=True)
    depositperiod = models.IntegerField(blank=True, null=True)
    vendorshiftno = models.IntegerField(blank=True, null=True)
    if not DATADUMP:
        main_shift = models.ForeignObject(
            MainShift,
            models.DO_NOTHING,
            from_fields=("deviceclassid", "deviceid", "uniquemsid"),
            to_fields=("deviceclassid", "deviceid", "uniquemsid"),
        )
        tariffversion = models.ForeignKey(
            "TariffVersions",
            models.DO_NOTHING,
            db_column="tariffversion",
            blank=True,
            null=True,
        )

    class Meta:
        managed = False
        db_table = "salesshift"

    def __str__(self):
        return "SalesShift: {},{},{},{}".format(  # noqa: UP032
            self.deviceclassid,
            self.deviceid,
            self.uniquemsid,
            self.salesshiftno,
        )


class SalesTransaction(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid",
        "deviceid",
        "uniquemsid",
        "salestransactionno",
    )
    abortedsale = models.BooleanField(blank=True, null=True)
    cashamount = models.IntegerField(blank=True, null=True)
    cashbookingflag = models.BooleanField(blank=True, null=True)
    cashflag = models.BooleanField(blank=True, null=True)
    cashlessflag = models.BooleanField(blank=True, null=True)
    creadate = models.DateField(blank=True, null=True)
    deviceclassid = models.IntegerField()
    deviceid = models.IntegerField()
    multipaymentflag = models.BooleanField(blank=True, null=True)
    partitioningdate = models.DateField(blank=True, null=True)
    salesshiftno = models.IntegerField()

    salestransactionno = models.IntegerField()
    snobamount = models.IntegerField(blank=True, null=True)
    snobflag = models.BooleanField(blank=True, null=True)
    testsaleflag = models.BooleanField(blank=True, null=True)
    uniquemsid = models.IntegerField()
    if not DATADUMP:
        sales_shift = models.ForeignObject(
            SalesShift,
            models.DO_NOTHING,
            from_fields=("deviceclassid", "deviceid", "uniquemsid", "salesshiftno"),
            to_fields=("deviceclassid", "deviceid", "uniquemsid", "salesshiftno"),
        )

    class Meta:
        managed = False
        db_table = "salestransaction"

    def __str__(self):
        return "SalesTransaction: {},{},{},{}".format(  # noqa: UP032
            self.deviceclassid,
            self.deviceid,
            self.uniquemsid,
            self.salestransactionno,
        )


class SalesDetail(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid",
        "deviceid",
        "uniquemsid",
        "salestransactionno",
        "salesdetailevsequno",
        "correctioncounter",
    )
    adultcount = models.IntegerField(blank=True, null=True)
    articleno = models.IntegerField(blank=True, null=True)
    articlesign = models.BooleanField(blank=True, null=True)
    branchlineid = models.IntegerField(blank=True, null=True)
    businessid = models.IntegerField(blank=True, null=True)
    cancellation = models.BooleanField(blank=True, null=True)
    cashbox = models.BooleanField(blank=True, null=True)
    childcount = models.IntegerField(blank=True, null=True)
    correctioncounter = models.IntegerField()
    correctiondate = models.DateField(blank=True, null=True)
    correctionflag = models.BooleanField()
    correctionuser = models.CharField(max_length=20, blank=True, null=True)
    creadate = models.DateField()
    customspeccard = models.BooleanField(blank=True, null=True)
    customspeccardno = models.IntegerField(blank=True, null=True)
    deststation = models.IntegerField(blank=True, null=True)
    desttype = models.IntegerField(blank=True, null=True)
    devaluation = models.BooleanField(blank=True, null=True)
    deviceclassid = models.IntegerField()
    deviceid = models.IntegerField()
    distancecategory = models.IntegerField(blank=True, null=True)
    fareoptamount = models.IntegerField(blank=True, null=True)
    fareoptvaldate = models.DateField(blank=True, null=True)
    fixedvariableprice = models.BooleanField(blank=True, null=True)
    latestorno = models.BooleanField(blank=True, null=True)
    locationtype = models.IntegerField(blank=True, null=True)
    machinebooking = models.BooleanField(blank=True, null=True)
    miscellaneous = models.BooleanField(blank=True, null=True)
    partitioningdate = models.DateField(blank=True, null=True)
    plausisign = models.BooleanField(blank=True, null=True)
    prevticketsn = models.BigIntegerField(blank=True, null=True)
    productionarticle = models.BooleanField(blank=True, null=True)
    productiondone = models.BooleanField(blank=True, null=True)
    productionunsure = models.BooleanField(blank=True, null=True)
    realstatisticarticle = models.BooleanField(blank=True, null=True)
    recoveredaftercrash = models.BooleanField(blank=True, null=True)
    refeventsequno = models.IntegerField(blank=True, null=True)
    replacementticket = models.BooleanField(blank=True, null=True)
    runreceiptno = models.IntegerField(blank=True, null=True)
    rvtrancountinprodjob = models.IntegerField(blank=True, null=True)
    salesdetailevsequno = models.IntegerField()
    salespackcount = models.IntegerField(blank=True, null=True)
    salespackid = models.IntegerField(blank=True, null=True)
    salestransactionno = models.IntegerField()
    if not DATADUMP:
        sales_transaction = models.ForeignObject(
            SalesTransaction,
            models.DO_NOTHING,
            from_fields=(
                "deviceclassid",
                "deviceid",
                "uniquemsid",
                "salestransactionno",
            ),
            to_fields=("deviceclassid", "deviceid", "uniquemsid", "salestransactionno"),
        )
    sellingrrid = models.IntegerField(blank=True, null=True)
    singlegrouptick = models.BooleanField(blank=True, null=True)
    singlesumsale = models.BooleanField(blank=True, null=True)
    sn_processed = models.FloatField(blank=True, null=True)
    soldforcompany = models.IntegerField(blank=True, null=True)
    startstation = models.IntegerField(blank=True, null=True)
    starttype = models.IntegerField(blank=True, null=True)
    tarifflocationid = models.IntegerField(blank=True, null=True)
    tariffversion = models.IntegerField(blank=True, null=True)
    tempbooking = models.BooleanField(blank=True, null=True)
    ticketserialchar = models.CharField(max_length=32, blank=True, null=True)
    ticketserialno = models.BigIntegerField(blank=True, null=True)
    ticketserialnoint64flag = models.BooleanField(blank=True, null=True)
    ticketstocktype = models.IntegerField(blank=True, null=True)
    transactsign = models.BooleanField(blank=True, null=True)
    transportother = models.BooleanField(blank=True, null=True)
    uniquemsid = models.IntegerField()
    upgrade = models.BooleanField(blank=True, null=True)
    valperiodend = models.DateField(blank=True, null=True)
    viastation = models.IntegerField(blank=True, null=True)
    viatype = models.IntegerField(blank=True, null=True)
    youthcount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "salesdetail"

    def __str__(self):
        return "SalesDetail: {},{},{},{},{},{}".format(  # noqa: UP032
            self.deviceclassid,
            self.deviceid,
            self.uniquemsid,
            self.salestransactionno,
            self.salesdetailevsequno,
            self.correctioncounter,
        )


class CashLessPayment(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid",
        "deviceid",
        "uniquemsid",
        "salestransactionno",
        "eventsequno",
    )
    deviceclassid = models.IntegerField()
    deviceid = models.IntegerField()
    eventsequno = models.IntegerField()
    uniquemsid = models.IntegerField()
    creadate = models.DateField()
    salestransactionno = models.IntegerField()

    identtype = models.IntegerField(blank=True, null=True)
    paytypecashless = models.IntegerField()
    chkvoubankid = models.CharField(max_length=24, blank=True, null=True)
    shortepan = models.CharField(max_length=4, blank=True, null=True)
    chkvounum = models.CharField(max_length=24, blank=True, null=True)
    cardidnumber = models.CharField(max_length=40, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    bookingselection = models.BooleanField(blank=True, null=True)
    bankauthno = models.CharField(max_length=12, blank=True, null=True)
    banktraceno = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=24, blank=True, null=True)
    bookingsequno = models.IntegerField(blank=True, null=True)
    expiredate = models.CharField(max_length=4, blank=True, null=True)
    authorisationdate = models.DateField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    currencyflag = models.BooleanField(blank=True, null=True)
    refundflag = models.IntegerField(blank=True, null=True)
    keyindex = models.IntegerField(blank=True, null=True)
    partitioningdate = models.DateField(blank=True, null=True)
    hashedepan = models.CharField(max_length=40, blank=True, null=True)
    if not DATADUMP:
        sales_transaction = models.ForeignObject(
            SalesTransaction,
            models.DO_NOTHING,
            from_fields=(
                "deviceclassid",
                "deviceid",
                "uniquemsid",
                "salestransactionno",
            ),
            to_fields=("deviceclassid", "deviceid", "uniquemsid", "salestransactionno"),
        )

    class Meta:
        managed = False
        db_table = "cashlesspayment"

    def __str__(self):
        return self.name


class CashPayment(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid",
        "deviceid",
        "uniquemsid",
        "salestransactionno",
        "paymenttype",
        "paymenttypeid",
        "changeflag",
    )
    changeflag = models.IntegerField()
    creadate = models.DateField()
    deviceclassid = models.IntegerField()
    deviceid = models.IntegerField()
    eventsequno = models.IntegerField()
    numberpieces = models.IntegerField(blank=True, null=True)
    partitioningdate = models.DateField(blank=True, null=True)
    paymenttype = models.IntegerField()
    paymenttypeid = models.IntegerField()
    paymenttypevalue = models.IntegerField()
    salestransactionno = models.IntegerField()

    uniquemsid = models.IntegerField()
    if not DATADUMP:
        sales_transaction = models.ForeignObject(
            SalesTransaction,
            models.DO_NOTHING,
            from_fields=(
                "deviceclassid",
                "deviceid",
                "uniquemsid",
                "salestransactionno",
            ),
            to_fields=("deviceclassid", "deviceid", "uniquemsid", "salestransactionno"),
        )

    class Meta:
        managed = False
        db_table = "cashpayment"

    def __str__(self):
        return "{},{},{},{},{},{},{}".format(  # noqa: UP032
            self.deviceclassid,
            self.deviceid,
            self.uniquemsid,
            self.salestransactionno,
            self.paymenttype,
            self.paymenttypeid,
            self.changeflag,
        )


class Relation(models.Model):
    pk = models.CompositePrimaryKey(
        "version",
        "basetickettypeid",
        "startid",
        "starttype",
        "viaid",
        "viatype",
        "destid",
        "desttype",
    )
    version = models.ForeignKey(
        "TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )
    startid = models.IntegerField()
    starttype = models.IntegerField()
    viaid = models.IntegerField()
    basetickettypeid = models.IntegerField()
    tickettypeid = models.IntegerField()
    viatype = models.IntegerField()
    validflag = models.IntegerField()
    destid = models.IntegerField()
    companyid = models.ForeignKey(
        Company,
        models.DO_NOTHING,
        db_column="companyid",
        blank=True,
        null=True,
    )
    amount = models.IntegerField(blank=True, null=True)
    distancecategoryid = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    desttype = models.IntegerField()
    multimediagroupid = models.IntegerField(blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    timenew = models.DateTimeField(blank=True, null=True)
    shortindex = models.IntegerField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateTimeField(blank=True, null=True)
    if not DATADUMP:
        start = models.ForeignObject(
            ZoneStation,
            models.DO_NOTHING,
            from_fields=("version", "startid", "starttype"),
            to_fields=("version", "zonestationid", "type"),
            related_name="relation_start_set",
        )
        base_ticket_type = models.ForeignObject(
            TicketType,
            models.DO_NOTHING,
            from_fields=("version", "basetickettypeid"),
            to_fields=("version", "tickettypeid"),
            related_name="relation_base_set",
        )
        ticket_type = models.ForeignObject(
            TicketType,
            models.DO_NOTHING,
            from_fields=("version", "tickettypeid"),
            to_fields=("version", "tickettypeid"),
            related_name="relation_tickettype_set",
        )
        via = models.ForeignObject(
            ZoneStation,
            models.DO_NOTHING,
            from_fields=("version", "viaid", "viatype"),
            to_fields=("version", "zonestationid", "type"),
            related_name="relation_via_set",
        )
        dest = models.ForeignObject(
            ZoneStation,
            models.DO_NOTHING,
            from_fields=("version", "destid", "desttype"),
            to_fields=("version", "zonestationid", "type"),
            related_name="relation_dest_set",
        )

    class Meta:
        managed = False
        db_table = "relation"

    def __str__(self):
        return self.description


class Miscellaneous(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid",
        "deviceid",
        "uniquemsid",
        "salestransactionno",
        "salesdetailevsequno",
        "correctioncounter",
    )
    deviceclassid = models.IntegerField()
    deviceid = models.IntegerField()
    uniquemsid = models.IntegerField()
    salestransactionno = models.IntegerField()
    salesdetailevsequno = models.IntegerField()

    correctioncounter = models.IntegerField()
    creadate = models.DateField()
    miscevsequno = models.IntegerField(blank=True, null=True)
    misctype = models.IntegerField(blank=True, null=True)
    correctnoticeno = models.IntegerField(blank=True, null=True)
    employeeno = models.CharField(max_length=20, blank=True, null=True)
    workdate = models.DateField(blank=True, null=True)
    salesagent = models.IntegerField(blank=True, null=True)
    locationid = models.IntegerField(blank=True, null=True)
    carunitjobno = models.IntegerField(blank=True, null=True)
    checkno = models.IntegerField(blank=True, null=True)
    tsmid = models.IntegerField(blank=True, null=True)
    monthyear = models.CharField(max_length=4, blank=True, null=True)
    bikeperopenno = models.IntegerField(blank=True, null=True)
    bikepercloseno = models.IntegerField(blank=True, null=True)
    novoidbikeper = models.IntegerField(blank=True, null=True)
    billno = models.IntegerField(blank=True, null=True)
    manufactserialno = models.BigIntegerField(blank=True, null=True)
    ticketstocktype = models.CharField(max_length=5, blank=True, null=True)
    numoftickets = models.IntegerField(blank=True, null=True)
    cashreptrno = models.IntegerField(blank=True, null=True)
    cashrepworkdate = models.DateField(blank=True, null=True)
    cashrepremdate = models.DateField(blank=True, null=True)
    cardidno = models.CharField(max_length=50, blank=True, null=True)
    partitioningdate = models.DateField(blank=True, null=True)
    if not DATADUMP:
        sales_detail = models.ForeignObject(
            SalesDetail,
            models.DO_NOTHING,
            from_fields=(
                "deviceclassid",
                "deviceid",
                "uniquemsid",
                "salestransactionno",
                "salesdetailevsequno",
                "correctioncounter",
            ),
            to_fields=(
                "deviceclassid",
                "deviceid",
                "uniquemsid",
                "salestransactionno",
                "salesdetailevsequno",
                "correctioncounter",
            ),
            related_name="miscellaneus_set",
        )

    class Meta:
        managed = False
        db_table = "miscellaneous"

    def __str__(self):
        return "Miscellaneous: {},{},{},{},{},{}".format(  # noqa: UP032
            self.deviceclassid,
            self.deviceid,
            self.uniquemsid,
            self.salestransactionno,
            self.salesdetailevsequno,
            self.correctioncounter,
        )
