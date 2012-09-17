from pyramid.view import view_config
from pyramid.security import authenticated_userid


@view_config(route_name='home', renderer='index.mak')
def home(request):
    print "logged in as", authenticated_userid(request)
    return {}


@view_config(route_name='webhook', renderer='string')
def webhook(request):
    """ Handle github webhook. """
    import pprint
    pprint.pprint(request.params)
    return "OK"


@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)
