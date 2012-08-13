from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('twitter_button', button('langkawi/twitter/twitter_button.html'))