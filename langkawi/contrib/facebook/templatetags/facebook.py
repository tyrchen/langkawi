from django import template

from langkawi.templatetags import button

register = template.Library()

register.tag('facebook_button', button('langkawi/facebook/facebook_button.html'))