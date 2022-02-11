from django.shortcuts import render
from django.views.generic import TemplateView


class HelloReact(TemplateView):
    title = 'Hello React View'
    template_name = '{{ cookiecutter.module_name }}/hello_react.html'
    component = 'js/hello-react.js'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


def page_not_found(request, exception, template_name='{{ cookiecutter.module_name }}/404.html'):
    return render(request, template_name, status=404)


def server_error(request, template_name='{{ cookiecutter.module_name }}/500.html'):
    return render(request, template_name, status=500)
