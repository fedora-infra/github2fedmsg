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
import pep8bot.traversal
import datetime
from hashlib import md5
from .jsonifiable import JSONifiable

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base(cls=JSONifiable)
Base.query = DBSession.query_property()

#from pygithub3 import Github
#gh = Github()


org_to_user_mapping = Table(
    'org_to_user_mapping', Base.metadata,
    Column('org_id', Unicode, ForeignKey('users.username'), primary_key=True),
    Column('usr_id', Unicode, ForeignKey('users.username'), primary_key=True),
)

import logging
log = logging.getLogger("pep8bot.models")


class User(Base):
    __tablename__ = 'users'
    username = Column(Unicode, primary_key=True)
    emails = Column(Unicode, nullable=False)
    full_name = Column(Unicode, nullable=False)
    oauth_access_token = Column(Unicode)
    created_on = Column(DateTime, default=datetime.datetime.now)
    repos = relation('Repo', backref=('user'))

    @property
    def all_repos(self):
        print "*" * 40
        print len(self.repos)
        print len(self.organizations)
        return sum(
            [self.repos] + [org.repos for org in self.organizations],
            [])

    def sync_repos(self):
        """ Ask github about what repos I have and cache that. """
        if self.users:
            # Then I am an organization, not a user.
            gh_repos = gh.repos.list_by_org(self.username).all()
        else:
            # Then I am a real boy
            gh_repos = gh.repos.list(self.username).all()

        # TODO -- fix this.  this is inefficient
        for repo in gh_repos:
            if Repo.query.filter(and_(
                Repo.name==repo.name,
                Repo.username==self.username
            )).count() < 1:
                pep8bot.models.DBSession.add(pep8bot.models.Repo(
                    user=self,
                    name=unicode(repo.name),
                    description=unicode(repo.description),
                    language=unicode(repo.language),
                ))

        # Refresh my list of organizations.
        if not self.users:
            # Then I am a real User.
            gh_orgs = gh.orgs.list(self.username).all()
            for o in gh_orgs:
                query = User.query.filter(User.username==o.login)
                if query.count() < 1:
                    log.debug("Adding new org %r" % o.login)
                    organization = User(
                        username=o.login, full_name='', emails='')
                    DBSession.add(organization)
                else:
                    log.debug("Found prexisting org %r" % o.login)
                    organization = query.one()

                if self not in organization.users:
                    log.debug("Adding %r to %r" % (
                        self.username, organization.username))
                    organization.users.append(self)
                    DBSession.flush()
                else:
                    log.debug("Already in %r" % organization.username)
        else:
            # I am an organization.  Do not recurse.
            pass

        # Follow up with all my orgs too (they are also "User"s)
        for organization in self.organizations:
            organization.sync_repos()

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
        email = self.emails.split(',')[0]
        digest = md5(email).hexdigest()
        return "http://www.gravatar.com/avatar/%s" % digest

    @property
    def created_on_fmt(self):
        return str(self.created_on)

    def __getitem__(self, key):
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

    def widget_link(self):
        prefix = pyramid.threadlocal.get_current_request().resource_url(None)
        tmpl = "{prefix}widget/{username}/embed.js" + \
            "?width=400&height=55&duration=1600&n=100"
        link = tmpl.format(prefix=prefix, username=self.username)
        return "<script type='text/javascript' src='%s'></script>" % link

User.__mapper__.add_property('organizations', relation(
    User,
    primaryjoin=User.username == org_to_user_mapping.c.org_id,
    secondaryjoin=org_to_user_mapping.c.usr_id == User.username,
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
    username = Column(Unicode, ForeignKey('users.username'))
    commits = relation('Commit', backref=('repo'))

    #
    pep8_enabled = Column(Boolean, default=False)
    pylint_enabled = Column(Boolean, default=False)
    pyflakes_enabled = Column(Boolean, default=False)
    mccabe_enabled = Column(Boolean, default=False)

    def __getitem__(self, key):
        if key != 'commits':
            raise KeyError

        class DynamicCommitIndex(object):
            def __getitem__(shmelf, key):
                for commit in self.commits:
                    if commit.sha == key:
                        return commit

                raise KeyError

        return DynamicCommitIndex()


    @property
    def enabled(self):
        return (
            self.pep8_enabled or
            self.pylint_enabled or
            self.pyflakes_enabled or
            self.mccabe_enabled
        )

class Commit(Base):
    __tablename__ = 'commits'
    id = Column(Integer, primary_key=True)
    status = Column(Unicode(20), nullable=False)
    sha = Column(Unicode(40), nullable=False)
    url = Column(Unicode, nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)
    repo_id = Column(Unicode, ForeignKey('repos.id'))

    pep8_error_count = Column(Integer)
    pep8_errors = Column(Unicode)
    pylint_error_count = Column(Integer)
    pylint_errors = Column(Unicode)
    pyflakes_error_count = Column(Integer)
    pyflakes_errors = Column(Unicode)
    mccabe_complexity = Column(Integer)
