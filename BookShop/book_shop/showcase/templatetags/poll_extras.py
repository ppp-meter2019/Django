from django import template

register = template.Library()

@register.filter
def new_price(old_price , percent):
    return round(old_price * ((100 - percent)/100),1)
