import mistune
from django import template

register = template.Library()


@register.filter
def markdown(value):
    return mistune.markdown(value)
