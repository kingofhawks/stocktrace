from django.utils.translation import ugettext as _
from django import template
register = template.Library()


@register.filter(name='tag_url')
def tag_url(value):
    if value:
        return '<a href="test">test</a>'
    else:
        return _('No')

