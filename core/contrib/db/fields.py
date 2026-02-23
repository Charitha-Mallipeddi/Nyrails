import decimal
from typing import Any

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.fields import DecimalField


class DecimalIntField(DecimalField):
    """
    A DecimalField that stores as an integer.
    """

    base_multiplier = 0

    def __init__(
        self,
        verbose_name=None,
        name=None,
        max_digits=10,
        decimal_places=None,
        **kwargs,
    ):
        if decimal_places is not None and decimal_places >= 0:
            max_digits = 10 - decimal_places
            self.base_multiplier = int("1" + ("0" * decimal_places))

        super().__init__(verbose_name, name, max_digits, decimal_places, **kwargs)

    def get_internal_type(self):
        return "IntegerField"

    def from_db_value(
        self, value: Any, expression: Any, connection: BaseDatabaseWrapper
    ) -> decimal.Decimal:
        return value / self.base_multiplier

    def get_db_prep_save(self, value: Any, connection: BaseDatabaseWrapper) -> Any:
        if isinstance(value, decimal.Decimal):
            value = round(value * self.base_multiplier)
        return super().get_db_prep_save(value, connection)
