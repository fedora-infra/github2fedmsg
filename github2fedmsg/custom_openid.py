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

import velruse.api
import velruse.providers.openid as vr

from pyramid.security import NO_PERMISSION_REQUIRED


def add_openid_login(config, realm, identity_provider):
    provider = SingleOpenIDConsumer(
        'openid', 'openid',
        realm=realm,
        identity_provider=identity_provider,
        storage=None,
    )
    login_path='/login/openid'
    callback_path='/login/openid/callback'
    config.add_route(provider.login_route, login_path)
    config.add_view(provider, attr='login', route_name=provider.login_route,
                    permission=NO_PERMISSION_REQUIRED)
    config.add_route(provider.callback_route, callback_path,
                     use_global_views=True,
                     factory=provider.callback)
    velruse.api.register_provider(config, 'openid', provider)


class SingleOpenIDConsumer(vr.OpenIDConsumer):
    def __init__(self,
                 name,
                 _type,
                 realm=None,
                 identity_provider=None,
                 storage=None,
                 context=vr.OpenIDAuthenticationComplete):
        super(SingleOpenIDConsumer, self).__init__(
            name, _type, realm, storage, context)
        self.identity_provider = identity_provider

    def _lookup_identifier(self, request, url):
        return self.identity_provider
