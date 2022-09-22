import os

from django.shortcuts import render
from django.views.generic import TemplateView


class ReactView(TemplateView):
    title = "React Page"
    template_name = "{{ cookiecutter.module_name }}/react_page.html"
    component = "js/App.js"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


def robots_txt(request):
    return render(
        request,
        "{{ cookiecutter.module_name }}/robots.txt",
        {"ALLOW_CRAWL": True if os.getenv("ALLOW_CRAWL") == "True" else False},
        content_type="text/plain",
    )


def page_not_found(
    request, exception, template_name="{{ cookiecutter.module_name }}/404.html"
):
    return render(request, template_name, status=404)


def server_error(request, template_name="{{ cookiecutter.module_name }}/500.html"):
    return render(request, template_name, status=500)
