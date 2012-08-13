from django import template
from langkawi.templatetags import button

register = template.Library()

register.tag('weibo_button', button('langkawi/weibo/weibo_button.html'))
