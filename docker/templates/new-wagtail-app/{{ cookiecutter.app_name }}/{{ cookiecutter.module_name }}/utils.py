from wagtail.core.models import Page


def get_site_menu():
    """Taken from the CALES app
    https://github.com/datamade/ucb-cales/pull/120/files
    #diff-b59096721a79856b109fac1104ad803e71e68fa4fe2660bf850048a8afe66840"""
    from .models import BasePage
    site_home = Page.objects.type(BasePage).first()
    nav_items = list(site_home.get_children().live().in_menu())

    top_level = [{'page': page, 'url': page.get_url()} for page in nav_items]
    nav_plus_children = [{
        'parent': item,
        'children': list(Page.objects.child_of(item['page']).live().in_menu())}
        for item in top_level]

    return {
        'home_url': site_home.url,
        'menu': [{
            'nav_item': item['parent'],
            'children': [{
              'page': child,
              'url': child.get_url()
            } for child in item['children']]
        } for item in nav_plus_children]
    }
