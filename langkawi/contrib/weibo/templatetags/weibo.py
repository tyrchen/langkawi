from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('weibo_button', button('socialregistration/weibo/weibo_button.html'))
