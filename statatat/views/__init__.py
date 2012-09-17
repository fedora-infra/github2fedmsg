from pyramid.view import view_config
from pyramid.security import authenticated_userid

import moksha.hub.hub
import json


@view_config(route_name='home', renderer='index.mak')
def home(request):
    print "logged in as", authenticated_userid(request)
    return {}



@view_config(route_name='webhook', renderer='string')
def webhook(request):
    """ Handle github webhook. """

    if 'payload' in request.params:
        payload = request.params['payload']
        if isinstance(payload, basestring):
            payload = json.loads(payload)

        topic = "%s.%s" % (
            payload['repository']['owner']['name'],
            payload['repository']['name']
        )
        hub = moksha.hub.hub.MokshaHub(request.registry.settings)
        hub.send_message(topic=topic, message=payload)

    return "OK"


@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)
