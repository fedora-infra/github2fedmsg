from pyramid.view import view_config
from pyramid.security import authenticated_userid

import statatat.models as m

from hashlib import md5
import requests

import moksha.hub.hub
import json


@view_config(route_name='home', renderer='index.mak')
def home(request):
    return {}



@view_config(route_name='webhook', renderer='string')
def webhook(request):
    """ Handle github webhook. """

    if 'payload' in request.params:
        payload = request.params['payload']
        if isinstance(payload, basestring):
            payload = json.loads(payload)

        hub = moksha.hub.hub.MokshaHub(request.registry.settings)

        topic_extractors = {
            'repo': lambda i: payload['repository']['url'],
            'repo_owner': lambda i: payload['repository']['owner']['email'],
            'author': lambda i: payload['commits'][i]['author']['email'],
            'committer': lambda i: payload['commits'][i]['committer']['email'],
        }
        for prefix, extractor in topic_extractors.items():
            for i, commit in enumerate(payload['commits']):
                topic = "%s.%s" % (prefix, md5(extractor(i)).hexdigest())
                hub.send_message(topic=topic, message=commit)

    return "OK"


@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)


@view_config(name='toggle', context=m.Repo, renderer='json')
def repo_toggle_enabled(request):
    repo = request.context
    repo.enabled = not repo.enabled
    event = "push"
    github_url = "https://api.github.com/hub"
    data = {
      "access_token": request.session['token'],
      "hub.mode": ['unsubscribe', 'subscribe'][repo.enabled],
      "hub.topic": "https://github.com/%s/%s/events/%s" % (
          repo.user.username, repo.name, event),
      "hub.callback": "http://requestb.in/15zb0tk1",
    }
    # Subscribe to events via pubsubhubbub
    result = requests.post(github_url, data=data)

    # TODO -- handle errors more gracefully.
    assert(result.status_code == 204)

    return {
        'status': 'ok',
        'enabled': request.context.enabled,
        'repo': request.context.__json__(),
    }
