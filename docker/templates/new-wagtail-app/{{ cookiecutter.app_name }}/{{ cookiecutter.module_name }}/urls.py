"""example_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import ReactView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('react-page/', ReactView.as_view(), name='react-page'),
    path("", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Translatable URLs
# These will be available under a language code prefix. For example /en/search/
#
# from django.conf.urls.i18n import i18n_patterns
# from django.views.i18n import JavaScriptCatalog
#
# urlpatterns += i18n_patterns(
#   path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
#   path("", include(wagtail_urls)),
# ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = '{{ cookiecutter.module_name }}.views.page_not_found'
handler500 = '{{ cookiecutter.module_name }}.views.server_error'
