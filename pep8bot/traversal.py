from hashlib import md5
import tw2.core as twc

import pep8bot.models
import pep8bot.widgets


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

        query = pep8bot.models.User.query.filter_by(username=key)
        if query.count() != 1:
            raise KeyError("No such user")
        return UserApp(user=query.one())


class ApiApp(object):
    def __getitem__(self, key):
        query = pep8bot.models.User.query.filter_by(username=key)
        if query.count() != 1:
            raise KeyError("No such user")
        return query.one()


class UserApp(pep8bot.widgets.UserProfile):
    __name__ = None
    __parent__ = RootApp


class APISuccess(object):
    def __init__(self, data):
        self.data = data
