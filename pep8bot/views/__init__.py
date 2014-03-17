from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized, HTTPForbidden

import pep8bot.models as m
from sqlalchemy import and_

import datetime
import hashlib
import hmac
import requests

import json

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
    return {}


@view_config(route_name='docs', renderer='docs.mak')
def docs(request):
    return {}


@view_config(route_name='webhook', request_method="POST", renderer='string')
def webhook(request):
    """ Handle github webhook. """

    github_secret = request.registry.settings.get("github.secret")

    if 'payload' in request.params:
        hex = hmac.new(github_secret, request.body, hashlib.sha1).hexdigest()
        valid_sig = "sha1=%s" % hex

        if not 'X-Hub-Signature' in request.headers:
            msg = "No X-Hub-Signature provided"
            raise HTTPUnauthorized(msg)

        actual_sig = request.headers['X-Hub-Signature']

        if actual_sig != valid_sig:
            msg = "Invalid X-Hub-Signature"
            raise HTTPForbidden(msg)

        payload = request.params['payload']
        payload = json.loads(payload)

        import pprint
        print " ** RECEIVED THIS FROM GITHUB ** "
        pprint.pprint(payload)

        # TODO -- extract a smart topic from the payload.
        fedmsg.publish(
            modname="github",
            topic='wat',
            msg=payload,
        )
    else:
        raise NotImplementedError()

    return "OK"


@view_config(context=m.Commit, renderer='commit.mak')
def view_commit(request):
    return dict(commit=request.context)


@view_config(name='sync', context=m.User, renderer='json')
def sync_user(request):
    # TODO -- someday, learn how to do the __acls__ thing.. :/
    userid = authenticated_userid(request)
    if userid != request.context.username:
        raise HTTPUnauthorized()

    import transaction
    request.context.sync_repos()
    transaction.commit()
    raise HTTPFound('/' + request.context.username)


@view_config(name='toggle', context=m.Repo, renderer='json')
def repo_toggle_enabled(request):
    # TODO -- someday, learn how to do the __acls__ thing.. :/
    userid = authenticated_userid(request)
    if userid != request.context.username:
        if userid not in [
            member.username for member in request.context.user.users
        ]:
            raise HTTPUnauthorized()

    possible_kinds = ['pep8', 'pylint', 'pyflakes', 'mccabe']
    possible_attrs = ['%s_enabled' % kind for kind in possible_kinds]

    kind = request.GET.get('kind')
    if kind not in possible_kinds:
        raise ValueError("%r not in %r" % (kind, possible_kinds))

    attr = '%s_enabled' % kind

    repo = request.context

    should_notify_github = False
    # If we had *no* attributes on *before* toggling, then *subscribe*.
    if not any([getattr(repo, a) for a in possible_attrs]):
        should_notify_github = True

    # Toggle that attribute on our db model.
    setattr(repo, attr, not getattr(repo, attr))

    # If we had *no* attributes on *after* toggling, then *unsubscribe*.
    if not any([getattr(repo, a) for a in possible_attrs]):
        should_notify_github = True

    if should_notify_github:
        token = repo.user.oauth_access_token
        if not token and repo.user.users:
            token = repo.user.users[0].oauth_access_token

        data = {
            "access_token": token,
            "hub.mode": ['unsubscribe', 'subscribe'][getattr(repo, attr)],
            # TODO -- use our real url
            "hub.callback": "http://pep8.me/webhook",
            "hub.secret": request.registry.settings.get("github.secret"),
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

    response = {
        'status': 'ok',
        'repo': request.context.__json__(),
        'user': repo.user.username,
        'kind': kind,
    }
    response.update(dict(zip(
        possible_attrs,
        [getattr(request.context, a) for a in possible_attrs]
    )))
    return response


@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)
