from hashlib import md5
import tw2.core as twc

import github2fedmsg.models
import github2fedmsg.widgets
import pyramid.threadlocal
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
        request = pyramid.threadlocal.get_current_request()
        userid = authenticated_userid(request)
        # TODO -- check if this is an org that I own
        show_buttons = (userid == user.username)
        return UserApp(user=query.one(), show_buttons=show_buttons)


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
