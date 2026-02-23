# ruff: noqa: DJ001, DJ008, COM812, E501
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cashlesspayment(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid", "deviceid", "uniquemsid", "salestransactionno", "eventsequno"
    )
    deviceclassid = models.ForeignKey(
        "Salestransaction", models.DO_NOTHING, db_column="deviceclassid"
    )
    deviceid = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="deviceid",
        to_field="deviceid",
        related_name="cashlesspayment_deviceid_set",
    )
    eventsequno = models.IntegerField()
    uniquemsid = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="uniquemsid",
        to_field="uniquemsid",
        related_name="cashlesspayment_uniquemsid_set",
    )
    creadate = models.DateField()
    salestransactionno = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="salestransactionno",
        to_field="salestransactionno",
        related_name="cashlesspayment_salestransactionno_set",
    )
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

    class Meta:
        managed = False
        db_table = "cashlesspayment"


class Cashpayment(models.Model):
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
    deviceclassid = models.ForeignKey(
        "Salestransaction", models.DO_NOTHING, db_column="deviceclassid"
    )
    deviceid = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="deviceid",
        to_field="deviceid",
        related_name="cashpayment_deviceid_set",
    )
    eventsequno = models.IntegerField()
    numberpieces = models.IntegerField(blank=True, null=True)
    partitioningdate = models.DateField(blank=True, null=True)
    paymenttype = models.IntegerField()
    paymenttypeid = models.IntegerField()
    paymenttypevalue = models.IntegerField()
    salestransactionno = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="salestransactionno",
        to_field="salestransactionno",
        related_name="cashpayment_salestransactionno_set",
    )
    uniquemsid = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="uniquemsid",
        to_field="uniquemsid",
        related_name="cashpayment_uniquemsid_set",
    )

    class Meta:
        managed = False
        db_table = "cashpayment"


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
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    turnovertaxid = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    validflag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "company"


class Deviceclass(models.Model):
    balancegroupid = models.IntegerField(blank=True, null=True)
    description = models.CharField(unique=True, max_length=30, blank=True, null=True)
    deviceclassid = models.IntegerField(primary_key=True)
    deviceclasstype = models.IntegerField(blank=True, null=True)
    parametergroupid = models.IntegerField(blank=True, null=True)
    ruleartifactid = models.CharField(max_length=50, blank=True, null=True)
    testflag = models.BooleanField()
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
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


class Deviceclassgroup(models.Model):
    pk = models.CompositePrimaryKey("versionid", "deviceclassgroupid")
    description = models.CharField(max_length=50, blank=True, null=True)
    deviceclassgroupid = models.IntegerField()
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    versionid = models.ForeignKey(
        "Tariffversions", models.DO_NOTHING, db_column="versionid"
    )

    class Meta:
        managed = False
        db_table = "deviceclassgroup"


class Deviceclassgroupelements(models.Model):
    pk = models.CompositePrimaryKey("deviceclassgroupid", "versionid", "deviceclassid")
    deviceclassgroupid = models.ForeignKey(
        Deviceclassgroup,
        models.DO_NOTHING,
        db_column="deviceclassgroupid",
        to_field="deviceclassgroupid",
    )
    deviceclassid = models.ForeignKey(
        Deviceclass, models.DO_NOTHING, db_column="deviceclassid"
    )
    versionid = models.ForeignKey(
        Deviceclassgroup,
        models.DO_NOTHING,
        db_column="versionid",
        related_name="deviceclassgroupelements_versionid_set",
    )

    class Meta:
        managed = False
        db_table = "deviceclassgroupelements"


class Mainshift(models.Model):
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


class Mainshiftgroup(models.Model):
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


class Mainshiftgroupelements(models.Model):
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


