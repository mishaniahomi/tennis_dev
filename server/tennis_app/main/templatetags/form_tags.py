from django import template
from main.models import PriceList, Photo

register = template.Library()


@register.simple_tag()
def get_pricelist(kind):
    return PriceList.objects.filter(item_type=kind, is_active=True)


@register.simple_tag()
def get_photoes():
    return Photo.objects.all()


@register.simple_tag()
def get_active_photo():
    return Photo.objects.all()[0]

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={'class': css})
