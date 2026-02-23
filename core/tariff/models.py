from django.db import models

from core.contrib.db.constraints import ForeignReferencesConstraint
from core.tariff import model_types


class TicketType(models.Model):
    """
    This is the list of all known ticket types.

    The TicketType and the relation tables are the most important tables of the
    fare structure.

    The amount is only used if the fare of the ticket type is fixed.

    So here some examples for ticket types:\n
    - One Way Adult\n
    - Monthly Adult\n
    - Monthly Adult, discounted fare\n
    - Admission for a special event\n
    - Metrocard 30$\n
    - Connection service
    """

    class TYPES(models.IntegerChoices):
        FIXED = (1, "Tfixed amount (not dependent from relation table)")
        RELATION = (2, "relation dependent article")
        DIST_CAT = (3, "distance category dependent article")
        CALC_RULE = (4, "calculation rule dependent article")

    pk = models.CompositePrimaryKey("version", "ticket_type_id")
    version = models.ForeignKey(
        "general.TariffVersions",
        db_column="versionid",
        on_delete=models.PROTECT,
        help_text="ID of tariff version",
        related_name="ticket_types",
    )
    ticket_type_id = models.IntegerField(
        db_column="tickettypeid", help_text="Unique id of this ticket type"
    )

    amount = models.IntegerField(
        db_column="amount",
        blank=True,
        null=True,
        help_text="Value of Ticket, NULL if calculated or resulted by Relation",
    )
    bal_amount_1 = models.IntegerField(
        db_column="balamount1",
        blank=True,
        null=True,
        help_text="Additional Amount for Balance/ Report purposes, "
        "application dependent",
    )
    bal_amount_2 = models.IntegerField(
        db_column="balamount2",
        blank=True,
        null=True,
        help_text="Additional Amount for Balance/ Report purposes, "
        "application dependent",
    )
    description = models.CharField(max_length=100, help_text="Description")
    gender_input = models.IntegerField(
        db_column="genderinput",
        blank=True,
        null=True,
        choices=model_types.TicketTypeGenerInput,
    )
    multimedia_group_id = models.IntegerField(
        db_column="multimediagroupid",
        blank=True,
        null=True,
        help_text="Unique identification of a Multimedia Group",
    )
    parameter_1 = models.IntegerField(
        db_column="parameter1", blank=True, null=True, help_text="Variable usage"
    )
    parameter_2 = models.IntegerField(
        db_column="parameter2", blank=True, null=True, help_text="Variable usage"
    )
    parameter_3 = models.IntegerField(
        db_column="parameter3", blank=True, null=True, help_text="Variable usage"
    )
    parameter_4 = models.IntegerField(
        db_column="parameter4", blank=True, null=True, help_text="Variable usage"
    )
    parameter_5 = models.IntegerField(
        db_column="parameter5", blank=True, null=True, help_text="Variable usage"
    )
    parameter_6 = models.IntegerField(
        db_column="parameter6", blank=True, null=True, help_text="Variable usage"
    )
    parameter_7 = models.IntegerField(
        db_column="parameter7", blank=True, null=True, help_text="Variable usage"
    )
    parameter_8 = models.IntegerField(
        db_column="parameter8", blank=True, null=True, help_text="Variable usage"
    )
    parameter_9 = models.CharField(
        db_column="parameter9", max_length=50, blank=True, help_text="Variable usage"
    )
    parameter_10 = models.CharField(
        db_column="parameter10", max_length=50, blank=True, help_text="Variable usage"
    )
    company = models.ForeignKey(
        "general.Company",
        on_delete=models.SET_NULL,
        null=True,
        db_column="serviceproviderid",
        help_text="ID of provider who gives any kind of service",
        related_name="ticket_types",
    )
    summary = models.IntegerField(
        blank=True, null=True, choices=model_types.TicketTypeSummary
    )
    type = models.IntegerField(blank=True, null=True, choices=TYPES)
    validity_id = models.IntegerField(db_column="validityid", null=True)
    validity = models.ForeignObject(
        "general.Validity",
        on_delete=models.SET_NULL,
        from_fields=("validity_id", "version"),
        to_fields=("validity_id", "version"),
        auto_created=True,
        null=True,
        serialize=False,
    )
    time_new = models.DateTimeField(db_column="timenew", auto_created=True)
    user_new = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="created_ticket_type_set",
        db_column="usernew",
    )
    time_change = models.DateTimeField(db_column="timechange", auto_now=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_ticket_type_set",
        db_column="userchange",
    )

    class Meta:
        db_table = "tickettype"
        constraints = [
            ForeignReferencesConstraint(
                "general.Validity",
                name="r_543",
                from_fields=("version", "validity_id"),
                to_fields=("version", "validity_id"),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.description} [{self.ticket_type_id}] ({self.version})"


class TicketTypeGroup(models.Model):
    """
    A Ticket Type Group links tickettypes together which could be summarized in Reports.

    Because of the many reasons to link a TicketType to different groups,
    there are no limitations for that.

    The sales machine does not need this group information.
    """

    pk = models.CompositePrimaryKey(
        "version",
        "ticket_type_group_id",
        "ticket_type_group_type",
    )
    ticket_type_group_id = models.IntegerField(
        db_column="tickettypegroupid", help_text="Unique ID of this ticket type group"
    )
    ticket_type_group_type = models.IntegerField(
        db_column="tickettypegrouptype", help_text="To classify this ticket type group"
    )
    abbreviation = models.CharField(
        max_length=10, blank=True, help_text="Abbreviation for the group"
    )
    description = models.CharField(
        max_length=50,
        blank=True,
        help_text="Short description of this ticket type group",
    )
    multimedia_group_id = models.IntegerField(
        db_column="multimediagroupid", blank=True, null=True
    )
    time_change = models.DateTimeField(blank=True, null=True)
    time_new = models.DateTimeField(blank=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_ticket_type_group",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_ticket_type_group",
    )
    version = models.ForeignKey(
        "general.TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
        related_name="ticket_type_groups",
    )

    class Meta:
        db_table = "tickettypegroup"

    def __str__(self):
        return self.description


class TicketTypeGroupElements(models.Model):
    """This table links tickettypes to one group"""

    pk = models.CompositePrimaryKey(
        "version",
        "ticket_type_id",
        "ticket_type_group_type",
        "ticket_type_group_id",
    )

    version = models.ForeignKey(
        "general.TariffVersions",
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="ticket_type_group_elements",
    )
    ticket_type_group_id = models.IntegerField(
        db_column="tickettypegroupid", help_text="Unique ID of this ticket type group"
    )
    ticket_type_id = models.IntegerField(
        db_column="tickettypeid",
        help_text="Unique id of this ticket type",
        choices=TicketType.TYPES,
    )
    ticket_type = models.ForeignObject(
        TicketType,
        models.CASCADE,
        from_fields=("version", "ticket_type_id"),
        to_fields=("version", "ticket_type_id"),
        related_name="ticket_type_group_elements",
    )
    ticket_type_group_type = models.IntegerField(
        db_column="tickettypegrouptype", help_text="To classify this ticket type group"
    )
    ticket_type_group = models.ForeignObject(
        TicketTypeGroup,
        models.CASCADE,
        from_fields=("version", "ticket_type_group_id", "ticket_type_group_type"),
        to_fields=("version", "ticket_type_group_id", "ticket_type_group_type"),
        related_name="ticket_type_group_elements",
    )

    class Meta:
        db_table = "tickettypegroupelements"
        constraints = [
            ForeignReferencesConstraint(
                "tariff.TicketTypeGroup",
                name="r_192",
                from_fields=(
                    "version",
                    "ticket_type_group_id",
                    "ticket_type_group_type",
                ),
                to_fields=("version", "ticket_type_group_id", "ticket_type_group_type"),
            ),
            ForeignReferencesConstraint(
                "tariff.TicketType",
                name="r_193",
                from_fields=("version", "ticket_type_id"),
                to_fields=("version", "ticket_type_id"),
            ),
        ]

    def __str__(self):
        return "{},{},{},{}".format(  # noqa: UP032
            self.version,
            self.ticket_type_id,
            self.ticket_type_group_type,
            self.ticket_type_group_id,
        )


# Create your models here.
class SalesPackets(models.Model):
    """
    A sales packet will allow you to bind one or more tickets together
    into a 'Sales Packet'. This table describes a 'Sales Packet'.

    In the table 'SalesPacketElements' the single ticket types are assigned
    to this packet. There are several links to other tables for purchase limitations.

    For example,
    the possible start stations for this packet (maybe for a special event).
    The sales packet maybe a 'Special Event' or an other definable combination of
    ticket types. The type of the packet is identified in the field 'PacketType'.

    In addition to this, a sales packet is automatically created,
    by setting up a new ticket type.
    This automatically created sales packet is identified by the field 'PacketType'
    """

    class TYPES(models.IntegerChoices):
        AUTOSALE = (
            0,
            "sales packet was created automatically from the Tickettype Maintenance "
            "Screen, sales packet is not saleable",
        )
        AUTONOSALE = (
            1,
            "sales packet was created automatically from the Tickettype Maintenance "
            "Screen, sales packet is saleable",
        )
        SPECIALEVENT = 2, "sales packet is a special event packet"
        OTHER = 3, "all other sales packets that were created manually"

    pk = models.CompositePrimaryKey("version", "packet_id")
    packet_id = models.IntegerField(
        db_column="packetid", help_text="Unique ID of a salespacket"
    )
    version = models.ForeignKey(
        "general.TariffVersions",
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="sales_packets",
    )
    packet_type = models.IntegerField(
        db_column="packettype", blank=True, null=True, choices=TYPES
    )
    description = models.CharField(max_length=50, blank=True, help_text="Description")
    dest_station_group_id = models.IntegerField(
        db_column="deststationgroupid",
        blank=True,
        null=True,
        help_text="Unique identification of this station group",
    )
    dest_station_group = models.ForeignObject(
        "general.StationGroup",
        models.SET_NULL,
        from_fields=("version", "dest_station_group_id"),
        to_fields=("version", "station_group_id"),
        related_name="sales_packets_dest",
        null=True,
        serialize=False,
    )
    device_class_group_id = models.IntegerField(
        db_column="deviceclassgroupid",
        blank=True,
        null=True,
        help_text="Unique identification of a device class group if not NULL",
    )
    device_class_group = models.ForeignObject(
        "general.DeviceClassGroup",
        models.SET_NULL,
        from_fields=("version", "device_class_group_id"),
        to_fields=("version", "device_class_group_id"),
        null=True,
        editable=False,
        serialize=False,
    )

    external_id = models.CharField(
        db_column="externalid",
        max_length=20,
        blank=True,
        help_text="Reference to external (3rd party) sources (in SWT it is RJIS data).",
    )
    group_fare_id = models.IntegerField(
        db_column="groupfareid",
        blank=True,
        null=True,
        help_text="Link to the Group Fare Table",
    )
    multimedia_group_id = models.IntegerField(
        db_column="multimediagroupid",
        blank=True,
        null=True,
        help_text="Unique identification of a Multimedia Group",
    )

    pay_accept_group_id = models.IntegerField(
        db_column="payacceptgroupid",
        blank=True,
        null=True,
        help_text="Link to a payment acceptance group if not NULL",
    )
    plus_group_id = models.IntegerField(
        db_column="plusgroupid",
        blank=True,
        null=True,
        help_text="Empty or Packets with different Plus GroupID's may not be sold "
        "in one sale",
    )
    sales_station_group_id = models.IntegerField(
        db_column="salesstationgroupid",
        blank=True,
        null=True,
        help_text="Unique identification of this station group",
    )
    sales_station_group = models.ForeignObject(
        "general.StationGroup",
        models.SET_NULL,
        from_fields=("version", "sales_station_group_id"),
        to_fields=("version", "station_group_id"),
        related_name="sales_packets",
        null=True,
        serialize=False,
    )
    send_onl_evt = models.IntegerField(
        db_column="sendonlevt",
        blank=True,
        null=True,
        choices=model_types.SalesPacketsSendOnlEvt,
    )
    start_station_group_id = models.IntegerField(
        db_column="startstationgroupid",
        blank=True,
        null=True,
        help_text="Unique identification of this station group",
    )
    start_station_group = models.ForeignObject(
        "general.StationGroup",
        models.SET_NULL,
        from_fields=("version", "start_station_group_id"),
        to_fields=("version", "station_group_id"),
        related_name="sales_packets_start",
        null=True,
        serialize=False,
    )
    time_lock_group_id = models.IntegerField(
        db_column="timelockgroupid",
        blank=True,
        null=True,
        help_text="Identifier for a specified Timelockgroup",
    )
    time_lock_group = models.ForeignObject(
        "general.TimeLockGroup",
        models.SET_NULL,
        from_fields=("version", "time_lock_group_id"),
        to_fields=("version", "time_lock_group_id"),
        null=True,
        serialize=False,
    )
    time_change = models.DateTimeField(db_column="timechange", blank=True, null=True)
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_sales_packets",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_sales_packets",
    )

    class Meta:
        db_table = "salespackets"
        constraints = [
            ForeignReferencesConstraint(
                "general.DeviceClassGroup",
                name="r_191",
                from_fields=("version", "device_class_group_id"),
                to_fields=("version", "device_class_group_id"),
            ),
            ForeignReferencesConstraint(
                "general.StationGroup",
                name="r_197",
                from_fields=("version", "start_station_group_id"),
                to_fields=("version", "station_group_id"),
            ),
            ForeignReferencesConstraint(
                "general.StationGroup",
                name="r_198",
                from_fields=("version", "dest_station_group_id"),
                to_fields=("version", "station_group_id"),
            ),
            ForeignReferencesConstraint(
                "general.StationGroup",
                name="r_200",
                from_fields=("version", "sales_station_group_id"),
                to_fields=("version", "station_group_id"),
            ),
            ForeignReferencesConstraint(
                "general.TimeLockGroup",
                name="r_201",
                from_fields=("version", "time_lock_group_id"),
                to_fields=("version", "time_lock_group_id"),
            ),
        ]

    def __str__(self):
        return f"{self.description} [{self.version},{self.packet_id}]"


