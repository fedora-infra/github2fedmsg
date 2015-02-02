# This file is a part of github2fedmsg, a pubsubhubbub to zeromq bridge.
# Copyright (C) 2014, Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized, HTTPForbidden

import github2fedmsg.models as m

import fedmsg
import hashlib
import hmac
import json
import requests


# http://developer.github.com/v3/repos/hooks/
github_pubsubhubub_api_url = "https://api.github.com/hub"
# All events: http://developer.github.com/webhooks/#events
github_events = [
    # "push",            # Any git push to a Repository
    # "commit_comment",  # Any time a Commit is commented on.
    # "create",          # Any time a Repository, Branch, or Tag is created.
    # "delete",          # Any time a Branch or Tag is deleted.
    # "release",          # Any time a Release is published in the Repository.
    # "issues",          # Any time an Issue is opened or closed.
    # "issue_comment",   # Any time an Issue is commented on.
    # "pull_request",    # Any time a Pull Request is opened, closed, or
    #                     # synchronized (updated due to a new push in the
    #                     # branch that the pull request is tracking).
    # "pull_request_review_comment", # Any time a Commit is commented on while
    #                                 # inside a Pull Request review (the Files
    #                                 # Changed tab).
    # "gollum",          # Any time a Wiki page is updated.
    # "watch",           # Any time a User watches the Repository.
    # "download",        # ?
    # "fork",            # Any time a Repository is forked.
    # "fork_apply",      # ?
    # "member",          # Any time a User is added as a collaborator to a
    #                    # non-Organization Repository.
    # "public",          # Any time a Repository changes from private to public
    # "status",          # Any time a Repository has a status update from
    #                    # the API.
    # "team_add",        # Any time a team is added or modified on a
    #                    # Repository.
    # "deployment",      # Any time a Repository has a new deployment created
    #                    # from the API.
    # "deployment_status",# Any time a deployment for the Repository has a
    #                    #status update from the API.
    # "page_build",      # Any time a Pages site is built or results in a
    #                    # failed build.
    "*",               # Any time any event is triggered (Wildcard Event).
]


@view_config(route_name='webhook', request_method="POST", renderer='string')
def webhook(request):
    """ Handle github webhook. """

    github_secret = request.registry.settings.get("github.secret")

    hex = hmac.new(github_secret, request.body, hashlib.sha1).hexdigest()
    valid_sig = "sha1=%s" % hex

    if 'X-Hub-Signature' not in request.headers:
        msg = "No X-Hub-Signature provided"
        raise HTTPUnauthorized(msg)

    actual_sig = request.headers['X-Hub-Signature']

    if actual_sig != valid_sig:
        msg = "Invalid X-Hub-Signature"
        raise HTTPForbidden(msg)

    if 'payload' in request.params:
        # pubsubhubbub
        payload = request.params['payload']
        payload = json.loads(payload)
    else:
        # whatever webhooks
        payload = request.json_body

    event_type = request.headers['X-Github-Event'].lower()

    # github sends us a 'ping' when we first subscribe to let us know that
    # it worked.
    if event_type == 'ping':
        event_type = 'webhook'

        # They don't actually tell us which repo is signed up, so, for
        # presentation purposes only, we'll rip out the repo name here and
        # build a nice human-clickable url.
        tokens = payload['hook']['url'].split('/')
        owner, repo = tokens[-4], tokens[-3]
        payload['compare'] = 'https://github.com/%s/%s' % (owner, repo)

    # Turn just 'issues' into 'issue.reopened'
    if event_type == 'issues':
        event_type = 'issue.' + payload['action']

    # Same here
    if event_type == 'pull_request':
        event_type = 'pull_request.' + payload['action']

    # Make issues comments match our scheme more nicely
    if event_type == 'issue_comment':
        event_type = 'issue.comment'

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

    return "OK"


def prune_useless_urls(payload):
    """ Given *any* github message, strip out unneeded information. """

    for k, v in payload.items():
        if k == '_links':
            payload['html_url'] = v['html']['href']
            del payload[k]
        elif isinstance(v, dict):
            payload[k] = prune_useless_urls(v)
        elif k.endswith('_url') and k not in ['html_url', 'target_url']:
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
        if 'login' in payload['sender']:
            usernames.add(payload['sender']['login'])

    if 'forkee' in payload:
        if 'login' in payload['forkee']['owner']:
            usernames.add(payload['forkee']['owner']['login'])

    if 'repository' in payload:
        if 'login' in payload['repository']['owner']:
            usernames.add(payload['repository']['owner']['login'])

    # Take all that, and roll it up into a dict mapping those to FAS
    mapping = {}
    for github_username in usernames:
        if not github_username:
            continue
        user = m.User.query.filter_by(github_username=github_username).first()
        if user:
            mapping[github_username] = user.username

    return mapping


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

    # We used to do this with pubsubhubbub, but not all of github's oauth
    # scopes work there.
    # toggle_pubsubhubbub_hooks(request, repo, token)
    toggle_webhook_directly(request, repo, token)

    response = {
        'status': 'ok',
        'repo': request.context.__json__(),
        'username': repo.user.username,
        'github_username': repo.user.github_username,
        'enabled': repo.enabled,
    }
    return response


def toggle_pubsubhubbub_hooks(request, repo, token):
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
        result = requests.post(github_pubsubhubbub_api_url, data=data)

        if result.status_code < 200 or result.status_code > 299:
            d = result.json()
            d['status_code'] = result.status_code
            raise IOError(d)


def toggle_webhook_directly(request, repo, token):
    actually_enabled = _get_webhook_status_directly(request, repo, token)

    # Here, repo.enabled represents our database knowledge of the hook state.
    # "actually_enabled" represents github's own record keeping.

    if repo.enabled and not actually_enabled:
        _enable_webhook_directly(request, repo, token)
    elif repo.enabled and actually_enabled:
        pass  # nothing to do
    elif not repo.enabled and actually_enabled:
        _disable_webhook_directly(request, repo, actually_enabled, token)
    elif not repo.enabled and not actually_enabled:
        pass  # nothing to do


def _get_webhook_status_directly(request, repo, token):
    auth = {"access_token": token}
    url = "https://api.github.com/repos/%s/%s/hooks" % (
        repo.user.github_username, repo.name)
    result = requests.get(url, params=auth)

    if result.status_code < 200 or result.status_code > 299:
        d = result.json()
        d['status_code'] = result.status_code
        raise IOError(d)

    callback = request.registry.settings.get("github.callback")

    hooks = result.json()
    for hook in hooks:
        if hook['name'] == 'web' and hook['config'].get('url') == callback:
            return hook

    return None


def _enable_webhook_directly(request, repo, token):
    auth = {"access_token": token}
    data = {
        "name": "web",
        "active": True,
        "events": github_events,
        "config": {
            "url": request.registry.settings.get("github.callback"),
            "content_type": "json",
            "secret": request.registry.settings.get("github.secret"),
        },
    }

    headers = {'content-type': 'application/json'}
    url = "https://api.github.com/repos/%s/%s/hooks" % (
        repo.user.github_username, repo.name)
    result = requests.post(
        url, params=auth, data=json.dumps(data), headers=headers)

    if result.status_code < 200 or result.status_code > 299:
        d = result.json()
        d['status_code'] = result.status_code
        raise IOError(d)


def _disable_webhook_directly(request, repo, hook, token):
    auth = {"access_token": token}
    url = "https://api.github.com/repos/%s/%s/hooks/%i" % (
        repo.user.github_username, repo.name, hook['id'])
    requests.delete(url, params=auth)
