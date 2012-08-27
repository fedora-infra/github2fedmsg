from pyramid.view import view_config
from pyramid.security import authenticated_userid


@view_config(route_name='home', renderer='index.mak')
def my_view(request):
    print "logged in as", authenticated_userid(request)
    return {}


@view_config(context="tw2.core.widgets.WidgetMeta", renderer='string')
def widget_view(request):
    return request.context.display()
