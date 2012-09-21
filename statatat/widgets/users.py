import tw2.core as twc

from hashlib import md5

from pygithub3 import Github
gh = Github()

class UserProfile(twc.Widget):
    template = "mako:statatat.widgets.templates.profile"
    user = twc.Param("An instance of the User SQLAlchemy model.")

    # These get filled in just before the widget is displayed.
    gh_user = twc.Variable()
    gh_repos = twc.Variable()

    def prepare(self):
        """ Query github for some information before display """
        self.gh_user = gh.users.get(self.user.username)
        # Sort repos alphabetically by name
        self.gh_repos = sorted(
            gh.repos.list(self.user.username).all(),
            lambda x, y: cmp(x.name.lower(), y.name.lower()),
        )

        topics = [
            "%s.%s" % ('author', md5(email).hexdigest())
            for email in self.user.emails.split(',')
        ]

    def make_button(self, repo_name):
        # TODO -- actually implement this by checking the DB or checking for the
        # hook.
        link = 'http://github.com/%s/%s/admin/hooks#generic_minibucket' % (
            self.user.username, repo_name)
        click = 'onclick="window.open(\'%s\', \'_blank\');"' % link
        return "<button class='btn btn-success' %s>Enable</button>" % click

        #import random
        #if random.random() > 0.5:
        #    return "<button class='btn btn-success' %s>Enable</button>" % click
        #else:
        #    return "<button class='btn btn-danger' %s>Disable</button>" % click
