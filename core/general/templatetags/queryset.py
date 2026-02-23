from django import template

register = template.Library()


@register.filter
def int_to_decimal(value):
    """
    Returns the value of the specified key from the given dictionary.
    Usage: {{ dictionary|get_item:key }}
    """
    return value / 100


@register.filter
def order_by(queryset, order_string):
    """
    Sorts a queryset by the specified order string(s).
    Usage: {% for item in items|order_by:"field_name" %}
    or with multiple fields: {% for item in items|order_by:"field_name,-other_field" %}
    """
    args = [x.strip() for x in order_string.split(",")]
    return queryset.order_by(*args)
