from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('linkedin_button', button('langkawi/linkedin/linkedin_button.html'))