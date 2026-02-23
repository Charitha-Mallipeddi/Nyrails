from django.db import models

from core.contrib.db.constraints import ForeignReferencesConstraint
from core.general.model_types import ZoneStationType
from core.revenue import model_types


# Create your models here.
class MainShift(models.Model):
    """Table with entries for mainshift open and close"""

    pk = models.CompositePrimaryKey("device_class", "device_id", "unique_ms_id")
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.CASCADE,
        db_column="deviceclassid",
        help_text="unique identifier of DeviceClass",
    )
    device_id = models.IntegerField(
        db_column="deviceid", help_text="unique identifier for TVM"
    )
    unique_ms_id = models.IntegerField(
        db_column="uniquemsid",
        help_text="Unique Main Shift ID, this ID is unique for each Device, it is "
        "steadily incremented, even if Device is set back (047'er)",
    )
    main_shift_no = models.IntegerField(
        db_column="mainshiftno", help_text="Main shift number"
    )
    start_crea_date = models.DateField(
        db_column="startcreadate",
        help_text="Date and time of creation of mainshift start",
    )
    start_event_sequ_no = models.IntegerField(
        db_column="starteventsequno",
        blank=True,
        null=True,
        help_text="Event sequence number of mainshift start",
    )
    end_crea_date = models.DateField(
        db_column="endcreadate",
        blank=True,
        null=True,
        help_text="Date and time of creation of mainshift end",
    )
    poll_date = models.DateField(
        db_column="polldate",
        blank=True,
        null=True,
        help_text="timestamp of uploaded SVN file",
    )
    end_event_sequ_no = models.IntegerField(
        db_column="endeventsequno",
        blank=True,
        null=True,
        help_text="Event sequence number of mainshift end",
    )
    proceeding_type = models.IntegerField(
        db_column="proceedingtype",
        blank=True,
        null=True,
        help_text="Type of proceeding",
    )
    db_write_cmd_date = models.DateField(
        db_column="dbwritecmddate",
        blank=True,
        null=True,
        help_text="timestamp of command to DBWrite process",
    )
    vendor_no = models.IntegerField(
        db_column="vendorno", blank=True, null=True, help_text="Number of vendor"
    )
    modul_no = models.IntegerField(
        db_column="modulno", blank=True, null=True, help_text="Module number"
    )
    vehicle_no = models.IntegerField(db_column="vehicleno", blank=True, null=True)
    modul_user_type = models.IntegerField(
        db_column="modulusertype", blank=True, null=True, help_text="Module user type"
    )
    shift_minus_piece = models.IntegerField(
        db_column="shiftminuspiece",
        blank=True,
        null=True,
        help_text="Shift sum minus amount",
    )
    service_no = models.IntegerField(db_column="serviceno", blank=True, null=True)
    tariff_version = models.ForeignKey(
        "general.TariffVersions",
        on_delete=models.SET_NULL,
        null=True,
        db_column="tariffversion",
        related_name="main_shifts",
    )
    shift_minus_amount = models.IntegerField(
        db_column="shiftminusamount", blank=True, null=True
    )
    tariff_location_id = models.IntegerField(
        db_column="tarifflocationid",
        blank=True,
        null=True,
        help_text="(TariffVersion, TariffLocationID, LocationType) is reference to "
        "table ZoneStation. This is the tariff location at main shift start.",
    )

    route_no = models.ForeignKey(
        "general.Routes",
        on_delete=models.SET_NULL,
        null=True,
        db_column="routeno",
        related_name="main_shifts",
    )

    shift_type = models.IntegerField(
        db_column="shifttype",
        blank=True,
        null=True,
        choices=model_types.ShiftTypes,
        help_text="Shift type differs between a manual shift opened by a sales clerk "
        "or machine shifts opened by the device. A TVM always generates machine shifts",
    )
    location_type = models.IntegerField(
        db_column="locationtype",
        blank=True,
        null=True,
        help_text="see TariffLocationID",
    )
    location_id = models.IntegerField(
        db_column="locationid",
        blank=True,
        null=True,
        help_text="reference to TvmStation.StationID, this is the physical station at "
        "main shift start",
    )
    sellingrrid = models.IntegerField(db_column="sellingrrid", blank=True, null=True)
    shift_piece = models.IntegerField(
        db_column="shiftpiece", blank=True, null=True, help_text="Shift sum pieces"
    )
    tour_no = models.IntegerField(db_column="tourno", blank=True, null=True)
    shift_out_amount = models.IntegerField(
        db_column="shiftoutamount",
        blank=True,
        null=True,
        help_text="Shift sum output amount",
    )
    cashless = models.IntegerField(db_column="cashless", blank=True, null=True)
    credit_amount = models.IntegerField(
        db_column="creditamount",
        blank=True,
        null=True,
        help_text="Amount of credit (Haben-Betrag)",
    )
    last_salesshift_no = models.IntegerField(
        db_column="lastsalesshiftno",
        blank=True,
        null=True,
        help_text="Number of last sales shift in actual mainshift",
    )
    mainshift_close_status = models.IntegerField(
        db_column="mainshiftclosestatus",
        blank=True,
        null=True,
        help_text="Close status of mainshift 0 - main shift closed, 1 - close of not "
        "existing mainshift close",
    )
    job_id = models.CharField(
        db_column="jobid",
        max_length=24,
        blank=True,
        help_text="Job ID unique ID to identify a job that is processed on more than "
        "one machine, this job ID is a combined information of device-no. and system "
        "time/date of the creating device (10 digits for time/Date in seconds and 10 "
        "digits for the TSM ID, in this case no DeviceClassID is necessary because "
        "JobID's only used for TOM), for LIRR/MNR the JOB-ID is equal to the "
        "MULTI-TOUR-ID",
    )
    job_sequ_id = models.IntegerField(
        db_column="jobsequid",
        blank=True,
        null=True,
        help_text="this number defines the actual position of a part of a job in a "
        "complete job, defined by JOB-ID; for LIRR/MNR the sequence no. is equal to "
        "the actual MINI-TOUR-NO. in a MULTI-TOUR",
    )
    bank_code = models.BigIntegerField(
        db_column="bankcode",
        blank=True,
        null=True,
        help_text="each shift can be assigned to a special account, "
        "if DeviceClassType = 1, then BankCode and BankAccount are always taken from "
        "TvmTable, each shift can be assigned to a special account, "
        "if DeviceClassType = 2, then BankCode and BankAccount can be taken from table "
        "UserData (to configure in device application), "
        "but usually like (DeviceClassType = 1)",
    )
    bank_account = models.BigIntegerField(
        db_column="bankaccount",
        blank=True,
        null=True,
        help_text="each shift can be assigned to a special account, "
        "if DeviceClassType = 1, then BankCode and BankAccount are taken from "
        "TvmTable, each shift can be assigned to a special account, "
        "if DeviceClassType = 2, then BankCode and BankAccount are "
        "taken from table UserData",
    )
    audit_status = models.IntegerField(
        db_column="auditstatus",
        blank=True,
        null=True,
        choices=model_types.AuditStatuses,
        help_text="The States 1,2 and 5 are set automatically by report RA24 is "
        "executed. The states 3 and 4 will only be set manually.",
    )
    insert_date = models.DateField(db_column="insertdate", blank=True, null=True)
    test_flag = models.BooleanField(
        db_column="testflag", help_text="test shift (to exclude from sales reports)"
    )
    auditor_system_id = models.CharField(
        db_column="auditorsystemid",
        max_length=20,
        blank=True,
        help_text="identification name of the user "
        'this is the real "user name" of the user',
    )
    status_date_time = models.DateField(
        db_column="statusdatetime",
        blank=True,
        null=True,
        help_text="timestamp of receivment of the tour envelop",
    )
    job_state = models.IntegerField(
        db_column="jobstate", blank=True, null=True, choices=model_types.JobStates
    )
    sold_currency = models.IntegerField(db_column="soldcurrency", blank=True, null=True)
    currency = models.IntegerField(db_column="currency", blank=True, null=True)
    shift_change_reason_start = models.IntegerField(
        db_column="shiftchangereasonstart",
        blank=True,
        null=True,
        choices=model_types.ShiftChangeReasons,
    )
    shift_change_reason_end = models.IntegerField(
        db_column="shiftchangereasonend",
        blank=True,
        null=True,
        choices=model_types.ShiftChangeReasons,
    )
    sb_serial_number = models.IntegerField(
        db_column="sbserialnumber", blank=True, null=True
    )
    base_plate_id = models.CharField(db_column="baseplateid", max_length=12, blank=True)
    sold_for_company = models.IntegerField(
        db_column="soldforcompany",
        blank=True,
        null=True,
        help_text="Reference sales to company",
    )

    class Meta:
        db_table = "mainshift"
        unique_together = (
            (
                "device_class",
                "device_id",
                "start_crea_date",
                "end_crea_date",
                "main_shift_no",
            ),
        )

    def __str__(self):
        return "MainShift: {},{},{}".format(  # noqa: UP032
            self.device_class,
            self.device_id,
            self.unique_ms_id,
        )


