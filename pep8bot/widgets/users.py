import tw2.core as twc
import pep8bot.models
import pyramid.threadlocal

from pygithub3 import Github
gh = Github()


class UserProfile(twc.Widget):
    template = "mako:pep8bot.widgets.templates.profile"
    user = twc.Param("An instance of the User SQLAlchemy model.")
    resources = [
        twc.JSLink(filename="static/profile.js"),
    ]

    # These get filled in just before the widget is displayed.
    gh_user = twc.Variable()
    gh_repos = twc.Variable()

    def prepare(self):
        """ Query github for some information before display """

        # TODO -- don't call this on every page load, only when asked.
        #self.user.sync_repos()

    def make_button(self, repo_name):
        # TODO -- Can we use resource_url here?
        link = '/api/%s/%s/toggle' % (self.user.username, repo_name)
        click = 'onclick="subscribe(\'%s\')"' % link
        if self.user.repo_by_name(repo_name).enabled:
            cls, text = "btn-success", "Disable"
        else:
            cls, text = "btn-danger", "Enable"

        return "<button id='%s' class='btn %s' %s>%s</button>" % (
            repo_name, cls, click, text)