class Miscellaneous(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid",
        "deviceid",
        "uniquemsid",
        "salestransactionno",
        "salesdetailevsequno",
        "correctioncounter",
    )
    deviceclassid = models.ForeignKey(
        "Salesdetail", models.DO_NOTHING, db_column="deviceclassid"
    )
    deviceid = models.ForeignKey(
        "Salesdetail",
        models.DO_NOTHING,
        db_column="deviceid",
        to_field="deviceid",
        related_name="miscellaneous_deviceid_set",
    )
    uniquemsid = models.ForeignKey(
        "Salesdetail",
        models.DO_NOTHING,
        db_column="uniquemsid",
        to_field="uniquemsid",
        related_name="miscellaneous_uniquemsid_set",
    )
    salestransactionno = models.ForeignKey(
        "Salesdetail",
        models.DO_NOTHING,
        db_column="salestransactionno",
        to_field="salestransactionno",
        related_name="miscellaneous_salestransactionno_set",
    )
    salesdetailevsequno = models.ForeignKey(
        "Salesdetail",
        models.DO_NOTHING,
        db_column="salesdetailevsequno",
        to_field="salesdetailevsequno",
        related_name="miscellaneous_salesdetailevsequno_set",
    )
    correctioncounter = models.ForeignKey(
        "Salesdetail",
        models.DO_NOTHING,
        db_column="correctioncounter",
        to_field="correctioncounter",
        related_name="miscellaneous_correctioncounter_set",
    )
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

    class Meta:
        managed = False
        db_table = "miscellaneous"


class Relation(models.Model):
    pk = models.CompositePrimaryKey(
        "versionid",
        "basetickettypeid",
        "startid",
        "starttype",
        "viaid",
        "viatype",
        "destid",
        "desttype",
    )
    versionid = models.ForeignKey(
        "Zonestation", models.DO_NOTHING, db_column="versionid"
    )
    startid = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="startid",
        to_field="zonestationid",
        related_name="relation_startid_set",
    )
    starttype = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="starttype",
        to_field="type",
        related_name="relation_starttype_set",
    )
    viaid = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="viaid",
        to_field="zonestationid",
        related_name="relation_viaid_set",
    )
    basetickettypeid = models.ForeignKey(
        "Tickettype",
        models.DO_NOTHING,
        db_column="basetickettypeid",
        to_field="tickettypeid",
    )
    tickettypeid = models.ForeignKey(
        "Tickettype",
        models.DO_NOTHING,
        db_column="tickettypeid",
        to_field="tickettypeid",
        related_name="relation_tickettypeid_set",
    )
    viatype = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="viatype",
        to_field="type",
        related_name="relation_viatype_set",
    )
    validflag = models.IntegerField()
    destid = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="destid",
        to_field="zonestationid",
        related_name="relation_destid_set",
    )
    companyid = models.ForeignKey(
        Company, models.DO_NOTHING, db_column="companyid", blank=True, null=True
    )
    amount = models.IntegerField(blank=True, null=True)
    distancecategoryid = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    desttype = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="desttype",
        to_field="type",
        related_name="relation_desttype_set",
    )
    multimediagroupid = models.IntegerField(blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    shortindex = models.IntegerField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "relation"


class Routes(models.Model):
    versionid = models.IntegerField(blank=True, null=True)
    routeid = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateField(blank=True, null=True)
    simfotoid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "routes"


class Salesdetail(models.Model):
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
    deviceclassid = models.ForeignKey(
        "Salestransaction", models.DO_NOTHING, db_column="deviceclassid"
    )
    deviceid = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="deviceid",
        to_field="deviceid",
        related_name="salesdetail_deviceid_set",
    )
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
    salestransactionno = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="salestransactionno",
        to_field="salestransactionno",
        related_name="salesdetail_salestransactionno_set",
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
    uniquemsid = models.ForeignKey(
        "Salestransaction",
        models.DO_NOTHING,
        db_column="uniquemsid",
        to_field="uniquemsid",
        related_name="salesdetail_uniquemsid_set",
    )
    upgrade = models.BooleanField(blank=True, null=True)
    valperiodend = models.DateField(blank=True, null=True)
    viastation = models.IntegerField(blank=True, null=True)
    viatype = models.IntegerField(blank=True, null=True)
    youthcount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "salesdetail"


