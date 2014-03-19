from pyramid.threadlocal import get_current_request
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.security import authenticated_userid

import tw2.core


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

    when_ready(
        "$('.dropdown-toggle').dropdown();"
    )
