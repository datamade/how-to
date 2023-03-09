from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = '{{cookiecutter.module_name}}/index.html'


{% if cookiecutter.include_react %}
class ReactView(TemplateView):
    title = "React Page"
    template_name = "{{ cookiecutter.module_name }}/react_page.html"
    component = "js/App.js"
{% endif %}


def page_not_found(request, exception, template_name='{{cookiecutter.module_name}}/404.html'):
    return render(request, template_name, status=404)


def server_error(request, template_name='{{cookiecutter.module_name}}/500.html'):
    return render(request, template_name, status=500)


def robots_txt(request):
    return render(
        request,
        "{{ cookiecutter.module_name }}/robots.txt",
        {"ALLOW_CRAWL": True if os.getenv("ALLOW_CRAWL") == "True" else False},
        content_type="text/plain",
    )
