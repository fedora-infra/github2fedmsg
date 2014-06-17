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

import tw2.core as twc
import github2fedmsg.models
import pyramid.threadlocal
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
        home = self.request.route_url('home')
        link = home + 'api/%s/%s/%s/toggle' % (username, github_username, repo.name)
        click = 'onclick="subscribe(\'%s\')"' % link

        if repo.enabled:
            cls, text = "btn-success", "On"
        else:
            cls, text = "btn-default", "Off"

        return "<button id='%s-%s' class='btn %s' %s>%s</button>" % (
            github_username, repo.name, cls, click, text)

    @property
    def request(self):
        return pyramid.threadlocal.get_current_request()
