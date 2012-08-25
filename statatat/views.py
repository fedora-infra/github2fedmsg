from pyramid.threadlocal import get_current_request
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)

from sqlalchemy.exc import DBAPIError

from moksha.api.widgets import get_moksha_socket

import statatat.models as m


@subscriber(BeforeRender)
def inject_globals(event):
    event['moksha_socket'] = get_moksha_socket(
        get_current_request().registry.settings
    )


@view_config(route_name='home', renderer='index.mak')
def my_view(request):
    print "logged in as", authenticated_userid(request)
    return {}


@view_config(context='velruse.AuthenticationComplete')
def github_login_complete_view(request):
    username = request.context.profile['preferredUsername']

    query = m.User.query.filter_by(username=username)
    if query.count() == 0:
        m.DBSession.add(m.User(username=username))

    headers = remember(request, username)
    # TODO -- how not to hard code this location?
    return HTTPFound(location="/", headers=headers)


@view_config(context='velruse.AuthenticationDenied', renderer='json')
def login_denied_view(request):
    # TODO -- fancy flash and redirect
    return {'result': 'denied'}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location="/", headers=headers)
