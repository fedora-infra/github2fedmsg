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


@view_config(route_name='home', renderer='index.mak')
def home(request):
    if request.user:
        return HTTPFound(location=request.user.username)
    return {}


@view_config(name='sync', context=m.User, renderer='json')
def sync_user(request):
    # TODO -- someday, learn how to do the __acls__ thing.. :/
    username = request.context.username
    userid = authenticated_userid(request)
    if userid != username:
        raise HTTPUnauthorized()

    config_key = 'github.secret_oauth_access_token'
    value = request.registry.settings[config_key]
    oauth_creds = dict(access_token=value)

    import transaction
    request.context.sync_repos(oauth_creds)
    transaction.commit()
    home = request.route_url('home')
    raise HTTPFound(home + username)


@view_config(context="tw2.core.widgets.WidgetMeta",
             renderer='widget.mak')
def widget_view(request):
    return dict(widget=request.context)
