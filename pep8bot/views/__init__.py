from pyramid.view import view_config
from pyramid.security import authenticated_userid

import pep8bot.models as m

import datetime
from hashlib import md5
import requests

import json
import retask.task
import retask.queue

# http://developer.github.com/v3/repos/hooks/
github_api_url = "https://api.github.com/hub"
github_events = [
    "push",
    #"issues",
    #"issue_comment",
    "pull_request",
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
    return {
    }


@view_config(route_name='webhook', request_method="POST", renderer='string')
def webhook(request):
    """ Handle github webhook. """

    # TODO -- check X-Hub-Signature

    salt = "TODO MAKE THIS SECRET"

    if 'payload' in request.params:
        payload = request.params['payload']
        if isinstance(payload, basestring):
            payload = json.loads(payload)

        # Drop a note in our db about it
        user = m.User.query.filter_by(
            username=payload['repository']['owner']['name']).one()
        repo = m.Repo.query.filter_by(
            name=payload['repository']['name'],
            username=payload['repository']['owner']['name'],
        ).one()

        for commit in payload['commits']:
            if m.Commit.query.filter_by(sha=commit['id']).count() > 0:
                continue
            m.DBSession.add(m.Commit(
                status="pending",
                sha=commit['id'],
                message=commit['message'],
                timestamp=datetime.datetime.strptime(
                    commit['timestamp'][:-6],  # strip timezone.. :/
                    "%Y-%m-%dT%H:%M:%S",
                ),
                url=commit['url'],
                repo=repo,
                # TODO -- sort this out.  what if author isn't in pep8bot?
                #author=author,
                #committer=committer,
            ))

        # Now, put a note in our work queue for it, too.
        queue = retask.queue.Queue('commits')
        task = retask.task.Task(payload)
        queue.connect()

        # Fire and forget
        job = queue.enqueue(task)

    else:
        raise NotImplementedError()

    return "OK"


@view_config(name='toggle', context=m.Repo, renderer='json')
def repo_toggle_enabled(request):
    repo = request.context
    repo.enabled = not repo.enabled
    data = {
        "access_token": repo.user.oauth_access_token,
        "hub.mode": ['unsubscribe', 'subscribe'][repo.enabled],
        # TODO -- use our real url
        "hub.callback": "http://localhost:6543/webhook",
    }

    for event in github_events:
        data["hub.topic"] = "https://github.com/%s/%s/events/%s" % (
            repo.user.username, repo.name, event)
        # Subscribe to events via pubsubhubbub
        result = requests.post(github_api_url, data=data)

        if result.status_code != 204:
            raise IOError(result.status_code)

    return {
        'status': 'ok',
        'enabled': request.context.enabled,
        'repo': request.context.__json__(),
    }

@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)