class Salespacketelements(models.Model):
    pk = models.CompositePrimaryKey("versionid", "packetid", "packagesortcount")
    versionid = models.ForeignKey("Validity", models.DO_NOTHING, db_column="versionid")
    packetid = models.ForeignKey(
        "Salespackets", models.DO_NOTHING, db_column="packetid", to_field="packetid"
    )
    packagesortcount = models.IntegerField()
    productionid = models.IntegerField(blank=True, null=True)
    packagevariable = models.IntegerField(blank=True, null=True)
    tickettypeid = models.ForeignKey(
        "Tickettype",
        models.DO_NOTHING,
        db_column="tickettypeid",
        to_field="tickettypeid",
        blank=True,
        null=True,
    )
    startstationtype = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="startstationtype",
        to_field="type",
        blank=True,
        null=True,
    )
    validityid = models.ForeignKey(
        "Validity",
        models.DO_NOTHING,
        db_column="validityid",
        to_field="validityid",
        related_name="salespacketelements_validityid_set",
        blank=True,
        null=True,
    )
    startstationid = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="startstationid",
        to_field="zonestationid",
        related_name="salespacketelements_startstationid_set",
        blank=True,
        null=True,
    )
    deststationtype = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="deststationtype",
        to_field="type",
        related_name="salespacketelements_deststationtype_set",
        blank=True,
        null=True,
    )
    deststationid = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="deststationid",
        to_field="zonestationid",
        related_name="salespacketelements_deststationid_set",
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    parentsalespacketid = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="parentsalespacketid",
        to_field="packetid",
        blank=True,
        null=True,
    )
    usernew = models.CharField(max_length=20, blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateField(blank=True, null=True)
    parentpackagesortcount = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="parentpackagesortcount",
        to_field="packagesortcount",
        related_name="salespacketelements_parentpackagesortcount_set",
        blank=True,
        null=True,
    )
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

    class Meta:
        managed = False
        db_table = "salespacketelements"


