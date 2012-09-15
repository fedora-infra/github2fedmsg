import tw2.core as twc

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
