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

        import pyramid
        settings = pyramid.threadlocal.get_current_registry().settings
        config_key = 'github.secret_oauth_access_token'
        value = settings[config_key]
        oauth_creds = dict(access_token=value)

        # Try to refresh list of repos only if the user has none.
        if not self.user.all_repos:
            self.user.sync_repos(oauth_creds)


    def make_button(self, username, repo_name):
        # TODO -- Can we use resource_url here?
        link = '/api/%s/%s/toggle' % (username, repo_name)
        click = 'onclick="subscribe(\'%s\')"' % link
        Repo = github2fedmsg.models.Repo
        query = Repo.query.filter(and_(
            Repo.username==username, Repo.name==repo_name))

        repo = query.one()

        if repo.enabled:
            cls, text = "btn-success", "Disable"
        else:
            cls, text = "btn-danger", "Enable"

        return "<button id='%s-%s' class='btn %s' %s>%s</button>" % (
            username, repo_name, cls, click, text)