class Salespackets(models.Model):
    pk = models.CompositePrimaryKey("versionid", "packetid")
    description = models.CharField(max_length=50, blank=True, null=True)
    deststationgroupid = models.ForeignKey(
        "Stationgroup",
        models.DO_NOTHING,
        db_column="deststationgroupid",
        to_field="stationgroupid",
        blank=True,
        null=True,
    )
    deviceclassgroupid = models.ForeignKey(
        Deviceclassgroup,
        models.DO_NOTHING,
        db_column="deviceclassgroupid",
        to_field="deviceclassgroupid",
        blank=True,
        null=True,
    )
    externalid = models.CharField(max_length=20, blank=True, null=True)
    groupfareid = models.IntegerField(blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    packetid = models.IntegerField()
    packettype = models.IntegerField(blank=True, null=True)
    payacceptgroupid = models.IntegerField(blank=True, null=True)
    plusgroupid = models.IntegerField(blank=True, null=True)
    salesstationgroupid = models.ForeignKey(
        "Stationgroup",
        models.DO_NOTHING,
        db_column="salesstationgroupid",
        to_field="stationgroupid",
        related_name="salespackets_salesstationgroupid_set",
        blank=True,
        null=True,
    )
    sendonlevt = models.IntegerField(blank=True, null=True)
    startstationgroupid = models.ForeignKey(
        "Stationgroup",
        models.DO_NOTHING,
        db_column="startstationgroupid",
        to_field="stationgroupid",
        related_name="salespackets_startstationgroupid_set",
        blank=True,
        null=True,
    )
    timechange = models.DateField(blank=True, null=True)
    timelockgroupid = models.ForeignKey(
        "Timelockgroup",
        models.DO_NOTHING,
        db_column="timelockgroupid",
        to_field="timelockgroupid",
        blank=True,
        null=True,
    )
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    versionid = models.ForeignKey(
        "Tariffversions", models.DO_NOTHING, db_column="versionid"
    )

    class Meta:
        managed = False
        db_table = "salespackets"


class Salespacketsgroup(models.Model):
    pk = models.CompositePrimaryKey("versionid", "packetgroupid")
    description = models.CharField(max_length=50, blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    packetgroupid = models.IntegerField()
    packetgrouptype = models.IntegerField(blank=True, null=True)
    sortorder = models.IntegerField(blank=True, null=True)
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    versionid = models.ForeignKey(
        "Tariffversions", models.DO_NOTHING, db_column="versionid"
    )

    class Meta:
        managed = False
        db_table = "salespacketsgroup"


class Salespacketsgroupelements(models.Model):
    pk = models.CompositePrimaryKey("versionid", "packetid", "packetgroupid")
    versionid = models.ForeignKey(
        Salespackets, models.DO_NOTHING, db_column="versionid"
    )
    packetid = models.ForeignKey(
        Salespackets,
        models.DO_NOTHING,
        db_column="packetid",
        to_field="packetid",
        related_name="salespacketsgroupelements_packetid_set",
    )
    packetgroupid = models.ForeignKey(
        Salespacketsgroup,
        models.DO_NOTHING,
        db_column="packetgroupid",
        to_field="packetgroupid",
    )
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

    class Meta:
        managed = False
        db_table = "salespacketsgroupelements"


class Salesshift(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid", "deviceid", "uniquemsid", "salesshiftno"
    )
    deviceclassid = models.ForeignKey(
        Mainshift, models.DO_NOTHING, db_column="deviceclassid"
    )
    uniquemsid = models.ForeignKey(
        Mainshift,
        models.DO_NOTHING,
        db_column="uniquemsid",
        to_field="uniquemsid",
        related_name="salesshift_uniquemsid_set",
    )
    deviceid = models.ForeignKey(
        Mainshift,
        models.DO_NOTHING,
        db_column="deviceid",
        to_field="deviceid",
        related_name="salesshift_deviceid_set",
    )
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

    class Meta:
        managed = False
        db_table = "salesshift"


class Salestransaction(models.Model):
    pk = models.CompositePrimaryKey(
        "deviceclassid", "deviceid", "uniquemsid", "salestransactionno"
    )
    abortedsale = models.BooleanField(blank=True, null=True)
    cashamount = models.IntegerField(blank=True, null=True)
    cashbookingflag = models.BooleanField(blank=True, null=True)
    cashflag = models.BooleanField(blank=True, null=True)
    cashlessflag = models.BooleanField(blank=True, null=True)
    creadate = models.DateField(blank=True, null=True)
    deviceclassid = models.ForeignKey(
        Salesshift, models.DO_NOTHING, db_column="deviceclassid"
    )
    deviceid = models.ForeignKey(
        Salesshift,
        models.DO_NOTHING,
        db_column="deviceid",
        to_field="deviceid",
        related_name="salestransaction_deviceid_set",
    )
    multipaymentflag = models.BooleanField(blank=True, null=True)
    partitioningdate = models.DateField(blank=True, null=True)
    salesshiftno = models.ForeignKey(
        Salesshift,
        models.DO_NOTHING,
        db_column="salesshiftno",
        to_field="salesshiftno",
        related_name="salestransaction_salesshiftno_set",
    )
    salestransactionno = models.IntegerField()
    snobamount = models.IntegerField(blank=True, null=True)
    snobflag = models.BooleanField(blank=True, null=True)
    testsaleflag = models.BooleanField(blank=True, null=True)
    uniquemsid = models.ForeignKey(
        Salesshift,
        models.DO_NOTHING,
        db_column="uniquemsid",
        to_field="uniquemsid",
        related_name="salestransaction_uniquemsid_set",
    )

    class Meta:
        managed = False
        db_table = "salestransaction"


class Stationgroup(models.Model):
    pk = models.CompositePrimaryKey("versionid", "stationgroupid")
    description = models.CharField(max_length=50, blank=True, null=True)
    grouptype = models.IntegerField(blank=True, null=True)
    stationgroupid = models.IntegerField()
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    versionid = models.ForeignKey(
        "Tariffversions", models.DO_NOTHING, db_column="versionid"
    )

    class Meta:
        managed = False
        db_table = "stationgroup"


class Stationgroupelements(models.Model):
    pk = models.CompositePrimaryKey(
        "versionid", "stationtype", "stationid", "stationgroupid"
    )
    versionid = models.ForeignKey(
        Stationgroup, models.DO_NOTHING, db_column="versionid"
    )
    stationtype = models.ForeignKey(
        "Zonestation", models.DO_NOTHING, db_column="stationtype", to_field="type"
    )
    stationid = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="stationid",
        to_field="zonestationid",
        related_name="stationgroupelements_stationid_set",
    )
    stationgroupid = models.ForeignKey(
        Stationgroup,
        models.DO_NOTHING,
        db_column="stationgroupid",
        to_field="stationgroupid",
        related_name="stationgroupelements_stationgroupid_set",
    )

    class Meta:
        managed = False
        db_table = "stationgroupelements"


class Stationrouteelements(models.Model):
    pk = models.CompositePrimaryKey("versionid", "stationid", "stationtype", "routeid")
    versionid = models.ForeignKey(
        "Zonestation", models.DO_NOTHING, db_column="versionid"
    )
    stationid = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="stationid",
        to_field="zonestationid",
        related_name="stationrouteelements_stationid_set",
    )
    routeid = models.ForeignKey(Routes, models.DO_NOTHING, db_column="routeid")
    stationtype = models.ForeignKey(
        "Zonestation",
        models.DO_NOTHING,
        db_column="stationtype",
        to_field="type",
        related_name="stationrouteelements_stationtype_set",
    )
    stationindex = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stationrouteelements"


