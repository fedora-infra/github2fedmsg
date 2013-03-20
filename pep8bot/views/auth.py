from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)

import pep8bot.models as m


@view_config(context='velruse.AuthenticationComplete')
def github_login_complete_view(request):
    username = request.context.profile['preferredUsername']
    full_name = request.context.profile['displayName']
    emails = request.context.profile['emails'] or []
    emails = ','.join((item['value'] for item in emails if item['value']))

    query = m.User.query.filter_by(username=username)
    if query.count() == 0:
        m.DBSession.add(m.User(
            username=username,
            full_name=full_name,
            emails=emails,
        ))

    user = query.one()

    # TODO -- how to update the users emails if they change them on github

    headers = remember(request, username)

    request.session['token'] = request.context.credentials['oauthAccessToken']

    # Also save this in the db so our worker can use it later.
    user.oauth_access_token = request.session['token']

    # TODO -- how not to hard code this location?
    return HTTPFound(location="/" + username, headers=headers)


@view_config(context='velruse.AuthenticationDenied', renderer='json')
def login_denied_view(request):
    # TODO -- fancy flash and redirect
    return {'result': 'denied'}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location="/", headers=headers)