class SalesPacketElements(models.Model):
    """
    This table will group several tickets together into a 'Sales Packet'.

    There are several fields in this table to set up purchase rules
    and production Information.
    """

    class PACKAGEVARIABLES(models.IntegerChoices):
        # - Values for single elements:
        REQUIRED_SINGLE = 0, "Required Single Element"
        OPT_SINGLE_CUST = 1, "Optional Single Element / Customer counts"
        OPT_SINGLE_CALC = 3, "Optional Single Element / Calculated Count"
        # - Values for Grouping
        REQUIRED_GROUP = 10, "Required Group"
        OPT_GROUP_CUST = 20, "Optional Group / Customer counts"
        OPT_GROUP_CALC = 21, "Optional Group / Calculated Count"
        GROUP_ELEMENT = 2, "Group element of Group Type 10, 20, 21"

    pk = models.CompositePrimaryKey("version", "packet_id", "package_sort_count")
    version = models.ForeignKey(
        "general.TariffVersions",
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="sales_packet_elements",
    )
    packet_id = models.IntegerField(
        db_column="packetid", help_text="Unique ID of a salespacket"
    )
    packet = models.ForeignObject(
        SalesPackets,
        models.PROTECT,
        from_fields=("version", "packet_id"),
        to_fields=("version", "packet_id"),
        related_name="sales_packet_elements",
    )

    package_sort_count = models.IntegerField(
        db_column="packagesortcount", help_text="0 - Primary ticketType, 1,2,3..."
    )
    production_id = models.IntegerField(
        db_column="productionid",
        blank=True,
        null=True,
        help_text="To make this entry unique",
    )
    package_variable = models.IntegerField(
        db_column="packagevariable", blank=True, null=True, choices=PACKAGEVARIABLES
    )
    ticket_type_id = models.IntegerField(
        db_column="tickettypeid",
        blank=True,
        null=True,
        help_text="Unique id of this ticket type",
    )
    ticket_type = models.ForeignObject(
        TicketType,
        models.SET_NULL,
        from_fields=("version", "ticket_type_id"),
        to_fields=("version", "ticket_type_id"),
        related_name="sales_packet_elements",
    )

    start_station_id = models.IntegerField(
        db_column="startstationid",
        blank=True,
        null=True,
        help_text="ID of Zone,Station or Connection",
    )
    start_station_type = models.IntegerField(
        db_column="startstationtype", blank=True, null=True
    )
    start_station = models.ForeignObject(
        "general.ZoneStation",
        models.SET_NULL,
        from_fields=("version", "start_station_id", "start_station_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="start_zonestation_set",
    )

    validity_id = models.IntegerField(db_column="validityid", blank=True, null=True)
    validity = models.ForeignObject(
        "general.Validity",
        models.SET_NULL,
        from_fields=("version", "validity_id"),
        to_fields=("version", "validity_id"),
    )

    dest_station_id = models.IntegerField(
        db_column="deststationid",
        blank=True,
        null=True,
        help_text="ID of Zone,Station or Connection",
    )
    dest_station_type = models.IntegerField(
        db_column="deststationtype", blank=True, null=True
    )
    dest_station = models.ForeignObject(
        "general.ZoneStation",
        models.SET_NULL,
        from_fields=("version", "dest_station_id", "dest_station_type"),
        to_fields=("version", "zone_station_id", "type"),
        related_name="dest_zonestation_set",
    )

    quantity = models.IntegerField(
        blank=True,
        null=True,
        help_text="sets the quantity to produce this Article in a packet",
    )
    description = models.CharField(max_length=50, blank=True, help_text="Description")
    multimedia_group_id = models.IntegerField(
        db_column="multimediagroupid",
        blank=True,
        null=True,
        help_text="Unique identification and link to a Multimedia Group",
    )
    parent_sales_packet_id = models.IntegerField(
        db_column="parentsalespacketid",
        blank=True,
        null=True,
        help_text="Unique ID of a salespacket",
    )
    parent_package_sort_count = models.IntegerField(
        db_column="parentpackagesortcount",
        blank=True,
        null=True,
        help_text="This element is a child record that belongs to a element "
        "with this PacketSortCount",
    )
    parent_package = models.ForeignObject(
        "self",
        models.SET_NULL,
        from_fields=("version", "parent_sales_packet_id", "parent_package_sort_count"),
        to_fields=("version", "packet_id", "package_sort_count"),
        related_name="children",
        null=True,
    )

    salesparam1 = models.IntegerField(
        db_column="salesparam1",
        blank=True,
        null=True,
        help_text="parameter used by application for sale",
    )
    salesparam2 = models.IntegerField(
        db_column="salesparam2",
        blank=True,
        null=True,
        help_text="parameter used by application for sale",
    )
    salesparam3 = models.IntegerField(
        db_column="salesparam3",
        blank=True,
        null=True,
        help_text="parameter used by application for sale",
    )
    salesparam4 = models.IntegerField(
        db_column="salesparam4",
        blank=True,
        null=True,
        help_text="parameter used by application for sale",
    )
    salesparam5 = models.IntegerField(
        db_column="salesparam5",
        blank=True,
        null=True,
        help_text="parameter used by application for sale",
    )
    salesparam6 = models.IntegerField(
        db_column="salesparam6",
        blank=True,
        null=True,
        help_text="parameter used by application for sale",
    )
    salesparam7 = models.IntegerField(
        db_column="salesparam7",
        blank=True,
        null=True,
        help_text="parameter used by application for sale",
    )
    salesparam8 = models.IntegerField(
        db_column="salesparam8",
        blank=True,
        null=True,
        help_text="parameter used by application for sale",
    )
    salesparam9 = models.CharField(
        db_column="salesparam9",
        max_length=50,
        blank=True,
        help_text="parameter used by application for sale",
    )
    salesparam10 = models.CharField(
        db_column="salesparam10",
        max_length=50,
        blank=True,
        help_text="parameter used by application for sale",
    )

    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    time_change = models.DateTimeField(db_column="timechange", blank=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_sales_packet_elements",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_sales_packet_elements",
    )

    class Meta:
        db_table = "salespacketelements"
        constraints = [
            ForeignReferencesConstraint(
                "tariff.TicketType",
                name="r_196",
                from_fields=("version", "ticket_type_id"),
                to_fields=("version", "ticket_type_id"),
            ),
            ForeignReferencesConstraint(
                "tariff.SalesPackets",
                name="r_199",
                from_fields=("version", "packet_id"),
                to_fields=("version", "packet_id"),
            ),
            ForeignReferencesConstraint(
                "general.ZoneStation",
                name="r_223",
                from_fields=("version", "dest_station_id", "dest_station_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                "general.ZoneStation",
                name="r_224",
                from_fields=("version", "start_station_id", "start_station_type"),
                to_fields=("version", "zone_station_id", "type"),
            ),
            ForeignReferencesConstraint(
                "tariff.SalesPacketElements",
                name="r_258",
                from_fields=(
                    "version",
                    "parent_sales_packet_id",
                    "parent_package_sort_count",
                ),
                to_fields=("version", "packet_id", "package_sort_count"),
            ),
            ForeignReferencesConstraint(
                "general.Validity",
                name="r_545",
                from_fields=("version", "validity_id"),
                to_fields=("version", "validity_id"),
            ),
        ]

    def __str__(self):
        return self.description


class SalesPacketsGroup(models.Model):
    """
    The major reason for this table is to group special event sales packet
    into one subject group.

    The TSM application creates screens for special events dynamically.
    So it has to know which sales packet belongs to the group 'Beach Getaways'
    for example.

    These groups are maintained in this table.
    """

    class TYPES(models.IntegerChoices):
        NORMAL = 0, "Normal Group (Special Events)"
        OTHER = 1, "All Other Groups"

    pk = models.CompositePrimaryKey("version", "packet_group_id")
    description = models.CharField(max_length=50, blank=True, help_text="Description")
    multimedia_group_id = models.IntegerField(
        db_column="multimediagroupid",
        blank=True,
        null=True,
        help_text="Unique identification of a Multimedia Group",
    )
    packet_group_id = models.IntegerField(
        db_column="packetgroupid",
        help_text="Unique identification of a sales packet group",
    )
    packet_group_type = models.IntegerField(
        db_column="packetgrouptype",
        blank=True,
        null=True,
        help_text="allows a classification of Packet Groups:",
        choices=TYPES,
    )
    sort_order = models.IntegerField(
        db_column="sortorder",
        blank=True,
        null=True,
        help_text="Sort order for showing sales packet group elements "
        "on the application screen.",
    )
    time_change = models.DateTimeField(db_column="timechange", blank=True, null=True)
    time_new = models.DateTimeField(db_column="timenew", blank=True, null=True)
    user_change = models.ForeignKey(
        "users.User",
        db_column="userchange",
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_sales_packets_group",
    )
    user_new = models.ForeignKey(
        "users.User",
        db_column="usernew",
        null=True,
        on_delete=models.SET_NULL,
        related_name="new_sales_packets_group",
    )
    version = models.ForeignKey(
        "general.TariffVersions",
        models.CASCADE,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="sales_packets_group",
    )

    class Meta:
        db_table = "salespacketsgroup"

    def __str__(self):
        return self.description


class SalesPacketsGroupElements(models.Model):
    """A table to link Sales Packets into a Sales Packet Group."""

    pk = models.CompositePrimaryKey("version", "packet_id", "packet_group_id")
    version = models.ForeignKey(
        "general.TariffVersions",
        models.DO_NOTHING,
        db_column="versionid",
        help_text="ID of tariff version",
        related_name="sales_packet_group_elements",
    )
    packet_id = models.IntegerField(
        db_column="packetid", help_text="Unique ID of a salespacket"
    )
    packet = models.ForeignObject(
        SalesPackets,
        models.CASCADE,
        from_fields=("version", "packet_id"),
        to_fields=("version", "packet_id"),
        related_name="sales_packet_group_elements",
    )
    packet_group_id = models.IntegerField(
        db_column="packetgroupid",
        help_text="Unique identification of a sales packet group",
    )
    packet_group = models.ForeignObject(
        SalesPacketsGroup,
        models.CASCADE,
        from_fields=("version", "packet_group_id"),
        to_fields=("version", "packet_group_id"),
        related_name="sales_packet_group_elements",
    )
    sort_order = models.IntegerField(
        db_column="sortorder",
        blank=True,
        null=True,
        help_text="To maintain an order in which the application will show "
        "the sales packets on the screen.(starting with 0)",
    )
    discount_percentage = models.IntegerField(
        db_column="discountpercentage", blank=True, null=True
    )
    parameter_1 = models.IntegerField(
        db_column="parameter1",
        blank=True,
        null=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_2 = models.IntegerField(
        db_column="parameter2",
        blank=True,
        null=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_3 = models.IntegerField(
        db_column="parameter3",
        blank=True,
        null=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_4 = models.IntegerField(
        db_column="parameter4",
        blank=True,
        null=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_5 = models.IntegerField(
        db_column="parameter5",
        blank=True,
        null=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_6 = models.IntegerField(
        db_column="parameter6",
        blank=True,
        null=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_7 = models.IntegerField(
        db_column="parameter7",
        blank=True,
        null=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_8 = models.IntegerField(
        db_column="parameter8",
        blank=True,
        null=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_9 = models.CharField(
        db_column="parameter9",
        max_length=50,
        blank=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )
    parameter_10 = models.CharField(
        db_column="parameter10",
        max_length=50,
        blank=True,
        help_text="Universal parameter used in POScom application (Munich project)"
        " for article reduction)",
    )

    class Meta:
        db_table = "salespacketsgroupelements"
        constraints = [
            ForeignReferencesConstraint(
                "tariff.SalesPackets",
                name="r_324",
                from_fields=("version", "packet_id"),
                to_fields=("version", "packet_id"),
            ),
        ]

    def __str__(self):
        return "SalesPacketsGroupElements: {},{},{}".format(  # noqa: UP032
            self.version,
            self.packet_id,
            self.packet_group_id,
        )
