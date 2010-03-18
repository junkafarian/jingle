from repoze.bfg.view import static, bfg_view
from jinja2 import Environment, PackageLoader
from webob import Response

from models import Root, Page

def render_properties_to_jinja(template, properties):
    output = []
    output.append(u'{%% extends "%s" %%}' % template)
    for key, content in properties.items():
        output.append('{%% block %s %%}%s{%% endblock %%}' % (key.replace('.', '__'), content))
    return '\n'.join(output)

env = Environment(loader=PackageLoader('jingle', 'templates'))


static_view = static('static')

@bfg_view(for_=Root)
def create_page_get(context, request):
    return Response()

@bfg_view(for_=Root, request_type='POST')
def create_page_post(context, request):
    data = request.POST
    page = Page(data['title'])
    page.layout_template = u'master.html'
    for behaviour in data.getall('behaviour'):
        page.update(behaviour, data, behaviour + '.')
    context[data['uid']] = page
    return Response('Successfully Updated')

@bfg_view(for_=Page)
def view_page(context, request):
    string = render_properties_to_jinja(context.layout_template, context.properties)
    template = env.from_string(string)
    return Response(template.render())
