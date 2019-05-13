import math
from django import template

register = template.Library()


@register.filter
def ceil(value):
    return math.ceil(value)
