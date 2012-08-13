from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('github_button', button('langkawi/github/github_button.html'))