from typing import Any
from rest_framework.serializers import Serializer
from boto3.dynamodb.types import TypeDeserializer

class DynamoDbSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._deserializer = TypeDeserializer()

    def to_representation(self, instance: Any) -> dict[str, Any]:
        return {k: self._deserializer.deserialize(v) for k, v in instance.items()}
