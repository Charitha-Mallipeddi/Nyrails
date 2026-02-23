from django.core.exceptions import ValidationError
from django.forms.fields import Field
from django.forms.widgets import Select
from django_tomselect.widgets import TomSelectModelWidget


class CompositeKeyModelChoiceField(Field):
    """Custom field to handle models with composite primary keys"""

    def __init__(  # noqa: PLR0913
        self,
        queryset,
        required=True,  # noqa: FBT002
        widget=None,
        label=None,
        initial=None,
        help_text="",
        to_field_name=None,
        label_from_instance=None,
        *args,
        **kwargs,
    ):  # Added parameter
        self.queryset = queryset
        self.to_field_name = to_field_name
        self.label_from_instance = label_from_instance  # Store it

        if widget is None:
            widget = Select

        if isinstance(widget, type):
            widget = widget(choices=self.choices)

        super().__init__(
            *args,
            required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            **kwargs,
        )

    def get_label(self, obj):
        """Get label for an object"""
        if self.label_from_instance:
            return self.label_from_instance(obj)
        return str(obj)

    @property
    def choices(self):
        # Create choices with string representation of composite key
        choices = [("", "---------")]
        for obj in self.queryset:
            key = self._obj_to_key(obj)
            label = self.get_label(obj)  # Use custom label
            choices.append((key, label))
        return choices

    def _obj_to_key(self, obj):
        """Convert object to string key"""
        if (
            hasattr(obj, "pk")
            and hasattr(obj.pk, "__iter__")
            and not isinstance(obj.pk, str)
        ):
            # Composite key
            return "|".join(str(v) for v in obj.pk)
        return str(obj.pk)

    def _key_to_obj(self, key):
        """Convert string key back to object"""
        if not key:
            return None

        # Try to find the object
        for obj in self.queryset:
            if self._obj_to_key(obj) == key:
                return obj
        return None

    def clean(self, value):
        if not value and not self.required:
            return None

        obj = self._key_to_obj(value)
        if obj is None and self.required:
            msg = "Select a valid choice."
            raise ValidationError(msg)

        return obj

    def prepare_value(self, value):
        """Prepare value for rendering"""
        if hasattr(value, "pk"):
            return self._obj_to_key(value)
        return value



class CompositeKeyTomSelectWidget(TomSelectModelWidget):
    """Custom TomSelect widget for composite key models"""
    
    def __init__(self, *args, **kwargs):
        self.composite_separator = kwargs.pop('composite_separator', '|')
        super().__init__(*args, **kwargs)
    
    def value_from_datadict(self, data, files, name):
        """Convert composite key string back to object"""
        value = super().value_from_datadict(data, files, name)
        if not value:
            return None
        return value
    
    def format_value(self, value):
        """Format object to composite key string for display"""
        if not value:
            return ''
        
        if hasattr(value, 'pk') and hasattr(value.pk, '__iter__') and not isinstance(value.pk, str):
            return self.composite_separator.join(str(v) for v in value.pk)
        elif hasattr(value, 'pk'):
            return str(value.pk)
        return str(value)
