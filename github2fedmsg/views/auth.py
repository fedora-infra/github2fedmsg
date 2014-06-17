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
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)

import github2fedmsg.models as m


@view_config(context='velruse.AuthenticationComplete')
def login_complete_view(request):
    """ This handles *both* login with FAS and login with github.. """

    # Github gives us:
    #{'accounts': [{'domain': 'github.com',
    #               'userid': 331338,
    #               'username': u'ralphbean'}],
    # 'displayName': u'Ralph Bean',
    # 'emails': [{'value': u'rbean@redhat.com'}],
    # 'preferredUsername': u'ralphbean'}

    # FAS gives us:
    #{'accounts': [{'domain': 'openid.net',
    #               'username': 'http://ralph.id.fedoraproject.org/'}],
    #  'displayName': u'Ralph Bean',
    #  'emails': [u'rbean@redhat.com'],
    #  'name': {'formatted': u'Ralph Bean'},
    #  'preferredUsername': u'ralph'}

    ctx = request.context
    accounts = ctx.profile['accounts']
    home = request.route_url('home')

    if accounts and accounts[0]['domain'] == 'github.com':
        if not request.user:
            # Bad scene.  Someone is trying to link with github.com while not
            # yet being signed in through FAS.  We will just deny this.
            return HTTPForbidden()
        token = ctx.credentials['oauthAccessToken']
        request.user.github_username = ctx.profile['preferredUsername']
        request.user.oauth_access_token = token
        request.session['token'] = token
        return HTTPFound(location=home + request.user.username)

    username = ctx.profile['preferredUsername']
    full_name = ctx.profile['displayName']
    emails = ctx.profile['emails'] or []

    if emails:
        if isinstance(emails[0], dict):
            emails = [item['value'] for item in emails if item['value']]

    emails = ','.join(emails)

    query = m.User.query.filter_by(username=username)
    if query.count() == 0:
        m.DBSession.add(m.User(
            username=username,
            full_name=full_name,
            emails=emails,
        ))

    user = query.one()
    headers = remember(request, username)
    request.session['token'] = user.oauth_access_token
    return HTTPFound(location=home + user.username, headers=headers)


@view_config(context='velruse.AuthenticationDenied', renderer='json')
def login_denied_view(request):
    # TODO -- fancy flash and redirect
    return {'result': 'denied'}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    home = request.route_url('home')
    return HTTPFound(location=home, headers=headers)


@view_config(route_name='forget_github_token')
def forget_github_token(request):
    if 'token' in request.session:
        request.session['token']

    username = request.user.username
    home = request.route_url('home')

    import transaction
    #request.user.github_username = None
    request.user.oauth_access_token = None
    transaction.commit()

    return HTTPFound(location=home + username)