class Tariffversions(models.Model):
    description = models.CharField(max_length=50, blank=True, null=True)
    railroadid = models.ForeignKey(
        Company, models.DO_NOTHING, db_column="railroadid", blank=True, null=True
    )
    status = models.IntegerField(blank=True, null=True)
    theovertakerflag = models.BooleanField()
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    validityendtime = models.DateField(blank=True, null=True)
    validitystarttime = models.DateField(blank=True, null=True)
    versionid = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "tariffversions"


class Tickettype(models.Model):
    pk = models.CompositePrimaryKey("versionid", "tickettypeid")
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
        Company, models.DO_NOTHING, db_column="serviceproviderid", blank=True, null=True
    )
    statetaxid = models.IntegerField(blank=True, null=True)
    summary = models.IntegerField(blank=True, null=True)
    ticketembgroupid = models.IntegerField(blank=True, null=True)
    tickettypeid = models.IntegerField()
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    validityid = models.ForeignKey(
        "Validity",
        models.DO_NOTHING,
        db_column="validityid",
        to_field="validityid",
        blank=True,
        null=True,
    )
    versionid = models.ForeignKey(
        "Validity",
        models.DO_NOTHING,
        db_column="versionid",
        related_name="tickettype_versionid_set",
    )

    class Meta:
        managed = False
        db_table = "tickettype"


class Tickettypegroup(models.Model):
    pk = models.CompositePrimaryKey(
        "versionid", "tickettypegroupid", "tickettypegrouptype"
    )
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    tickettypegroupid = models.IntegerField()
    tickettypegrouptype = models.IntegerField()
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    versionid = models.ForeignKey(
        Tariffversions, models.DO_NOTHING, db_column="versionid"
    )

    class Meta:
        managed = False
        db_table = "tickettypegroup"


class Tickettypegroupelements(models.Model):
    pk = models.CompositePrimaryKey(
        "versionid", "tickettypeid", "tickettypegrouptype", "tickettypegroupid"
    )
    versionid = models.ForeignKey(Tickettype, models.DO_NOTHING, db_column="versionid")
    tickettypegroupid = models.ForeignKey(
        Tickettypegroup,
        models.DO_NOTHING,
        db_column="tickettypegroupid",
        to_field="tickettypegroupid",
    )
    tickettypeid = models.ForeignKey(
        Tickettype,
        models.DO_NOTHING,
        db_column="tickettypeid",
        to_field="tickettypeid",
        related_name="tickettypegroupelements_tickettypeid_set",
    )
    tickettypegrouptype = models.ForeignKey(
        Tickettypegroup,
        models.DO_NOTHING,
        db_column="tickettypegrouptype",
        to_field="tickettypegrouptype",
        related_name="tickettypegroupelements_tickettypegrouptype_set",
    )

    class Meta:
        managed = False
        db_table = "tickettypegroupelements"


