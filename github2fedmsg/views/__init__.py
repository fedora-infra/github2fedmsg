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

import fedmsg

import github2fedmsg.githubutils as gh

# http://developer.github.com/v3/repos/hooks/
github_api_url = "https://api.github.com/hub"
# All events: http://developer.github.com/webhooks/#events
github_events = [
    #"push",            # Any git push to a Repository
    #"commit_comment",  # Any time a Commit is commented on.
    #"create",          # Any time a Repository, Branch, or Tag is created.
    #"delete",          # Any time a Branch or Tag is deleted.
    #"release",          # Any time a Release is published in the Repository.
    #"issues",          # Any time an Issue is opened or closed.
    #"issue_comment",   # Any time an Issue is commented on.
    #"pull_request",    # Any time a Pull Request is opened, closed, or
    #                    # synchronized (updated due to a new push in the
    #                    # branch that the pull request is tracking).
    #"pull_request_review_comment", # Any time a Commit is commented on while
    #                                # inside a Pull Request review (the Files
    #                                # Changed tab).
    #"gollum",          # Any time a Wiki page is updated.
    #"watch",           # Any time a User watches the Repository.
    #"download",        # ?
    #"fork",            # Any time a Repository is forked.
    #"fork_apply",      # ?
    #"member",          # Any time a User is added as a collaborator to a
    #                   # non-Organization Repository.
    #"public",          # Any time a Repository changes from private to public.
    #"status",          # Any time a Repository has a status update from
    #                   # the API.
    #"team_add",        # Any time a team is added or modified on a
    #                   # Repository.
    #"deployment",      # Any time a Repository has a new deployment created
    #                   # from the API.
    #"deployment_status",# Any time a deployment for the Repository has a
    #                   #status update from the API.
    #"page_build",      # Any time a Pages site is built or results in a
    #                   # failed build.
    "*",               # Any time any event is triggered (Wildcard Event).
]


@view_config(route_name='home', renderer='index.mak')
def home(request):
    if request.user:
        return HTTPFound(location=request.user.username)
    return {}


@view_config(route_name='webhook', request_method="POST", renderer='string')
def webhook(request):
    """ Handle github webhook. """

    # TODO -- eventually remove this debugging.
    print "GOT A MESSAGE FROM GITHUB WOWOWOWOW"
    print "here are the headers"
    import pprint
    pprint.pprint(request.headers.items())
    print "and here are the params",
    pprint.pprint(request.params.items())
    # End debugging block

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

        event_type = request.headers['X-Github-Event'].lower()

        # github sends us a 'ping' when we first subscribe to let us know that
        # it worked.
        if event_type == 'ping':
            event_type = 'webhook'

        # Turn just 'issues' into 'issue.reopened'
        if event_type == 'issues':
            event_type = 'issue.' + payload['action']

        # Make issues comments match our scheme more nicely
        if event_type == 'issue_comment':
            event_type = 'issue.comment'

        # TODO -- remove this debugging eventually.
        import pprint
        print " ** RECEIVED THIS FROM GITHUB ** "
        pprint.pprint(payload)

        # Strip out a bunch of redundant information that github sends us
        payload = prune_useless_urls(payload)

        # Build a little table of github usernames to fas usernames so
        # consumers can have an easy time.
        fas_usernames = build_fas_lookup(payload)
        payload['fas_usernames'] = fas_usernames

        fedmsg.publish(
            modname="github",
            topic=event_type,
            msg=payload,
        )
    else:
        raise NotImplementedError()

    return "OK"


def prune_useless_urls(payload):
    """ Given *any* github message, strip out unneeded information. """

    for k, v in payload.items():
        if isinstance(v, dict):
            payload[k] = prune_useless_urls(v)
        elif k.endswith('_url') and k != 'html_url':
            del payload[k]

    return payload

def build_fas_lookup(payload):
    """ Given *any* github message, build a lookup of github usernames to fas
    usernames for it.

    This involves hand coding a bunch of knowledge about github message
    formats.
    """

    usernames = set()

    # Trawl through every possible corner we can to find github usernames
    if 'commits' in payload:
        for commit in payload['commits']:
            usernames.add(commit['committer']['username'])
            usernames.add(commit['author']['username'])

    if 'pusher' in payload:
        usernames.add(payload['pusher']['name'])

    if 'sender' in payload:
        usernames.add(payload['sender']['login'])

    # Take all that, and roll it up into a dict mapping those to FAS
    mapping = {}
    for github_username in usernames:
        if not github_username:
            continue
        user = m.User.query.filter_by(github_username=github_username).first()
        if user:
            mapping[github_username] = user.username

    return mapping


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
    if userid != request.context.user.username:
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
        "hub.callback": request.registry.settings.get("github.callback"),
        "hub.secret": request.registry.settings.get("github.secret"),
    }

    for event in github_events:
        data["hub.topic"] = "https://github.com/%s/%s/events/%s" % (
            repo.user.github_username, repo.name, event)
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
        'username': repo.user.username,
        'github_username': repo.user.github_username,
        'enabled': repo.enabled,
    }
    return response


@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)
