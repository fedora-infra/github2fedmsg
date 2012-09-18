from pyramid.threadlocal import get_current_request
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.security import authenticated_userid

from moksha.wsgi.widgets.api import get_moksha_socket

from tw2.bootstrap.forms import bootstrap_responsive_css
import tw2.core

bootstrap_css = tw2.core.CSSLink(
    filename="static/bootswatch/united/bootstrap.min.css",
    modname=__name__,
)


@subscriber(BeforeRender)
def inject_globals(event):
    request = get_current_request()

    # Expose these as global attrs for our templates
    event['moksha_socket'] = get_moksha_socket(request.registry.settings)
    event['identity'] = authenticated_userid(request)

    # Register bootstrap for injection with the tw2 middleware
    bootstrap_css.inject()
    bootstrap_responsive_css.inject()
