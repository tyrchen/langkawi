from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('qq_button', button('langkawi/qq/qq_button.html'))
