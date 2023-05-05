from typing import Any
from django import template
from datetime import datetime

register = template.Library()

@register.filter(name="timestamp_to_datetime")
def to_category(value: Any) -> str:
    """
    Custom filter for django template, that converts timestamp to datetime representation.

    Parameters
    ----------
    value : Any
        Timestamp.

    Returns
    -------
    str
        String representation of timestamp.

    """
    return datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M")