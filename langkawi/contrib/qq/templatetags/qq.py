from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('qq_button', button('socialregistration/qq/qq_button.html'))
