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

from hashlib import md5
import tw2.core as twc

import github2fedmsg.models
import github2fedmsg.widgets
from pyramid.security import authenticated_userid


def make_root(request):
    return RootApp(request)


class RootApp(dict):
    __name__ = None
    __parent__ = None

    def __init__(self, request):
        dict.__init__(self)
        self.request = request
        self.static = dict(
            api=ApiApp(),
        )

    def __getitem__(self, key):
        if key in self.static:
            return self.static[key]

        query = github2fedmsg.models.User.query.filter_by(username=key)
        if query.count() != 1:
            raise KeyError("No such user")

        user = query.one()

        # TODO -- use __acl__ machinery some day
        userid = authenticated_userid(self.request)
        # TODO -- check if this is an org that I own
        show_buttons = (userid == user.username)
        return UserApp(user=user, show_buttons=show_buttons)


class ApiApp(object):
    def __getitem__(self, key):
        query = github2fedmsg.models.User.query.filter_by(username=key)
        if query.count() != 1:
            raise KeyError("No such user")
        return query.one()


class UserApp(github2fedmsg.widgets.UserProfile):
    __name__ = None
    __parent__ = RootApp

    @classmethod
    def __getitem__(self, key):
        for repo in self.user.repos:
            if repo.name == key:
                return repo

        raise KeyError


class APISuccess(object):
    def __init__(self, data):
        self.data = data