class MainShiftGroup(models.Model):
    """Store user defined mainshift groups for completeness and order validation."""

    pk = models.CompositePrimaryKey("device_class", "device_id", "group_id")
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.CASCADE,
        db_column="deviceclassid",
        help_text="unique identifier of DeviceClass",
    )
    group_id = models.IntegerField(db_column="groupid")
    start_crea_date = models.DateField(db_column="startcreadate", blank=True, null=True)
    end_crea_date = models.DateField(db_column="endcreadate", blank=True, null=True)
    start_event_sequ_no = models.IntegerField(
        db_column="starteventsequno", blank=True, null=True
    )
    end_event_sequ_no = models.IntegerField(
        db_column="endeventsequno", blank=True, null=True
    )
    start_main_shift_no = models.IntegerField(
        db_column="startmainshiftno", blank=True, null=True
    )
    end_main_shift_no = models.IntegerField(
        db_column="endmainshiftno", blank=True, null=True
    )
    start_unique_ms_id = models.IntegerField(
        db_column="startuniquemsid", blank=True, null=True
    )
    end_unique_ms_id = models.IntegerField(
        db_column="enduniquemsid", blank=True, null=True
    )
    flag_is_basegroup = models.BooleanField(
        db_column="flag_isbasegroup",
        blank=True,
        null=True,
        choices=model_types.ShiftIsBaseGroup,
    )
    user_is_basegroup = models.CharField(
        db_column="user_isbasegroup",
        max_length=50,
        blank=True,
        help_text="This user defined this group as a base group.",
    )
    time_is_basegroup = models.DateField(
        db_column="time_isbasegroup",
        blank=True,
        null=True,
        help_text="Time of definition.",
    )
    device_id = models.IntegerField(
        db_column="deviceid", help_text="Unique Tvm ID 1-999999"
    )

    class Meta:
        db_table = "mainshiftgroup"

    def __str__(self):
        return "MainShiftGroup: {},{},{}".format(  # noqa: UP032
            self.device_class,
            self.device_id,
            self.group_id,
        )


class MainShiftGroupElements(models.Model):
    """
    Store mainshifts of user defined mainshift groups for completeness
    and order test purposes.
    """

    pk = models.CompositePrimaryKey("device_class", "device_id", "unique_ms_id")
    db_write_cmd_date = models.DateField(
        db_column="dbwritecmddate", blank=True, null=True
    )
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.CASCADE,
        db_column="deviceclassid",
        help_text="unique identifier of DeviceClass",
    )
    device_id = models.IntegerField(
        db_column="deviceid", help_text="Unique Tvm ID 1-999999"
    )
    end_crea_date = models.DateField(db_column="endcreadate", blank=True, null=True)
    end_event_sequ_no = models.IntegerField(
        db_column="endeventsequno", blank=True, null=True
    )
    group_id = models.IntegerField(db_column="groupid", blank=True, null=True)
    insert_date = models.DateField(db_column="insertdate", blank=True, null=True)
    main_shift_no = models.IntegerField(db_column="mainshiftno", blank=True, null=True)
    position = models.IntegerField(db_column="position", blank=True, null=True)
    start_crea_date = models.DateField(db_column="startcreadate", blank=True, null=True)
    start_event_sequ_no = models.IntegerField(
        db_column="starteventsequno", blank=True, null=True
    )
    unique_ms_id = models.IntegerField(db_column="uniquemsid")

    class Meta:
        db_table = "mainshiftgroupelements"

    def __str__(self):
        return "MainShiftGroupElements: {},{},{}".format(  # noqa: UP032
            self.device_class,
            self.device_id,
            self.unique_ms_id,
        )


