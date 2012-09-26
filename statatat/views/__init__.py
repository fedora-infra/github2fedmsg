from pyramid.view import view_config
from pyramid.security import authenticated_userid

import statatat.models as m

from hashlib import md5
import requests

import moksha.hub.hub
import json

# http://developer.github.com/v3/repos/hooks/
github_api_url = "https://api.github.com/hub"
github_events = [
    "push",
    #"issues",
    #"issue_comment",
    #"pull_request",
    #"gollum",
    #"watch",
    #"download",
    #"fork",
    #"fork_apply",
    #"member",
    #"public",
    #"status",
]


@view_config(route_name='home', renderer='index.mak')
def home(request):
    return {}


_hub = None
def make_moksha_hub(settings):
    """ Global singleton. """
    global _hub
    if not _hub:
        _hub = moksha.hub.hub.MokshaHub(settings)

    return _hub


@view_config(route_name='webhook', request_method="POST", renderer='string')
def webhook(request):
    """ Handle github webhook. """

    if 'payload' in request.params:
        payload = request.params['payload']
        if isinstance(payload, basestring):
            payload = json.loads(payload)

        hub = make_moksha_hub(request.registry.settings)

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
    else:
        raise NotImplementedError()

    return "OK"


@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)


@view_config(name='toggle', context=m.Repo, renderer='json')
def repo_toggle_enabled(request):
    repo = request.context
    repo.enabled = not repo.enabled
    data = {
        "access_token": request.session['token'],
        "hub.mode": ['unsubscribe', 'subscribe'][repo.enabled],
        # TODO -- use our own callback and not requestb.in
        # ... think over the best pattern for traversal first.
        "hub.callback": "http://statatat.threebean.org/webhook",
    }
    for event in github_events:
        data["hub.topic"] = "https://github.com/%s/%s/events/%s" % (
            repo.user.username, repo.name, event)
        # Subscribe to events via pubsubhubbub
        result = requests.post(github_api_url, data=data)

        # TODO -- handle errors more gracefully.
        assert(result.status_code == 204)

    return {
        'status': 'ok',
        'enabled': request.context.enabled,
        'repo': request.context.__json__(),
    }
