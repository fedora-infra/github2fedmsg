import tw2.core as twc

import statatat.models
import statatat.widgets


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

        query = statatat.models.User.query.filter_by(username=key)
        if query.count() != 1:
            raise KeyError("No such user")
        return UserApp(user=query.one())


class ApiApp(object):
    def __getitem__(self, key):
        query = statatat.models.User.query.filter_by(username=key)
        if query.count() != 1:
            raise KeyError("No such user")
        return query.one()


class UserApp(statatat.widgets.UserProfile):
    __name__ = None
    __parent__ = RootApp

    @classmethod
    def __getitem__(self, key):
        if key == 'new':
            return statatat.widgets.NewWidgetWidget(user=self.user)

        # I dunno about this yet.. what is this app going to do?
        raise NotImplementedError("The stuff below this needs thinking over..")
        suffix = '.widget'
        if key.endswith(suffix):
            # Visiting /username/my_widget produces a user page detailing the
            # widget, what options it has, displaying it...  Visiting
            # /username/my_widget.widget produces the embeddable version.
            chrome = False
            key = key[:-len(suffix)]

        for conf in self.user.widget_configurations:
            if conf.name == key:
                return statatat.widgets.make_widget(conf, chrome)

        raise KeyError("No such widget %r" % key)


class APISuccess(object):
    def __init__(self, data):
        self.data = data
