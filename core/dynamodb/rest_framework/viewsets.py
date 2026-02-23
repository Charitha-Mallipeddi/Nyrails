

from core.dynamodb.rest_framework.generic import GenericDynamoDbViewSet
from rest_framework.mixins import ListModelMixin


class DynamoDbViewSet(ListModelMixin, GenericDynamoDbViewSet):
    """A viewset that provides default list() actions."""
    pass