class SalesShift(models.Model):
    """Table with entries for base SalesShift no"""

    pk = models.CompositePrimaryKey(
        "device_class",
        "device_id",
        "unique_ms_id",
        "sales_shift_no",
    )
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.CASCADE,
        db_column="deviceclassid",
        help_text="unique identifier of DeviceClass",
    )
    unique_ms_id = models.IntegerField(
        db_column="uniquemsid",
        help_text="Unique Main Shift ID, this ID is unique for each Device, "
        "it is steadily incremented, even if Device is set back (047'er)",
    )
    device_id = models.IntegerField(
        db_column="deviceid", help_text="Unique Tvm ID 1-999999"
    )
    sales_shift_no = models.IntegerField(
        db_column="salesshiftno", help_text="Number of sales shift"
    )
    start_crea_date = models.DateField(
        db_column="startcreadate",
        blank=True,
        null=True,
        help_text="Date and time of creation of salesshift",
    )
    vendor_no = models.IntegerField(db_column="vendorno", blank=True, null=True)
    modul_no = models.IntegerField(
        db_column="modulno",
        blank=True,
        null=True,
        help_text="Current module number which was used to open the main shift.",
    )
    modul_user_type = models.IntegerField(
        db_column="modulusertype", blank=True, null=True
    )
    shift_minus_piece = models.IntegerField(
        db_column="shiftminuspiece", blank=True, null=True
    )
    shift_minus_amount = models.IntegerField(
        db_column="shiftminusamount", blank=True, null=True
    )
    shift_piece = models.IntegerField(db_column="shiftpiece", blank=True, null=True)
    shift_out_amount = models.IntegerField(
        db_column="shiftoutamount", blank=True, null=True
    )
    vehicle_no = models.IntegerField(db_column="vehicleno", blank=True, null=True)
    service_no = models.IntegerField(db_column="serviceno", blank=True, null=True)

    credit_amount_ending = models.IntegerField(
        db_column="creditamountending", blank=True, null=True
    )
    tariff_location_id = models.IntegerField(
        db_column="tarifflocationid",
        blank=True,
        null=True,
        help_text="(TariffVersion, TariffLocationID, LocationType) is reference to "
        "table ZoneStation. This is the tariff location at main shift start.",
    )
    cashless = models.IntegerField(db_column="cashless", blank=True, null=True)
    shift_type = models.IntegerField(
        db_column="shifttype",
        blank=True,
        null=True,
        choices=model_types.SalesShiftTypes,
        help_text="Shift type differs between a manual shift opened by a sales clerk "
        "or machine shifts opened by the device. A TVM always generates machine shifts",
    )
    location_type = models.IntegerField(
        db_column="locationtype",
        blank=True,
        null=True,
        help_text="see TariffLocationID",
    )
    route_no = models.IntegerField(db_column="routeno", blank=True, null=True)
    credit_amount_start = models.IntegerField(
        db_column="creditamountstart", blank=True, null=True
    )
    location_id = models.IntegerField(
        db_column="locationid",
        blank=True,
        null=True,
        help_text="reference to TvmStation.StationID, this is the physical station "
        "at main shift start",
    )
    end_crea_date = models.DateField(db_column="endcreadate", blank=True, null=True)
    tour_no = models.IntegerField(db_column="tourno", blank=True, null=True)
    start_event_sequ_no = models.IntegerField(
        db_column="starteventsequno", blank=True, null=True
    )
    end_event_sequ_no = models.IntegerField(
        db_column="endeventsequno", blank=True, null=True
    )
    currency = models.IntegerField(db_column="currency", blank=True, null=True)
    partition_ing_date = models.DateField(
        db_column="partitioningdate", blank=True, null=True
    )
    shift_change_reason_start = models.IntegerField(
        db_column="shiftchangereasonstart",
        blank=True,
        null=True,
        choices=model_types.ShiftChangeReasons,
    )
    shift_change_reason_end = models.IntegerField(
        db_column="shiftchangereasonend",
        blank=True,
        null=True,
        choices=model_types.ShiftChangeReasons,
    )
    cash_period_no = models.IntegerField(
        db_column="cashperiodno",
        blank=True,
        null=True,
        help_text="Cash period reference No zCASHPER is increased by one for shift "
        "start. So same period number runs across one or more shifts until and "
        "including next shift end with same reason of shift change "
        "SHCHG_REASON_CASH_PERIOD",
    )
    cash_per_force_mode_start = models.IntegerField(
        db_column="cashperforcemodestart",
        blank=True,
        null=True,
        choices=model_types.CashPerForceMode,
    )
    cash_per_force_mode_end = models.IntegerField(
        db_column="cashperforcemodeend",
        blank=True,
        null=True,
        choices=model_types.CashPerForceMode,
    )
    cash_per_triggers_start = models.IntegerField(
        db_column="cashpertriggersstart",
        blank=True,
        null=True,
        choices=model_types.CashPerTrigger,
    )
    cash_per_triggers_end = models.IntegerField(
        db_column="cashpertriggersend",
        blank=True,
        null=True,
        choices=model_types.CashPerTrigger,
    )
    cash_per_condition_start = models.IntegerField(
        db_column="cashperconditionstart",
        blank=True,
        null=True,
        choices=model_types.CashPerCondition,
    )
    cash_per_condition_end = models.IntegerField(
        db_column="cashperconditionend",
        blank=True,
        null=True,
        choices=model_types.CashPerCondition,
    )
    cash_per_last_receipt_no_start = models.IntegerField(
        db_column="cashperlastreceiptnostart",
        blank=True,
        null=True,
        help_text="Machine issues receipts to service person on manual cash period "
        "change automatically with contents of closed cash period from transaction "
        "logging. These receipts show the cash period no zCASHPER - so a unique "
        "reference to NWC data is given."
        "Depending on application one or several receipts are issued for the data. "
        "So an additional running receipt no (overall) and increased for each "
        "receipt is printed. "
        "Data of shift contains zLASTRCPNO with the last receipt no issued. "
        "This number only shows the last receipt number issued before this cash "
        "period change, because receipt creation is always done after the closure "
        "of cash period!"
        "Each shift - independent of reason - contains always the last actual one.",
    )
    cash_per_last_receipt_no_end = models.IntegerField(
        db_column="cashperlastreceiptnoend",
        blank=True,
        null=True,
        help_text="Machine issues receipts to service person on manual cash period "
        "change automatically with contents of closed cash period from transaction "
        "logging."
        "These receipts show the cash period no zCASHPER - so a unique reference to "
        "NWC data is given."
        "Depending on application one or several receipts are issued for the data. "
        "So an additional running receipt no (overall) and increased for each "
        "receipt is printed."
        "Data of shift contains zLASTRCPNO with the last receipt no issued. "
        "This number only shows the last receipt number issued before this cash "
        "period change, because receipt creation is always done after the closure "
        "of cash period!"
        "Each shift - independent of reason - contains always the last actual one.",
    )
    cash_sub_period_no_start = models.IntegerField(
        db_column="cashsubperiodnostart",
        blank=True,
        null=True,
        help_text="Number of Sub Period at start",
    )
    cash_sub_period_no_end = models.IntegerField(
        db_column="cashsubperiodnoend",
        blank=True,
        null=True,
        help_text="Number of Sub Period at end",
    )
    deposit_period = models.IntegerField(
        db_column="depositperiod", blank=True, null=True
    )
    vendor_shift_no = models.IntegerField(
        db_column="vendorshiftno", blank=True, null=True
    )

    main_shift = models.ForeignObject(
        MainShift,
        models.PROTECT,
        from_fields=("device_class", "device_id", "unique_ms_id"),
        to_fields=("device_class", "device_id", "unique_ms_id"),
    )
    tariff_version = models.ForeignKey(
        "general.TariffVersions",
        models.SET_NULL,
        db_column="tariffversion",
        blank=True,
        null=True,
        help_text="link to TariffVersions.VersionID",
        related_name="sales_shifts",
    )

    class Meta:
        db_table = "salesshift"

        constraints = [
            ForeignReferencesConstraint(
                "revenue.MainShift",
                name="r_119",
                from_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                ),
                to_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                ),
            )
        ]

    def __str__(self):
        return "SalesShift: {},{},{},{}".format(  # noqa: UP032
            self.device_class,
            self.device_id,
            self.unique_ms_id,
            self.sales_shift_no,
        )


