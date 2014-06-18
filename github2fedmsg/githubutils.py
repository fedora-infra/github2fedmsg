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

""" Tools for querying github.

I tried using pygithub3, but it really sucks.
"""

import requests


def _link_field_to_dict(field):
    """ Utility for ripping apart github's Link header field.
    It's kind of ugly.
    """

    if not field:
        return dict()

    return dict([
        (
            part.split('; ')[1][5:-1],
            part.split('; ')[0][1:-1],
        ) for part in field.split(', ')
    ])


def get_repos(username, auth):
    """ username should be a string
    auth should be a tuple of username and password.

    item can be one of "repos" or "orgs"
    """

    tmpl = "https://api.github.com/users/{username}/repos?per_page=100"
    url = tmpl.format(username=username)
    return _getter(url, auth)

def get_orgs(username, auth):
    tmpl = "https://api.github.com/users/{username}/orgs?per_page=100"
    url = tmpl.format(username=username)
    return _getter(url, auth)


def _getter(url, auth):
    """ Pagination utility.  Obnoxious. """

    results = []
    link = dict(next=url)
    while 'next' in link:

        if isinstance(auth, tuple):
            # Is it a (username, password) tuple?
            kwargs = dict(auth=auth)
        elif isinstance(auth, dict):
            # Or, is it an oauth bearer token?
            kwargs = dict(params=auth)
        else:
            raise TypeError("No clue how to handle github auth obj: %r" % auth)

        response = requests.get(link['next'], **kwargs)

        # And.. if we didn't get good results, just bail.
        if response.status_code != 200:
            raise IOError(
                "Non-200 status code %r; %r; %r" % (
                    response.status_code, url, response.json))

        if callable(response.json):
            # Newer python-requests
            results += response.json()
        else:
            # Older python-requests
            results += response.json

        link = _link_field_to_dict(response.headers.get('link', None))

    return results

if __name__ == '__main__':
    # Little test.
    import getpass
    username = raw_input("GitHub Username: ")
    password = getpass.getpass()

    results = get_all(username, (username, password))
    print len(results), "repos found."
