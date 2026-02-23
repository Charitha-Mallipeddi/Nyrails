from boto3.dynamodb.types import TypeDeserializer


class ItemDeserializer:
    _deserializer: TypeDeserializer

    def __init__(self):
        self._deserializer = TypeDeserializer()

    def deserialize(self, item):
        return {k: self._deserializer.deserialize(v) for k, v in item.items()}