class SalesTransaction(models.Model):
    pk = models.CompositePrimaryKey(
        "device_class",
        "device_id",
        "unique_ms_id",
        "sales_transaction_no",
    )
    aborted_sale = models.BooleanField(
        db_column="abortedsale",
        blank=True,
        null=True,
        help_text="bit is set if a sales transaction was aborted without additional "
        "money in total in the system (e.g. spoiled tickets MNR/LIRR). It is of cause "
        "possible that changes in the money magazines and vaults contents took place.",
    )
    cash_amount = models.IntegerField(
        db_column="cashamount",
        blank=True,
        null=True,
        help_text="cash amount of sales transaction",
    )
    cash_booking_flag = models.BooleanField(
        db_column="cashbookingflag",
        blank=True,
        null=True,
        choices=model_types.CashBookingFlag,
    )
    cash_flag = models.BooleanField(
        db_column="cashflag", blank=True, null=True, choices=model_types.CashFlag
    )
    cashless_flag = models.BooleanField(
        db_column="cashlessflag",
        blank=True,
        null=True,
        choices=model_types.CashLessFlag,
    )
    crea_date = models.DateField(db_column="creadate", blank=True, null=True)
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.CASCADE,
        db_column="deviceclassid",
        help_text="unique identifier of DeviceClass",
    )
    device_id = models.IntegerField(db_column="deviceid")
    multi_payment_flag = models.BooleanField(
        db_column="multipaymentflag", blank=True, null=True
    )
    partition_ing_date = models.DateField(
        db_column="partitioningdate",
        blank=True,
        null=True,
        help_text="Timestamp related to MAINSHIFT.ENDCREADATE for "
        "Oracle Table Partitioning purposes.",
    )
    sales_shift_no = models.IntegerField(
        db_column="salesshiftno", help_text="Number of sales shift"
    )

    sales_transaction_no = models.IntegerField(
        db_column="salestransactionno",
        help_text="Running Transaction Number, unique for a main shift",
    )
    snob_amount = models.IntegerField(db_column="snobamount", blank=True, null=True)
    snob_flag = models.BooleanField(db_column="snobflag", blank=True, null=True)
    test_sale_flag = models.BooleanField(
        db_column="testsaleflag", blank=True, null=True
    )
    unique_ms_id = models.IntegerField(db_column="uniquemsid")

    sales_shift = models.ForeignObject(
        SalesShift,
        models.PROTECT,
        from_fields=("device_class", "device_id", "unique_ms_id", "sales_shift_no"),
        to_fields=("device_class", "device_id", "unique_ms_id", "sales_shift_no"),
        related_name="sales_transactions",
    )

    class Meta:
        db_table = "salestransaction"
        constraints = [
            ForeignReferencesConstraint(
                "revenue.SalesShift",
                name="r_456",
                from_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                    "sales_shift_no",
                ),
                to_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                    "sales_shift_no",
                ),
            )
        ]

    def __str__(self):
        return "SalesTransaction: {},{},{},{}".format(  # noqa: UP032
            self.device_class,
            self.device_id,
            self.unique_ms_id,
            self.sales_transaction_no,
        )


