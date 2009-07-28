from repoze.bfg.view import static, bfg_view
from jinja2 import Environment, PackageLoader
from webob import Response

from jingle.config import DEFAULT_PAGE_BEHAVIOUR
from models import Root, Page

def render_properties_to_jinja(template, properties):
    output = []
    output.append(u'{%% extends "%s" %%}' % template)
    for key, content in properties.items():
        output.append('{%% block %s %%}%s{%% endblock %%}' % (key.replace('.', '__'), content))
    return '\n'.join(output)

env = Environment(loader=PackageLoader('jingle', 'templates'))


static_view = static('static')

@bfg_view(for_=Page)
def view_page(context, request):
    string = render_properties_to_jinja('master.html', context.properties)
    template = env.from_string(string)
    return Response(template.render())
