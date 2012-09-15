from pyramid.threadlocal import get_current_request
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.security import authenticated_userid

from moksha.wsgi.widgets.api import get_moksha_socket


@subscriber(BeforeRender)
def inject_globals(event):
    request = get_current_request()
    event['moksha_socket'] = get_moksha_socket(request.registry.settings)
    event['identity'] = authenticated_userid(request)
