from django import template
from mpastats.models import Coverage

register = template.Library()

@register.simple_tag
def globalcoverage():
    return Coverage.objects.first()
