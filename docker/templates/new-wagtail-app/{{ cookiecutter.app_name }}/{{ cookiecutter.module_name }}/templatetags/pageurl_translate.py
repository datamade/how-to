from django import template
from wagtail.core.models import Page

register = template.Library()


@register.simple_tag()
def pageurl_translate(slug):
    page = Page.objects.filter(slug=slug).first()

    if page:
        return page.localized.specific.title
    else:
        return slug
