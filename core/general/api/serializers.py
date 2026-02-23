from rest_framework.serializers import ModelSerializer

from core.general.models import ZoneStation


class StationBasicSerializer(ModelSerializer):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = ZoneStation
        fields = ["description"]
