"""Package for all models related to the core.ticket app"""

import pytz
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from core.contrib.db.constraints import ForeignReferencesConstraint
from core.contrib.db.fields import DecimalIntField
from core.general.model_types import ZoneStationType
from core.ticket.model_managers import PaperTicketManager, TicketScanManager
from core.ticket.model_types import TicketFormType

User = get_user_model()


# Create your models here.


class TicketSource(models.Model):
    """Ticket source, (eTix, PaperTicket, OBTIMS)"""

    STIM = 1
    TIMS = 2
    OBTIMS = 3
    MNRGA = 4

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=6, default="")
    icon = models.CharField(max_length=50, default="", blank=True)

    def __str__(self) -> str:
        return self.name


class Ticket(models.Model):
    """
    Ticket table following the paper ticket structure

    .. image:: /static/images/ticket_number_decode.svg
    """

    sales_packet_id = models.IntegerField(
        db_column="tickettypeid",
        null=True,
        help_text="This field contains the packet ID for packet sales to determine "
        "under which packet a single transaction was made.",
    )
    sales_packet = models.ForeignObject(
        "tariff.SalesPackets",
        on_delete=models.SET_NULL,
        from_fields=("version", "sales_packet_id"),
        to_fields=("version_id", "packet_id"),
        null=True,
        editable=False,
    )
    form = models.CharField(
        max_length=12, choices=TicketFormType, default=TicketFormType.PAPER
    )
    number = models.CharField(
        max_length=20, db_index=True, help_text="Decoded full ticket-number"
    )
    amount = DecimalIntField(
        db_column="amount",
        decimal_places=2,
        help_text="This field is used for FARE-OPTION-AMOUNT",
    )
    from_type = models.SmallIntegerField(
        db_column="fromtype", null=True, blank=True, choices=ZoneStationType
    )
    from_station_id = models.IntegerField(
        db_column="fromstation",
        null=True,
        blank=True,
        help_text="for tickets with specified relations: source, "
        "destination and/or via (transfer) station. A via (transfer) station "
        "may be missing, if the sales transaction refers to direct connection.",
    )
    from_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "from_station_id", "from_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="ticket_from_station",
        editable=False,
    )
    to_type = models.SmallIntegerField(
        db_column="totype", null=True, blank=True, choices=ZoneStationType
    )
    to_station_id = models.IntegerField(
        db_column="tostation",
        null=True,
        blank=True,
        help_text="for tickets with specified relations: source, destination and/or "
        "via (transfer) station. A via (transfer) station may be missing, "
        "if the sales transaction refers to direct connection.",
    )
    to_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "to_station_id", "to_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="ticket_to_station",
        editable=False,
    )
    valid_from = models.DateTimeField(
        db_column="validfrom", help_text="contains FARE-OPTION_VALID-ON-DATE"
    )
    valid_to = models.DateTimeField(
        db_column="validto", help_text="contains FARE-OPTION_VALID-OFF-DATE"
    )
    count = models.IntegerField(default=1, help_text="Total number of trips")
    time_new = models.DateTimeField(db_column="timenew", auto_created=True)
    user_new = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_ticket_set",
        db_column="usernew",
    )
    version = models.ForeignKey(
        "general.TariffVersions",
        models.PROTECT,
        db_column="versionid",
        help_text="This field is used to store the tariff version for "
        "the sold article (tickettype)",
    )
    device_class = models.ForeignKey(
        "general.DeviceClass",
        on_delete=models.SET_NULL,
        db_column="deviceclassid",
        null=True,
        blank=True,
        help_text="unique identifier of DeviceClass",
    )
    device_id = models.IntegerField(
        db_column="deviceid", null=True, blank=True, help_text="Unique Tvm ID 1-999999"
    )
    unique_ms_id = models.IntegerField(
        db_column="uniquemsid",
        null=True,
        blank=True,
        help_text="Unique Main Shift ID, this ID is unique for each Device, "
        "it is steadily incremented, even if Device is set back (047'er)",
    )
    sales_transaction_no = models.IntegerField(
        db_column="salestransactionno",
        null=True,
        blank=True,
        help_text="Running Transaction Number, unique for a device",
    )
    sales_detail_ev_sequ_no = models.IntegerField(
        db_column="salesdetailevsequno",
        null=True,
        blank=True,
        help_text="Running Event Number, unique for a device",
    )
    correction_counter = models.IntegerField(
        db_column="correctioncounter",
        null=True,
        help_text="Counter to display a modified sales record by GUI",
    )
    sales_transaction = models.ForeignObject(
        "revenue.SalesTransaction",
        models.PROTECT,
        from_fields=(
            "device_class",
            "device_id",
            "unique_ms_id",
            "sales_transaction_no",
        ),
        to_fields=("device_class", "device_id", "unique_ms_id", "sales_transaction_no"),
        null=True,
        serialize=False,
        related_name="tickets",
    )

    sales_detail = models.ForeignObject(
        "revenue.SalesDetail",
        models.SET_NULL,
        from_fields=(
            "device_class",
            "device_id",
            "unique_ms_id",
            "sales_transaction_no",
            "sales_detail_ev_sequ_no",
            "correction_counter",
        ),
        to_fields=(
            "device_class",
            "device_id",
            "unique_ms_id",
            "sales_transaction_no",
            "sales_detail_ev_sequ_no",
            "correction_counter",
        ),
        null=True,
        serialize=False,
        related_name="tickets",
    )

    class Meta:
        constraints = [
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_ticket_from_station",
                from_fields=("version", "from_station_id", "from_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_ticket_to_station",
                from_fields=("version", "to_station_id", "to_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                to="tariff.SalesPackets",
                name="r_ticket_sales_packet",
                from_fields=("version", "sales_packet_id"),
                to_fields=("version_id", "packet_id"),
            ),
            ForeignReferencesConstraint(
                to="revenue.SalesTransaction",
                name="r_ticket_sales_transaction",
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
            ),
            ForeignReferencesConstraint(
                to="revenue.SalesDetail",
                name="r_ticket_sales_detail",
                from_fields=(
                    "device_class",
                    "device_id",
                    "unique_ms_id",
                    "sales_transaction_no",
                    "sales_detail_ev_sequ_no",
                    "correction_counter",
                ),
                to_fields=(
                    "device_class",
                    "device_id",
                    "unique_ms_id",
                    "sales_transaction_no",
                    "sales_detail_ev_sequ_no",
                    "correction_counter",
                ),
            ),
        ]

    def __str__(self):
        return f"{self.number}[{self.get_form_display()}]"  # pyright: ignore[reportAttributeAccessIssue]


class PaperTicket(models.Model):
    """Ticket table following the paper ticket structure"""

    ticket = models.OneToOneField(
        "Ticket", on_delete=models.CASCADE, db_column="ticketid"
    )
    sales_packet_id = models.IntegerField(db_column="tickettypeid", null=True)
    sales_packet = models.ForeignObject(
        "tariff.SalesPackets",
        on_delete=models.SET_NULL,
        from_fields=("version", "sales_packet_id"),
        to_fields=("version_id", "packet_id"),
        null=True,
        related_name="paper_tickets",
    )
    number = models.CharField(max_length=20, db_index=True)
    amount = DecimalIntField(db_column="amount", decimal_places=2)

    from_type = models.SmallIntegerField(db_column="fromtype", null=True, blank=True)
    from_station_id = models.IntegerField(
        db_column="fromstation", null=True, blank=True
    )
    from_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "from_station_id", "from_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="paper_ticket_from_station",
    )
    to_type = models.SmallIntegerField(db_column="totype", null=True, blank=True)
    to_station_id = models.IntegerField(db_column="tostation", null=True, blank=True)
    to_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "to_station_id", "to_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="paper_ticket_to_station",
    )
    via_type = models.SmallIntegerField(db_column="viatype", null=True, blank=True)
    via_station_id = models.IntegerField(db_column="viastation", null=True, blank=True)
    via_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "via_station_id", "via_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="paper_ticket_via_station",
    )
    from_return_type = models.SmallIntegerField(
        db_column="fromreturntype", null=True, blank=True
    )
    from_return_id = models.IntegerField(db_column="fromreturn", null=True, blank=True)
    from_return = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "from_return_id", "from_return_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="paper_ticket_from_return",
    )
    to_return_type = models.SmallIntegerField(
        db_column="toreturntype", null=True, blank=True
    )
    to_return_id = models.IntegerField(db_column="toreturn", null=True, blank=True)
    to_return = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "to_return_id", "to_return_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="paper_ticket_to_return",
    )
    via_return_type = models.SmallIntegerField(
        db_column="viareturntype", null=True, blank=True
    )
    via_return_id = models.IntegerField(db_column="viareturn", null=True, blank=True)
    via_return = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "via_return_id", "via_return_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="paper_ticket_via_return_station",
        serialize=False,
        editable=False,
    )
    valid_from = models.DateTimeField(db_column="validfrom")
    valid_to = models.DateTimeField(db_column="validto")
    count_passenger_category_1 = models.IntegerField(
        db_column="countpassengercategory1", default=1
    )
    start_connection_service = models.IntegerField(
        db_column="startconnectionservice", default=0
    )
    end_connection_service = models.IntegerField(
        db_column="endconnectionservice", default=0
    )

    version = models.ForeignKey(
        "general.TariffVersions",
        models.CASCADE,
        db_column="versionid",
    )

    objects = PaperTicketManager()

    class Meta:
        constraints = [
            ForeignReferencesConstraint(
                to="tariff.SalesPackets",
                name="r_paper_ticket_sales_packet",
                from_fields=("version", "sales_packet_id"),
                to_fields=("version_id", "packet_id"),
            ),
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_paper_ticket_from_station",
                from_fields=("version", "from_station_id", "from_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_paper_ticket_to_station",
                from_fields=("version", "to_station_id", "to_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_paper_ticket_via_station",
                from_fields=("version", "via_station_id", "via_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_paper_ticket_from_return",
                from_fields=("version", "from_return_id", "from_return_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_paper_ticket_to_return",
                from_fields=("version", "to_return_id", "to_return_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_paper_ticket_via_return",
                from_fields=("version", "via_return_id", "via_return_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
        ]

    def __str__(self):
        return f"{self.number}"


class ETixTicket(models.Model):
    """Model class to hold the etix ticket data, following the paper ticket structure"""

    class ActionCodes(models.IntegerChoices):
        """MA Action Codes"""

        NO_ACTION_TAKEN = -1, "No action taken"
        OKAY = 4001, "Validation Successful"
        FINAL = 5001, "Finalized ticket action"
        STEP_UP = 5901, "Step-up ticket"
        EXTEND = 5902, "Stend ticket validity"
        STEP_UP_AND_EXTEND = 5904, "Combined step-up and extend"

    ticket = models.OneToOneField("Ticket", on_delete=models.CASCADE)
    e_ticket_no = models.CharField(db_column="eticketno", max_length=12)
    price = DecimalIntField(db_column="price", decimal_places=2)
    discount_code = models.CharField(
        db_column="discountcode", max_length=20, blank=True, default=""
    )
    product_id = models.IntegerField(db_column="productid")
    activate_start = models.DateTimeField(db_column="activatestart")
    device_utc = models.DateTimeField(db_column="deviceutc")
    from_type = models.SmallIntegerField(db_column="fromtype", null=True, blank=True)
    from_station_id = models.IntegerField(
        db_column="fromstation", null=True, blank=True
    )
    from_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "from_station_id", "from_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="etix_ticket_from_station",
    )
    to_type = models.SmallIntegerField(db_column="totype", null=True, blank=True)
    to_station_id = models.IntegerField(db_column="tostation", null=True, blank=True)
    to_station = models.ForeignObject(
        "general.ZoneStation",
        on_delete=models.PROTECT,
        from_fields=("version", "to_station_id", "to_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="etix_ticket_to_station",
    )
    parent_product_id = models.CharField(db_column="parentproductid", max_length=8)
    line = models.CharField(max_length=128)
    abi = models.CharField(max_length=32)
    act = models.SmallIntegerField(choices=ActionCodes)
    tkt_oc = models.SmallIntegerField(db_column="tktoc")
    version = models.ForeignKey(
        "general.TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
    )

    class Meta:
        constraints = [
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_etix_ticket_from_station",
                from_fields=("version", "from_station_id", "from_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                to="general.ZoneStation",
                name="r_etix_ticket_to_station",
                from_fields=("version", "to_station_id", "to_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.e_ticket_no}"


class Position(models.Model):
    """Defines the tour position from OBTIMS"""

    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.name} [{self.code}]"


class Tour(models.Model):
    """Model class to hold the tour data, following the  OBTIMS structure"""

    code = models.IntegerField(unique=True)
    status = models.SmallIntegerField(default=0)
    company = models.ForeignKey("general.Company", on_delete=models.SET_NULL, null=True)
    emp_nbr = models.CharField(max_length=9)
    crew_id = models.CharField(max_length=15)
    tour_start = models.DateTimeField()
    tour_end = models.DateTimeField(null=True)
    system_date = models.DateTimeField()
    force_close_tour = models.BooleanField(default=False)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    car_number = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.car_number}-{self.emp_nbr}"


class TicketScan(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, related_name="scans")
    tour_id = models.IntegerField(db_column="tourid", default=0)
    conductor_id = models.IntegerField(db_column="conductorid", default=0)
    train_id = models.IntegerField(db_column="trainid", default=0)
    company = models.ForeignKey("general.Company", on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey("TicketSource", on_delete=models.SET_NULL, null=True)
    scanned_on = models.DateTimeField(db_column="scannedon", null=True)
    time_new = models.DateTimeField(db_column="timenew", auto_created=True)
    scan_sync_time = models.BigIntegerField(db_column="scansynctime", default=0)

    objects = TicketScanManager()

    class Meta:
        ordering = ["-scanned_on"]

    def __str__(self) -> str:
        return "{}-{}-{}".format(
            self.ticket.number,
            self.tour_id,
            self.scanned_on.strftime("%Y-%m-%d %H:%M:%S")
            if self.scanned_on is not None
            else "N/A",
        )

    def save(self, *args, **kwargs) -> None:
        if self.time_new and self.scanned_on:
            if isinstance(self.time_new, str):
                self.time_new = parse_datetime(self.time_new)
                if self.time_new and timezone.is_naive(self.time_new):
                    self.time_new = timezone.make_aware(
                        self.time_new,
                        timezone=pytz.UTC,
                    )
            if self.scanned_on.tzinfo is None:
                self.scanned_on = timezone.make_aware(
                    self.scanned_on,
                    timezone=pytz.UTC,
                )
            if self.time_new:
                self.scan_sync_time = abs(
                    (self.time_new - self.scanned_on).total_seconds() * 1000,
                )
        return super().save(*args, **kwargs)
