from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('tumblr_button', button('langkawi/tumblr/tumblr_button.html'))
