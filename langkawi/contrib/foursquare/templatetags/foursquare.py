from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('foursquare_button', button('langkawi/foursquare/foursquare_button.html'))
