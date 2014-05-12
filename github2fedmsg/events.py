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

from pyramid.threadlocal import get_current_request
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.security import authenticated_userid

import tw2.core


def when_ready(func):
    """
    Takes a js_function and returns a js_callback that will run
    when the document is ready.
    """
    return tw2.core.js_callback(
        '$(document).ready(function(){' + str(func) + '});'
    )


@subscriber(BeforeRender)
def inject_globals(event):
    request = get_current_request()

    # Expose these as global attrs for our templates
    event['identity'] = authenticated_userid(request)

    when_ready(
        "$('.dropdown-toggle').dropdown();"
    )
