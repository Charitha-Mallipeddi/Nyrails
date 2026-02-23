from rest_framework.serializers import ModelSerializer

from core.general.api.serializers import StationBasicSerializer
from core.tariff.models import SalesPackets
from core.ticket.models import Ticket, TicketScan, TicketSource


class SalesPacketBaseSerializer(ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = SalesPackets
        fields = ("packet_id", "version_id", "description")


class TicketSourceSerializer(ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = TicketSource
        fields = "__all__"


class TicketSerializer(ModelSerializer):
    sales_packet = SalesPacketBaseSerializer(read_only=True)
    from_station = StationBasicSerializer(read_only=True)
    to_station = StationBasicSerializer(read_only=True)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Ticket
        fields = (
            "id",
            "sales_packet",
            "number",
            "amount",
            "count",
            "from_station",
            "to_station",
            "valid_from",
            "valid_to",
        )


class TicketScanSerializer(ModelSerializer):
    source = TicketSourceSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = TicketScan
        fields = (
            "source",
            "ticket",
            "tour_id",
            "conductor_id",
            "train_id",
            "scanned_on",
        )