class SalesDetail(models.Model):
    pk = models.CompositePrimaryKey(
        "device_class",
        "device_id",
        "unique_ms_id",
        "sales_transaction_no",
        "sales_detail_ev_sequ_no",
        "correction_counter",
    )
    adult_count = models.IntegerField(
        db_column="adultcount",
        blank=True,
        null=True,
        help_text="In the case of single cards, the field NUMBER OF ADULTS has "
        "the value 1, the field NUMBER OF YOUTH has the value 0, the field NUMBER \n"
        "OF CHILDREN has the value 0. In the case of group cards, the respective "
        "number of persons can be stated in all three fields.",
    )
    article_no = models.IntegerField(
        db_column="articleno",
        blank=True,
        null=True,
        help_text="The unambiguousness of the article which is addressed "
        "by the procedure is given by the article number FLART and, with regard "
        "to the tariff, by the tariff version FLTAV. A data record in the article "
        "master file can be unambiguously defined by means of the combination "
        "TARIFF VERSION / ARTICLE NUMBER.",
    )
    article_sign = models.BooleanField(
        db_column="articlesign",
        blank=True,
        null=True,
        help_text="The article sign is defined in the tariff data. It describes "
        "whether an article is a sales article or if an article is a credit note. "
        "See also explanation for TRANSACTION SIGN above.",
    )
    branch_line_id = models.IntegerField(
        db_column="branchlineid",
        blank=True,
        null=True,
        help_text="defines the tariff related branch/line information "
        "(branch/line information are independent from the physical "
        "location of the selling device.",
    )
    business = models.ForeignKey(
        "general.Company",
        db_column="businessid",
        on_delete=models.SET_NULL,
        null=True,
        related_name="salesdetail_busicness",
        help_text="This field is used for BUSINESS-ID.",
    )
    cancellation = models.BooleanField(
        db_column="cancellation",
        blank=True,
        null=True,
        choices=model_types.CancelationType,
        help_text="Is only set in the case of served sales devices in case of a "
        "reversal transaction with the replacement or credit of paid amount, "
        "not with vending machine (informative character but also relevant "
        "to create the transaction sign). See also explanation for "
        "TRANSACTION SIGN above.",
    )
    cash_box = models.BooleanField(
        db_column="cashbox", blank=True, null=True, choices=model_types.CashBoxType
    )
    child_count = models.IntegerField(
        db_column="childcount",
        blank=True,
        null=True,
        help_text="In the case of single cards, the field NUMBER OF ADULTS has the "
        "value 1, the field NUMBER OF YOUTH has the value 0, the field "
        "NUMBER OF CHILDREN has the value 0. In the case of group cards, "
        "the respective number of persons can be stated in all three fields.",
    )
    correction_counter = models.IntegerField(
        db_column="correctioncounter",
        help_text="Counter to display a modified sales record by GUI",
    )
    correction_date = models.DateTimeField(
        db_column="correctiondate", blank=True, null=True
    )
    correction_flag = models.BooleanField(
        db_column="correctionflag", choices=model_types.CorrectionFlagType
    )
    correction_user = models.CharField(
        db_column="correctionuser",
        max_length=20,
        blank=True,
        help_text="identification name of the user this is the real "
        '"user name" of the user',
    )
    crea_date = models.DateTimeField(db_column="creadate", help_text="Selling date")
    custom_specific_card = models.BooleanField(
        db_column="customspeccard",
        blank=True,
        null=True,
        help_text="Yes: A customer-specific follow-up card record is a part of this "
        "sales event. Several sales events can follow until the respective "
        "customer-specific follow-up card record is entered.",
    )
    custom_specific_card_no = models.IntegerField(
        db_column="customspeccardno",
        blank=True,
        null=True,
        help_text="in the case of sales procedures effected by means of a "
        "customer-specific card (tokens), the entered or electronically "
        "read number of the customer-specific card is stated here. "
        "In the case of a spare ticket and in the case of an upgrade, "
        "the ticket number of the original is stated here.",
    )
    dest_station_id = models.IntegerField(
        db_column="deststation",
        blank=True,
        null=True,
        help_text="for tickets with specified relations: source, "
        "destination and/or via (transfer) station. A via (transfer) "
        "station may be missing, if the sales transaction refers to direct connection.",
    )
    dest_type = models.IntegerField(
        db_column="desttype",
        blank=True,
        null=True,
        choices=ZoneStationType,
        help_text="type of value in DestStation",
    )
    dest_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.SET_NULL,
        from_fields=("version", "dest_station_id", "via_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="sales_detail_dest_station",
    )
    devaluation = models.BooleanField(
        db_column="devaluation",
        blank=True,
        null=True,
        help_text="Yes: The article has been devaluated on the stored value card. "
        "The stored value card information is saved in the attached "
        "customer-specific card record.",
    )
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.CASCADE,
        db_column="deviceclassid",
        help_text="unique identifier of DeviceClass",
    )
    device_id = models.IntegerField(
        db_column="deviceid", help_text="Unique Tvm ID 1-999999"
    )
    distance_category = models.IntegerField(
        db_column="distancecategory",
        blank=True,
        null=True,
        help_text="distance category (needed in case of distance depending tariffs)",
    )
    fare_opt_amount = models.IntegerField(
        db_column="fareoptamount",
        blank=True,
        null=True,
        help_text="This field is used for FARE-OPTION-AMOUNT",
    )
    fare_opt_val_date = models.DateTimeField(
        db_column="fareoptvaldate",
        blank=True,
        null=True,
        help_text="contains FARE-OPTION_VALID-ON-DATE",
    )
    fixed_variable_price = models.BooleanField(
        db_column="fixedvariableprice",
        blank=True,
        null=True,
        help_text="a variable price is either entered by the operator during "
        "the sales procedure or it is an article the sales price of which is "
        "defined by means of an algorithm "
        "(e.g. distance calculation / price table) - for such articles it might not"
        " possible to carry out a multiplication of the article tariff with the "
        "number of units (no plausibility).",
    )
    late_cancelation = models.BooleanField(
        db_column="latestorno",
        blank=True,
        null=True,
        help_text="indication that a cancellation was done later then the original "
        "transaction but within the same shift",
    )
    location_type = models.IntegerField(
        db_column="locationtype",
        blank=True,
        null=True,
        choices=model_types.LocationType,
        help_text="type of value in TariffLocationID",
    )
    machine_booking = models.BooleanField(
        db_column="machinebooking",
        blank=True,
        null=True,
        help_text="A cancellation of the actual transaction caused by the sales "
        "device for production or booking-technical reasons (informative character "
        "but also relevant to create the transaction sign). "
        "See also explanation for TRANSACTION SIGN above.",
    )
    miscellaneous = models.BooleanField(
        db_column="miscellaneous",
        blank=True,
        null=True,
        help_text="YES: Transaction is a miscellaneous debit or credit. "
        "Credit or debit is indicated by Transaction sign (wFLTYP). "
        "This Flag is specially used in MNR/LIRR and following projects.",
    )
    partition_ing_date = models.DateTimeField(
        db_column="partitioningdate",
        blank=True,
        null=True,
        help_text="Timestamp related to MAINSHIFT.ENDCREADATE for "
        "Oracle Table Partitioning purposes.",
    )
    plausi_sign = models.BooleanField(
        db_column="plausisign",
        blank=True,
        null=True,
        help_text="indicates weather DBWrite process recovered anything not "
        "plausible in this record",
    )
    prev_ticket_sn = models.BigIntegerField(
        db_column="prevticketsn", blank=True, null=True
    )
    production_article = models.BooleanField(
        db_column="productionarticle",
        blank=True,
        null=True,
        help_text="This RVTRAN record is a member of a product which is produced "
        "at the machine (printer, magnet stripe unit, smart card unit) creating "
        "this record at the moment of production. In contrast 'Over the counter' "
        "products (only office machines) are 'no production' articles, their issuing "
        "is not under control of the machine, the agent is responsible.",
    )
    production_done = models.BooleanField(
        db_column="productiondone",
        blank=True,
        null=True,
        help_text="Yes:"
        "This RVTRAN record is a member of a product which is produced at "
        "the machine (printer, magnet stripe unit, smart card unit) creating "
        "this record at the moment of production. The production was successful "
        "in a way that the production device has detected all valid elements "
        "produced (a ticket is printed completely). "
        "In combination with following flag PRODUCTION_UNSURE reset (see below) "
        "the product was issued without error. If PRODUCTION_UNSURE is set , "
        "issuing of the well produced product was not detected or not possible."
        "No:"
        "If PRODUCTION_ARTICLE is set defining an article produced on the machine, "
        "production was started, but was not successfully completed. For a ticket it "
        "is assumed, that it is not issued in that case. "
        "A following RVTRAN record with same opposite amount voids this RVTRAN. "
        "PRODUCTION_UNSURE flag is set.",
    )
    production_unsure = models.BooleanField(
        db_column="productionunsure",
        blank=True,
        null=True,
        help_text="This RVTRAN record is a member of a product which is produced "
        "at the machine (printer, magnet stripe unit, smart card unit) creating "
        "this record at the moment of production. "
        "The production was not successful or not completely successful.",
    )
    real_statistic_article = models.BooleanField(
        db_column="realstatisticarticle",
        blank=True,
        null=True,
        help_text="Statistical articles do not correspond to sales procedures, "
        "they do not create a receipt on the vending machine, they are used for "
        "counting purposes ( e.g. ticket number tracking or handicapped persons "
        "or the like). They do not have an amount and its number is not "
        "contained in unit sums of shift data records.",
    )
    recovered_after_crash = models.BooleanField(
        db_column="recoveredaftercrash",
        blank=True,
        null=True,
        help_text="Bit is set for each record, which is completed "
        "(resetting temporary status) or added as a void record in a boot recovery "
        "of a sales transaction which was aborted by a crash of any reason "
        "(e.g. uncontrolled powerfail). Flag is for additional information only. "
        "It has no influence to the validity of the value and must not be excluded "
        "from settlement by this flag",
    )
    ref_event_sequ_no = models.IntegerField(
        db_column="refeventsequno",
        blank=True,
        null=True,
        help_text="Reference to related transaction record RVTRAN. "
        "This field (zFLREF) contains the RECORD SEQUENCE NUMBER (zFLLFN) of the "
        "related transaction record in case that the actual record is a "
        "cancellation or correction record.",
    )
    replacement_ticket = models.BooleanField(
        db_column="replacementticket",
        blank=True,
        null=True,
        help_text="Identifier whether the issued ticket is a "
        "physically replaced ticket",
    )
    run_receipt_no = models.IntegerField(
        db_column="runreceiptno",
        blank=True,
        null=True,
        help_text="accumulative number for printed receipts for sales transactions, "
        "this is a unique number that may differs from the running transaction "
        "sequence number (zFLRTNO)",
    )
    rv_tran_count_in_prod_job = models.IntegerField(
        db_column="rvtrancountinprodjob",
        blank=True,
        null=True,
        help_text="0-255.Each production job may include more than one RVTRAN - "
        "Record (combined ticket of different articles). This is also valid for a "
        "series of articles combined to a product which is not produced at machine "
        "but sold from store.First RVTRAN-Record of each job has "
        "set RVTRAN COUNT IN JOB = 0. "
        "All following RVTRAN records belonging to the same job carry an increased "
        "job count RVTRAN COUNT IN JOB 1-255.",
    )
    sales_detail_ev_sequ_no = models.IntegerField(
        db_column="salesdetailevsequno",
        help_text="Running Event Number, unique for a device",
    )
    sales_pack_count = models.IntegerField(
        db_column="salespackcount",
        blank=True,
        null=True,
        help_text="enumerates the sales packets in one transaction",
    )
    sales_pack_id = models.IntegerField(
        db_column="salespackid",
        blank=True,
        null=True,
        help_text="This field contains the packet ID for packet sales "
        "to determine under which packet a single transaction was made.",
    )
    sales_pack = models.ForeignObject(
        "tariff.SalesPackets",
        on_delete=models.SET_NULL,
        from_fields=("version", "sales_pack_id"),
        to_fields=("version", "packet_id"),
        null=True,
        serialize=False,
        related_name="sales_details",
    )
    sales_transaction_no = models.IntegerField(
        db_column="salestransactionno",
        help_text="Running Transaction Number, unique for a device",
    )

    sales_transaction = models.ForeignObject(
        SalesTransaction,
        models.PROTECT,
        from_fields=(
            "device_class",
            "device_id",
            "unique_ms_id",
            "sales_transaction_no",
        ),
        to_fields=("device_class", "device_id", "unique_ms_id", "sales_transaction_no"),
        serialize=False,
        related_name="sales_details",
    )
    selling_rail_road_id = models.IntegerField(
        db_column="sellingrrid",
        blank=True,
        null=True,
        help_text="defines the Railroad (tariff owner) from which tariff related "
        "article in this record was sold, references Company.CompanyID",
    )
    single_group_tick = models.BooleanField(
        db_column="singlegrouptick",
        blank=True,
        null=True,
        help_text="a group ticket is characterised by the specific definition of "
        "the individual customers tariff system.",
    )
    single_sum_sale = models.BooleanField(
        db_column="singlesumsale",
        blank=True,
        null=True,
        help_text="In the case of a sum sales procedure (accumulation key), "
        "several sales procedures are accumulated for a display of the accumulated "
        "amount in the sales device. Each sales procedure, however, "
        "has been booked separately - this identifier has informative character only.",
    )
    sn_processed = models.FloatField(db_column="sn_processed", blank=True, null=True)
    sold_for_company = models.ForeignKey(
        "general.Company",
        db_column="soldforcompany",
        on_delete=models.SET_NULL,
        null=True,
        related_name="salesdetail_sold_for_company",
        help_text="CompanyID of company for which article was sold",
    )
    start_station_id = models.IntegerField(
        db_column="startstation",
        blank=True,
        null=True,
        help_text="for tickets with specified relations: source, destination "
        "and/or via (transfer) station. A via (transfer) station may be missing, "
        "if the sales transaction refers to direct connection.",
    )
    start_type = models.IntegerField(
        db_column="starttype",
        blank=True,
        null=True,
        choices=ZoneStationType,
        help_text="type of value in StartStation",
    )
    start_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.SET_NULL,
        from_fields=("version", "start_station_id", "via_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="sales_detail_start_station",
    )
    tariff_location_id = models.IntegerField(
        db_column="tarifflocationid",
        blank=True,
        null=True,
        help_text="ID of tariff location where ticket was sold",
    )
    version = models.ForeignKey(
        "general.TariffVersions",
        models.PROTECT,
        db_column="tariffversion",
        help_text="This field is used to store the tariff version for the sold "
        "article (TicketType)",
        related_name="sales_details",
    )
    temp_booking = models.BooleanField(
        db_column="tempbooking",
        blank=True,
        null=True,
        help_text="bit is set as long as sales transaction was not finished. "
        "(e.g. in case of unsuccessful printing). "
        "In case of successful transaction the bit is reset to 0 by the "
        "selling device itself.",
    )
    ticket_serial_char = models.CharField(
        db_column="ticketserialchar", max_length=32, blank=True
    )
    ticket_serial_no = models.BigIntegerField(
        db_column="ticketserialno",
        blank=True,
        null=True,
        help_text="This field contains the MANUFATURER-SERIAL-NUMBER of the ticket. "
        "This is a 14 digit value.",
    )
    ticket_serial_no_int64_flag = models.BooleanField(
        db_column="ticketserialnoint64flag", blank=True, null=True
    )
    ticket_stock_type = models.IntegerField(
        db_column="ticketstocktype",
        blank=True,
        null=True,
        help_text="internal ticket stock type, reference to "
        "TicketStockType.IntTicketType",
    )
    transact_sign = models.BooleanField(
        db_column="transactsign",
        blank=True,
        null=True,
        help_text="describes the sign of the transaction. The flag defines how "
        "the amount zFLBTR is used for later summary calculations. "
        "The ARTICLE SIGN ( see below wFLAPAR, D4) together with the CANCELLATION FLAG "
        "or the MACHINE BOOKING FLAG (wFLAPAR, D6/D7) defines the TRANSACTION SIGN. "
        "If the CANCELLATION FLAG or the MACHINE BOOKING FLAG is set the "
        "TRANSACTION SIGN is the result of the inversion of the ARTICLE SIGN.",
    )
    transport_other = models.BooleanField(
        db_column="transportother",
        blank=True,
        null=True,
        help_text="Transportation comprises all tickets to which a transportation "
        "factor can be assigned to. Timetables, credit notes, etc. do not have a "
        "relevant START-DESTINATION relation in the data record.",
    )
    unique_ms_id = models.IntegerField(
        db_column="uniquemsid",
        help_text="Unique Main Shift ID, this ID is unique for each Device, "
        "it is steadily incremented, even if Device is set back (047'er)",
    )
    upgrade = models.BooleanField(
        db_column="upgrade",
        blank=True,
        null=True,
        help_text="This flag is set in case that an existing ticket is re-valued by "
        "the selling machine (e.g. BART add-fare machine)",
    )
    val_period_end = models.DateTimeField(
        db_column="valperiodend",
        blank=True,
        null=True,
        help_text="contains FARE-OPTION_VALID-OFF-DATE",
    )
    via_station_id = models.IntegerField(
        db_column="viastation",
        blank=True,
        null=True,
        help_text="for tickets with specified relations: source, destination "
        "and/or via (transfer) station. A via (transfer) station may be missing, "
        "if the sales transaction refers to direct connection.",
    )
    via_type = models.IntegerField(
        db_column="viatype",
        blank=True,
        null=True,
        help_text="type of value in ViaStation",
        choices=ZoneStationType,
    )
    via_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.SET_NULL,
        from_fields=("version", "via_station_id", "via_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="sales_detail_via_station",
    )
    youth_count = models.IntegerField(
        db_column="youthcount",
        blank=True,
        null=True,
        help_text="In the case of single cards, the field NUMBER OF ADULTS has the "
        "value 1, the field NUMBER OF YOUTH has the value 0, the field "
        "NUMBER OF CHILDREN has the value 0. In the case of group cards, "
        "the respective number of persons can be stated in all three fields.",
    )

    class Meta:
        db_table = "salesdetail"
        constraints = [
            ForeignReferencesConstraint(
                "revenue.SalesTransaction",
                name="r_457",
                from_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                    "sales_transaction_no",
                ),
                to_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                    "sales_transaction_no",
                ),
            )
        ]

    def __str__(self):
        return "SalesDetail: {},{},{},{},{},{}".format(  # noqa: UP032
            self.device_class,
            self.device_id,
            self.unique_ms_id,
            self.sales_transaction_no,
            self.sales_detail_ev_sequ_no,
            self.correction_counter,
        )


