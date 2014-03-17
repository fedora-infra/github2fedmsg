from pyramid.threadlocal import get_current_request
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.security import authenticated_userid

from tw2.bootstrap.forms import bootstrap_js
from tw2.bootstrap.forms import bootstrap_css
from tw2.bootstrap.forms import bootstrap_responsive_css
import tw2.core

# TODO -- move this into tw2.bootstrap like tw2.jqplugins.ui
#bootstrap_css = tw2.core.CSSLink(
#    filename="static/bootswatch/united/bootstrap.min.css",
#    modname=__name__,
#)


def when_ready(func):
    """
    Takes a js_function and returns a js_callback that will run
    when the document is ready.
    """
    return tw2.core.js_callback(
        '$(document).ready(function(){' + str(func) + '});'
    )


@subscriber(BeforeRender)
def inject_globals(event):
    request = get_current_request()

    # Expose these as global attrs for our templates
    event['identity'] = authenticated_userid(request)

    # Register bootstrap for injection with the tw2 middleware
    bootstrap_css.inject()
    bootstrap_responsive_css.inject()
    bootstrap_js.inject()

    when_ready(
        "$('.dropdown-toggle').dropdown();"
    )
