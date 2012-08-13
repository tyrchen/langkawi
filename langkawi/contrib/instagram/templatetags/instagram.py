from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('instagram_button', button('langkawi/instagram/instagram_button.html'))