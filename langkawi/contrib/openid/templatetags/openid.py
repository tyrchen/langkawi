from django import template


register = template.Library()

@register.inclusion_tag('langkawi/openid/form.html', takes_context=True)
def openid_form(context, provider=None, button=None):
    return {
        'provider': provider,
        'button': button,
        'request': context['request']
    }
    