class CashLessPayment(models.Model):
    """
    Contains sero or one record for every Transaction.
    A transaction is identified by UploadSalesData.RunTransctNo.
    FK references to the last UploadSalesRecord of a Transaction.
    The record contains information about the credit card payment.
    """

    pk = models.CompositePrimaryKey(
        "device_class",
        "device_id",
        "unique_ms_id",
        "sales_transaction_no",
        "event_sequ_no",
    )
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.CASCADE,
        db_column="deviceclassid",
        help_text="unique identifier of DeviceClass",
    )
    device_id = models.IntegerField(
        db_column="deviceid", help_text="Unique Tvm ID 1-999999"
    )
    event_sequ_no = models.IntegerField(db_column="eventsequno")
    unique_ms_id = models.IntegerField(
        db_column="uniquemsid",
        help_text="Unique Main Shift ID, this ID is unique for each Device, "
        "it is steadily incremented, even if Device is set back (047'er)",
    )
    crea_date = models.DateField(db_column="creadate")
    sales_transaction_no = models.IntegerField(
        db_column="salestransactionno",
        help_text="Running Transaction Number, unique for a main shift",
    )

    ident_type = models.IntegerField(db_column="identtype", blank=True, null=True)
    pay_type_cash_less = models.IntegerField(
        db_column="paytypecashless", choices=model_types.CashLessPaymentTypes
    )
    chk_vou_bank_id = models.CharField(
        db_column="chkvoubankid",
        max_length=24,
        blank=True,
        help_text="Encrypted Card Number",
    )
    short_epan = models.CharField(
        db_column="shortepan",
        max_length=4,
        blank=True,
        help_text="Last 4 digits of the Card Number",
    )
    chk_vou_num = models.CharField(db_column="chkvounum", max_length=24, blank=True)
    card_id_number = models.CharField(
        db_column="cardidnumber",
        max_length=40,
        blank=True,
        help_text="Encrypted Card Number",
    )
    amount = models.IntegerField(db_column="amount", blank=True, null=True)
    booking_selection = models.BooleanField(
        db_column="bookingselection",
        blank=True,
        null=True,
        choices=model_types.BookingSelection,
    )
    bank_auth_no = models.CharField(db_column="bankauthno", max_length=12, blank=True)
    bank_trace_no = models.IntegerField(db_column="banktraceno", blank=True, null=True)
    name = models.CharField(db_column="name", max_length=24, blank=True)
    booking_sequ_no = models.IntegerField(
        db_column="bookingsequno", blank=True, null=True
    )
    expire_date = models.CharField(
        db_column="expiredate",
        max_length=4,
        blank=True,
        help_text="expire date of card, format YYMM",
    )
    authorisation_date = models.DateField(
        db_column="authorisationdate", blank=True, null=True
    )
    currency = models.IntegerField(db_column="currency", blank=True, null=True)
    currency_flag = models.BooleanField(db_column="currencyflag", blank=True, null=True)
    refund_flag = models.IntegerField(db_column="refundflag", blank=True, null=True)
    key_index = models.IntegerField(db_column="keyindex", blank=True, null=True)
    partitioning_date = models.DateField(
        db_column="partitioningdate", blank=True, null=True
    )
    hashed_epan = models.CharField(db_column="hashedepan", max_length=40, blank=True)

    sales_transaction = models.ForeignObject(
        SalesTransaction,
        models.PROTECT,
        from_fields=(
            "device_class",
            "device_id",
            "unique_ms_id",
            "sales_transaction_no",
        ),
        to_fields=("device_class", "device_id", "unique_ms_id", "sales_transaction_no"),
        related_name="cashless_payments",
    )

    class Meta:
        db_table = "cashlesspayment"
        constraints = [
            ForeignReferencesConstraint(
                "revenue.SalesTransaction",
                name="r_459",
                from_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                    "sales_transaction_no",
                ),
                to_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                    "sales_transaction_no",
                ),
            )
        ]

    def __str__(self):
        return self.name


