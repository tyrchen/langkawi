from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('renren_button', button('langkawi/renren/renren_button.html'))
