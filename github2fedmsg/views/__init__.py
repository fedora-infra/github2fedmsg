from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized, HTTPForbidden

import github2fedmsg.models as m
from sqlalchemy import and_

import datetime
import hashlib
import hmac
import requests

import json

import github2fedmsg.githubutils as gh

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


@view_config(name='sync', context=m.User, renderer='json')
def sync_user(request):
    # TODO -- someday, learn how to do the __acls__ thing.. :/
    userid = authenticated_userid(request)
    if userid != request.context.username:
        raise HTTPUnauthorized()

    config_key = 'github.secret_oauth_access_token'
    value = request.registry.settings[config_key]
    oauth_creds = dict(access_token=value)

    import transaction
    request.context.sync_repos(oauth_creds)
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

    repo = request.context

    # Toggle that attribute on our db model.
    repo.enabled = not repo.enabled

    # Now notify github
    token = request.user.oauth_access_token

    if not token:
        raise HTTPForbidden("you need to link your account with github first")

    data = {
        "access_token": token,
        "hub.mode": ['unsubscribe', 'subscribe'][repo.enabled],
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
        'enabled': repo.enabled,
    }
    return response


@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)