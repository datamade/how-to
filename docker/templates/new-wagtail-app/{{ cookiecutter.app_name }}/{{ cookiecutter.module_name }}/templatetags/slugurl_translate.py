from django import template
from wagtail.models import Page

register = template.Library()


# Alternative to slugurl which uses chosen or default language for language
@register.simple_tag()
def slugurl_translate(slug):
    page = Page.objects.filter(slug=slug).first()

    if page:
        return page.localized.specific.url
    else:
        return slug
