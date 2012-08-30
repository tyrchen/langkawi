from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('douban_button', button('langkawi/douban/douban_button.html'))
