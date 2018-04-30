from django import template
from main.models import Tag

register = template.Library()

@register.filter(name='tags')
def tags(documento, revisao):
    return Tag.objects.filter(revisao=revisao, fichamentos__documento=documento)

