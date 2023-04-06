from typing import Any
from ..airplane_category import get_airplane_category
from django import template

register = template.Library()

@register.filter(name="to_category")
def to_category(value: Any) -> str:
    """
    Custom filter for django template, that converts category index to name

    Parameters
    ----------
    value : Any
        Index of the plane category

    Returns
    -------
    str
        Description of the plane category

    """
    return get_airplane_category(value)