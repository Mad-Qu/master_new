from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.urls import path
from django.conf import settings
import importlib


settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='asd',
)


TEMPLATE = """
<!DOCTYPE html>
<html>
 <head>
  <title>{title}</title>
 </head>
 <body>
  <h2>{module_name}</h2>
  {content}
 </body>
</html> 
"""


def module_handler(request, module_name):
    try:
        name_module = dir(importlib.import_module(module_name))
        name = [name for name in name_module if not name.startswith('_')]
        link = [f'<a href="/doc/{module_name}/{name}">{name}</a><br>'
                for name in name]
        return HttpResponse(TEMPLATE.format(title=f'Модуль {module_name}',
                                            module_name=f'Модуль Python {module_name}',
                                            content=''.join(link)))
    except ModuleNotFoundError:
        return HttpResponseNotFound()


def object_handler(request, module_name, object_name):
    try:
        module = importlib.import_module(module_name)
        object_doc = getattr(module, object_name).__doc__
        return HttpResponse(object_doc, content_type='text/plain')
    except (ModuleNotFoundError, AttributeError):
        return HttpResponseNotFound()


urlpatterns = [
    path('doc/<module_name>', module_handler),
    path('doc/<module_name>/<object_name>', object_handler),
]

if __name__ == '__main__':
    execute_from_command_line()
