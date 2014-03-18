import tw2.core as twc
import github2fedmsg.models
from sqlalchemy import and_


class UserProfile(twc.Widget):
    template = "mako:github2fedmsg.widgets.templates.profile"
    user = twc.Param("An instance of the User SQLAlchemy model.")
    resources = [
        twc.JSLink(filename="static/profile.js"),
    ]

    show_buttons = twc.Param("show my buttons?", default=False)

    def prepare(self):
        """ Query github for some information before display """

        oauth_creds = dict(access_token=self.user.oauth_access_token)

        # Try to refresh list of repos only if the user has none.
        if self.user.github_username and \
           self.user.oauth_access_token and \
           not self.user.all_repos:
            self.user.sync_repos(oauth_creds)


    def make_button(self, repo):
        # TODO -- Can we use resource_url here?
        username = repo.user.username
        github_username = repo.user.github_username
        link = '/api/%s/%s/%s/toggle' % (username, github_username, repo.name)
        click = 'onclick="subscribe(\'%s\')"' % link

        if repo.enabled:
            cls, text = "btn-success", "On"
        else:
            cls, text = "btn-default", "Off"

        return "<button id='%s-%s' class='btn %s' %s>%s</button>" % (
            github_username, repo.name, cls, click, text)