class CashPayment(models.Model):
    """
    Contains sero to n records for every Transaction.
    A transaction is identified by UploadSalesData.RunTransctNo.
    FK references to the last UploadSalesRecord of a Transaction.
    One record for every coin type used to pay for the Transaction.
    """

    pk = models.CompositePrimaryKey(
        "device_class",
        "device_id",
        "unique_ms_id",
        "sales_transaction_no",
        "payment_type",
        "payment_type_id",
        "change_flag",
    )
    change_flag = models.IntegerField(
        db_column="changeflag", choices=model_types.CashPaymentChangeFlags
    )
    crea_date = models.DateField(db_column="creadate")
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.CASCADE,
        db_column="deviceclassid",
        help_text="unique identifier of DeviceClass",
    )
    device_id = models.IntegerField(
        db_column="deviceid", help_text="Unique Tvm ID 1-999999"
    )
    event_sequ_no = models.IntegerField(db_column="eventsequno")
    number_pieces = models.IntegerField(
        db_column="numberpieces",
        blank=True,
        null=True,
        help_text="number of pieces of that coin type",
    )
    partition_ing_date = models.DateField(
        db_column="partitioningdate",
        blank=True,
        null=True,
        help_text="Timestamp related to MAINSHIFT.ENDCREADATE "
        "for Oracle Table Partitioning purposes.",
    )
    payment_type = models.IntegerField(
        db_column="paymenttype", choices=model_types.CashPaymentTypes
    )
    payment_type_id = models.IntegerField(
        db_column="paymenttypeid",
        help_text="(PaymentType, PaymentTypeID) is unique identifier for a cash type, "
        "eg new 20$ bill, or 10c coin, references to CashType.Type,CashType.CashTypeID",
    )
    payment_type_value = models.IntegerField(
        db_column="paymenttypevalue", help_text="value of that coin type"
    )
    sales_transaction_no = models.IntegerField(
        db_column="salestransactionno",
        help_text="Running Transaction Number, unique for a main shift",
    )

    unique_ms_id = models.IntegerField(
        db_column="uniquemsid",
        help_text="Unique Main Shift ID, this ID is unique for each Device, "
        "it is steadily incremented, even if Device is set back (047'er)",
    )

    sales_transaction = models.ForeignObject(
        SalesTransaction,
        models.CASCADE,
        from_fields=(
            "device_class",
            "device_id",
            "unique_ms_id",
            "sales_transaction_no",
        ),
        to_fields=(
            "device_class",
            "device_id",
            "unique_ms_id",
            "sales_transaction_no",
        ),
        related_name="cash_payments",
    )

    class Meta:
        db_table = "cashpayment"
        constraints = [
            ForeignReferencesConstraint(
                "revenue.SalesTransaction",
                name="r_458",
                from_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                    "sales_transaction_no",
                ),
                to_fields=(
                    "device_class_id",
                    "device_id",
                    "unique_ms_id",
                    "sales_transaction_no",
                ),
            )
        ]

    def __str__(self):
        return "{},{},{},{},{},{},{}".format(  # noqa: UP032
            self.device_class,
            self.device_id,
            self.unique_ms_id,
            self.sales_transaction_no,
            self.payment_type,
            self.payment_type_id,
            self.change_flag,
        )
