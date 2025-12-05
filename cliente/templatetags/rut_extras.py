from django import template

register = template.Library()

@register.filter
def format_rut(value):
    if not value:
        return ''
    s = str(value)
    if len(s) < 2:
        return s
    body = s[:-1]
    dv = s[-1]
    return f"{body}-{dv}"
