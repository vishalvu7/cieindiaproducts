from django import template

register = template.Library()

@register.filter
def indent(value, depth):
    indentation = '&mdash;' * (depth - 1) if depth > 0 else ''
    return f"{indentation}{value}"
