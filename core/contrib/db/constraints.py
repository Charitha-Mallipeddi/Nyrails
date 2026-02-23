from django.apps import apps
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.models import Model
from django.db.models.constants import LOOKUP_SEP
from django.db.models.constraints import BaseConstraint
from django.db.utils import DEFAULT_DB_ALIAS

__all__ = ["ForeignReferencesConstraint"]


class ForeignReferencesConstraint(BaseConstraint):  # noqa: PLW1641
    def __init__(  # noqa: PLR0913
        self,
        to: str,
        name,
        from_fields=(),
        to_fields=(),
        deferrable=None,
        violation_error_code=None,
        violation_error_message=None,
    ):
        if not name:
            error_msg = "A foreign reference constraint must be named."
            raise ValueError(error_msg)
        if not to:
            error_msg = (
                "ForeignReferencesConstraint.to is required "
                "to define a foreign reference."
            )
            raise ValueError(error_msg)
        if not from_fields:
            error_msg = (
                "ForeignReferencesConstraint.from_fields is required "
                "to define a foreign reference"
            )
            raise ValueError(error_msg)
        if not to_fields:
            error_msg = (
                "ForeignReferencesConstraint.to_fields is "
                "required to define a foreign reference"
            )
            raise ValueError(error_msg)
        if not isinstance(to, (str, Model)):
            error_msg = (
                "ForeignReferencesConstraint.to must be a string or a model instance."
            )
            raise TypeError(error_msg)
        if not isinstance(from_fields, (list, tuple)):
            error_msg = (
                "ForeignReferencesConstraint.from_fields must be a list or tuple."
            )
            raise TypeError(error_msg)
        if not isinstance(to_fields, (list, tuple)):
            error_msg = "ForeignReferencesConstraint.to_fields must be a list or tuple."
            raise TypeError(error_msg)
        self.to = to
        self.from_fields = tuple(from_fields)
        self.to_fields = tuple(to_fields)
        self.deferrable = deferrable
        super().__init__(
            name=name,
            violation_error_code=violation_error_code,
            violation_error_message=violation_error_message,
        )

    def check(self, model, connection):
        errors = model._check_local_fields({*self.from_fields}, "constraints")  # noqa: SLF001
        required_db_features = model._meta.required_db_features  # noqa: SLF001

        if self.deferrable is not None and not (
            connection.features.supports_deferrable_unique_constraints
            or "supports_deferrable_unique_constraints" in required_db_features
        ):
            errors.append(
                checks.Warning(
                    f"{connection.display_name} does not support deferrable unique "
                    "constraints.",
                    hint=(
                        "A constraint won't be created. Silence this warning if you "
                        "don't care about it."
                    ),
                    obj=model,
                    id="models.W038",
                )
            )

        references = set()

        errors.extend(self._check_references(model, references))
        return errors

    def _check_references(self, model, references):
        from django.db.models.fields.composite import (  # noqa: PLC0415
            CompositePrimaryKey,
        )

        errors = []
        fields = set()
        for field_name, *lookups in references:
            # pk is an alias that won't be found by opts.get_field().
            if field_name != "pk" or isinstance(model._meta.pk, CompositePrimaryKey):  # noqa: SLF001
                fields.add(field_name)
            if not lookups:
                # If it has no lookups it cannot result in a JOIN.
                continue
            try:
                if field_name == "pk":
                    field = model._meta.pk  # noqa: SLF001
                else:
                    field = model._meta.get_field(field_name)  # noqa: SLF001
                if not field.is_relation or field.many_to_many or field.one_to_many:
                    continue
            except FieldDoesNotExist:
                continue
            # JOIN must happen at the first lookup.
            first_lookup = lookups[0]
            if (
                hasattr(field, "get_transform")
                and hasattr(field, "get_lookup")
                and field.get_transform(first_lookup) is None
                and field.get_lookup(first_lookup) is None
            ):
                errors.append(
                    checks.Error(
                        "'constraints' refers to the joined field "
                        f"'{LOOKUP_SEP.join([field_name, *lookups])}'.",
                        obj=model,
                        id="models.E041",
                    )
                )
        errors.extend(model._check_local_fields(fields, "constraints"))  # noqa: SLF001
        return errors

    def constraint_sql(
        self, model: type[Model] | None, schema_editor: BaseDatabaseSchemaEditor
    ) -> str:
        to_model = apps.get_model(self.to)
        from_columns = [
            model._meta.get_field(field_name).column  # noqa: SLF001
            for field_name in self.from_fields
        ]
        to_columns = [
            to_model._meta.get_field(field_name).column  # noqa: SLF001
            for field_name in self.to_fields
        ]
        sql_constraint_fk = (
            "CONSTRAINT %(name)s FOREIGN KEY (%(column)s) "
            "REFERENCES %(to_table)s (%(to_column)s)%(on_delete_db)s%(deferrable)s"
        )
        return sql_constraint_fk % {
            "table": schema_editor.quote_name(model._meta.db_table),  # noqa: SLF001
            "name": self.name,
            "column": ", ".join(from_columns),
            "to_table": to_model._meta.db_table,  # noqa: SLF001
            "to_column": ", ".join(to_columns),
            "deferrable": "",
            "on_delete_db": "",
        }

    def create_sql(
        self, model: type[Model] | None, schema_editor: BaseDatabaseSchemaEditor | None
    ) -> str:
        to_model = apps.get_model(self.to)
        from_columns = [
            model._meta.get_field(field_name).column  # noqa: SLF001
            for field_name in self.from_fields
        ]
        to_columns = [
            to_model._meta.get_field(field_name).column  # noqa: SLF001
            for field_name in self.to_fields
        ]
        if schema_editor:
            return schema_editor.sql_create_fk % {
                "table": schema_editor.quote_name(model._meta.db_table),  # pyright: ignore[reportOptionalMemberAccess]  # noqa: SLF001
                "name": self.name,
                "column": ", ".join(from_columns),
                "to_table": to_model._meta.db_table,  # noqa: SLF001
                "to_column": ", ".join(to_columns),
                "deferrable": "",
                "on_delete_db": "",
            }
        return ""

    def remove_sql(self, model, schema_editor):
        if not schema_editor:
            return ""
        return schema_editor.sql_delete_fk % {
            "table": schema_editor.quote_name(model._meta.db_table),  # pyright: ignore[reportOptionalMemberAccess]  # noqa: SLF001
            "name": self.name,
        }

    def __repr__(self):
        return "<{}:{}{}{}{}{}{}>".format(
            self.__class__.__qualname__,
            "" if not self.to else f" to={self.to!r}",
            "" if not self.to_fields else f" to_fields={self.to_fields!r}",
            "" if not self.from_fields else f" from_fields={self.from_fields!r}",
            f" name={self.name!r}",
            (
                ""
                if self.violation_error_code is None
                else f" violation_error_code={self.violation_error_code}"
            ),
            (
                ""
                if self.violation_error_message is None
                or self.violation_error_message == self.default_violation_error_message
                else f" violation_error_message={self.violation_error_message}"
            ),
        )

    def __eq__(self, other):
        if isinstance(other, ForeignReferencesConstraint):
            return (
                self.name == other.name
                and self.to == other.to
                and self.from_fields == other.from_fields
                and self.to_fields == other.to_fields
                and self.violation_error_code == other.violation_error_code
                and self.violation_error_message == other.violation_error_message
            )
        return super().__eq__(other)

    def deconstruct(self):
        path, args, kwargs = super().deconstruct()
        kwargs["to"] = self.to
        if self.to_fields:
            kwargs["to_fields"] = self.to_fields
        if self.from_fields:
            kwargs["from_fields"] = self.from_fields
        return path, args, kwargs

    def validate(self, model, instance, exclude=None, using=DEFAULT_DB_ALIAS):
        pass
