from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
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


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    emails = Column(Text, nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.now)
    widget_configurations = relation('WidgetConfiguration', backref=('user'))
    repos = relation('Repo', backref=('user'))

    @property
    def total_enabled_repos(self):
        return sum([1 for repo in self.repos if repo.enabled])

    @property
    def percent_enabled_repos(self):
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

        raise KeyError("No such repo associated with %s" % self.username)

    def repo_by_name(self, repo_name):
        return self[repo_name]

    def widget_link(self):
        prefix = pyramid.threadlocal.get_current_request().resource_url(None)
        tmpl = "{prefix}widget/{username}/embed.js" + \
                "?width=400&height=55&duration=1600&n=100"
        link = tmpl.format(prefix=prefix, username=self.username)
        return "<script type='text/javascript' src='%s'></script>" % link


class Repo(Base):
    __tablename__ = 'repos'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    enabled = Column(Boolean, default=False)


class WidgetConfiguration(Base):
    __tablename__ = 'widget_configurations'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
