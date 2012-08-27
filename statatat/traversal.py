import tw2.core as twc

import statatat.models
import statatat.widgets


def make_root(request):
    return RootApp()


class RootApp(object):
    __name__ = None
    __parent__ = None

    def __getitem__(self, key):
        query = statatat.models.User.query.filter_by(username=key)
        if query.count() == 1:
            return UserApp(user=query.one())

        raise KeyError("No such user.")


class UserApp(statatat.widgets.UserProfile):
    __name__ = None
    __parent__ = RootApp

    @classmethod
    def __getitem__(self, key):
        raise "watwat"
