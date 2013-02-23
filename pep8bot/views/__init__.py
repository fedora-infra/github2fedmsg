from pyramid.view import view_config
from pyramid.security import authenticated_userid

import pep8bot.models as m
from sqlalchemy import and_

import datetime
from hashlib import md5
import requests

import json
import retask.task
import retask.queue

import pep8bot.githubutils as gh

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
    # TODO -- make this secret
    salt = "TODO MAKE THIS SECRET"

    if 'payload' in request.params:
        payload = request.params['payload']
        if isinstance(payload, basestring):
            payload = json.loads(payload)

        if 'action' not in payload:
            # This is a regular old push.. don't worry about it.
            commits = [c['id'] for c in payload['commits']]
            username = payload['repository']['owner']['name']
            reponame = payload['repository']['name']
            clone_url = "https://github.com/%s/%s/" % (username, reponame)
        else:
            # This is a pull request
            sha = payload['pull_request']['head']['sha']
            commits = [sha]
            username = payload['repository']['owner']['login']
            reponame = payload['repository']['name']
            clone_url = payload['pull_request']['base']['repo']['clone_url']

        # Drop a note in our db about it
        user = m.User.query.filter_by(username=username).one()
        repo = m.Repo.query.filter_by(and_(
            Repo.name==reponame, Repo.username==username)).one()

        template = "https://github.com/%s/%s/commit/%s"

        for sha in commits:
            if m.Commit.query.filter_by(sha=sha).count() > 0:
                continue

            m.DBSession.add(m.Commit(
                status="pending",
                sha=sha,
                url=template % (username, reponame, sha),
                repo=repo,
                # TODO -- sort this out.  what if author isn't in pep8bot?
                #author=author,
                #committer=committer,
            ))

            status = "pending"
            token = user.oauth_access_token
            desc = "PEP8Bot scan pending"
            gh.post_status(username, reponame, sha, status, token, desc)

        # Now, put a note in our work queue for it, too.
        queue = retask.queue.Queue('commits')
        task = retask.task.Task({
            'reponame': reponame,
            'username': username,
            'commits': commits,
            'clone_url': clone_url,
        })
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

    token = repo.user.oauth_access_token
    if not token and repo.user.users:
        token = repo.user.users[0].oauth_access_token

    data = {
        "access_token": token,
        "hub.mode": ['unsubscribe', 'subscribe'][repo.enabled],
        # TODO -- use our real url
        "hub.callback": "http://pep8.me/webhook",
    }


    for event in github_events:
        data["hub.topic"] = "https://github.com/%s/%s/events/%s" % (
            repo.user.username, repo.name, event)
        # Subscribe to events via pubsubhubbub
        result = requests.post(github_api_url, data=data)

        if result.status_code != 204:
            d = result.json
            if callable(d):
                d = d()

            d = dict(d)
            d['status_code'] = result.status_code
            raise IOError(d)

    return {
        'status': 'ok',
        'enabled': request.context.enabled,
        'repo': request.context.__json__(),
    }

@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)