class Timelock(models.Model):
    pk = models.CompositePrimaryKey("versionid", "timelockid", "deviceclassgroupid")
    versionid = models.ForeignKey(
        Tariffversions, models.DO_NOTHING, db_column="versionid"
    )
    timelockid = models.IntegerField()
    deviceclassgroupid = models.ForeignKey(
        Deviceclassgroup,
        models.DO_NOTHING,
        db_column="deviceclassgroupid",
        to_field="deviceclassgroupid",
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
    timenew = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    timechange = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "timelock"


class Timelockgroup(models.Model):
    pk = models.CompositePrimaryKey("versionid", "timelockgroupid")
    description = models.CharField(max_length=50, blank=True, null=True)
    lockflag = models.IntegerField(blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    timechange = models.DateField(blank=True, null=True)
    timelock = models.IntegerField(blank=True, null=True)
    timelockgroupid = models.IntegerField()
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    versionid = models.ForeignKey(
        Tariffversions, models.DO_NOTHING, db_column="versionid"
    )

    class Meta:
        managed = False
        db_table = "timelockgroup"


class Timelockgroupelements(models.Model):
    pk = models.CompositePrimaryKey(
        "versionid", "timelockgroupid", "timelockid", "deviceclassgroupid"
    )
    versionid = models.ForeignKey(Timelock, models.DO_NOTHING, db_column="versionid")
    deviceclassgroupid = models.ForeignKey(
        Timelock,
        models.DO_NOTHING,
        db_column="deviceclassgroupid",
        to_field="deviceclassgroupid",
        related_name="timelockgroupelements_deviceclassgroupid_set",
    )
    timelockgroupid = models.ForeignKey(
        Timelockgroup,
        models.DO_NOTHING,
        db_column="timelockgroupid",
        to_field="timelockgroupid",
    )
    timelockid = models.ForeignKey(
        Timelock,
        models.DO_NOTHING,
        db_column="timelockid",
        to_field="timelockid",
        related_name="timelockgroupelements_timelockid_set",
    )

    class Meta:
        managed = False
        db_table = "timelockgroupelements"


class Tvmstation(models.Model):
    companyid = models.ForeignKey(
        Company, models.DO_NOTHING, db_column="companyid", blank=True, null=True
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
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    town = models.CharField(max_length=20, blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "tvmstation"


class Validity(models.Model):
    pk = models.CompositePrimaryKey("versionid", "validityid")
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
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    validityid = models.IntegerField()
    validitytype = models.IntegerField(blank=True, null=True)
    versionid = models.ForeignKey(
        Tariffversions, models.DO_NOTHING, db_column="versionid"
    )

    class Meta:
        managed = False
        db_table = "validity"


class Zonestation(models.Model):
    pk = models.CompositePrimaryKey("versionid", "zonestationid", "type")
    description = models.CharField(max_length=50, blank=True, null=True)
    externalid = models.CharField(max_length=20, blank=True, null=True)
    multimediagroupid = models.IntegerField(blank=True, null=True)
    parameter1 = models.IntegerField(blank=True, null=True)
    parameter10 = models.IntegerField(blank=True, null=True)
    parameter11 = models.CharField(max_length=50, blank=True, null=True)
    parameter2 = models.IntegerField(blank=True, null=True)
    parameter3 = models.IntegerField(blank=True, null=True)
    parameter4 = models.IntegerField(blank=True, null=True)
    parameter5 = models.IntegerField(blank=True, null=True)
    parameter6 = models.IntegerField(blank=True, null=True)
    parameter7 = models.IntegerField(blank=True, null=True)
    parameter8 = models.IntegerField(blank=True, null=True)
    parameter9 = models.IntegerField(blank=True, null=True)
    timechange = models.DateField(blank=True, null=True)
    timenew = models.DateField(blank=True, null=True)
    type = models.IntegerField()
    typezone = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="typezone",
        to_field="type",
        blank=True,
        null=True,
    )
    userchange = models.CharField(max_length=20, blank=True, null=True)
    usernew = models.CharField(max_length=20, blank=True, null=True)
    versionid = models.ForeignKey(
        Tariffversions, models.DO_NOTHING, db_column="versionid"
    )
    zoneid = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="zoneid",
        to_field="zonestationid",
        related_name="zonestation_zoneid_set",
        blank=True,
        null=True,
    )
    zonestationid = models.IntegerField()

    class Meta:
        managed = False
        db_table = "zonestation"
