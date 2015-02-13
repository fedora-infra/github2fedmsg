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

from sqlalchemy import (
    Table,
    Column,
    Integer,
    DateTime,
    Boolean,
    Unicode,
    ForeignKey,
    and_,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relation,
    backref,
)

import pyramid.threadlocal
import github2fedmsg.traversal
import datetime
from hashlib import sha256
from .jsonifiable import JSONifiable

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base(cls=JSONifiable)
Base.query = DBSession.query_property()

import github2fedmsg.githubutils as gh

org_to_user_mapping = Table(
    'org_to_user_mapping', Base.metadata,
    Column('org_id', Unicode, ForeignKey('users.github_username'), primary_key=True),
    Column('usr_id', Unicode, ForeignKey('users.github_username'), primary_key=True),
)

import logging
log = logging.getLogger("github2fedmsg.models")


class User(Base):
    __tablename__ = 'users'
    username = Column(Unicode, primary_key=True)
    github_username = Column(Unicode, unique=True)
    emails = Column(Unicode, nullable=False)
    full_name = Column(Unicode, nullable=False)
    oauth_access_token = Column(Unicode)
    created_on = Column(DateTime, default=datetime.datetime.now)
    repos = relation('Repo', backref=('user'))

    @property
    def openid_url(self):
        return "http://%s.id.fedoraproject.org/" % self.username

    @property
    def all_repos(self):
        return sum(
            [self.repos] + [org.repos for org in self.organizations],
            [])

    def sync_repos(self, gh_auth):
        """ Ask github about what repos I have and cache that. """
        gh_repos = gh.get_repos(self.github_username, gh_auth)

        # TODO -- fix this.  this is inefficient
        for repo in gh_repos:

            if Repo.query.filter(and_(
                Repo.name==repo['name'],
                Repo.username==self.github_username
            )).count() < 1:
                github2fedmsg.models.DBSession.add(github2fedmsg.models.Repo(
                    user=self,
                    name=unicode(repo['name']),
                    description=unicode(repo['description']),
                    language=unicode(repo['language']),
                ))

        # Refresh my list of organizations.
        if not self.users:
            # Then I am a real User.
            gh_orgs = gh.get_orgs(self.github_username, gh_auth)
            for o in gh_orgs:
                query = User.query.filter(User.github_username==o['login'])
                if query.count() < 1:
                    log.debug("Adding new org %r" % o['login'])
                    organization = User(
                        username="github_org_" + o['login'],
                        github_username=o['login'],
                        full_name='',
                        emails='')
                    DBSession.add(organization)
                else:
                    log.debug("Found prexisting org %r" % o['login'])
                    organization = query.one()

                if self not in organization.users:
                    log.debug("Adding %r to %r" % (
                        self.github_username, organization.github_username))
                    organization.users.append(self)
                    DBSession.flush()
                else:
                    log.debug("Already in %r" % organization.github_username)
        else:
            # I am an organization.  Do not recurse.
            pass

        # Follow up with all my orgs too (they are also "User"s)
        for organization in self.organizations:
            organization.sync_repos(gh_auth)

    @property
    def total_enabled_repos(self):
        return sum([1 for repo in self.repos if repo.enabled])

    @property
    def percent_enabled_repos(self):
        # Avoid division by zero
        if not len(self.repos):
            return 0

        return 100.0 * self.total_enabled_repos / len(self.repos)

    @property
    def avatar(self):
        digest = sha256(self.openid_url).hexdigest()
        return "https://seccdn.libravatar.org/avatar/%s?d=retro" % digest

    @property
    def created_on_fmt(self):
        return str(self.created_on)

    def __getitem__(self, key):
        already_visited = getattr(self, '_visited', False)
        if not already_visited and key == self.github_username:
            self._visited = True
            return self

        for r in self.repos:
            if r.name == key:
                return r

        for o in self.organizations:
            try:
                return o[key]
            except KeyError:
                pass

        raise KeyError(
            "No such repo %r associated with %s" % (key, self.username))

    def repo_by_name(self, repo_name):
        return self[repo_name]

User.__mapper__.add_property('organizations', relation(
    User,
    primaryjoin=User.github_username == org_to_user_mapping.c.org_id,
    secondaryjoin=org_to_user_mapping.c.usr_id == User.github_username,
    secondary=org_to_user_mapping,
    doc="List of this users organizations",
    backref=backref('users', doc="List of this organizations users")
))


class Repo(Base):
    __tablename__ = 'repos'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=False)
    language = Column(Unicode, nullable=False)
    username = Column(Unicode, ForeignKey('users.github_username'))

    enabled = Column(Boolean, default=False)
