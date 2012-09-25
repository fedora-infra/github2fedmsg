from sqlalchemy import (
    Column,
    Integer,
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

import statatat.traversal
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
    widget_configurations = relation('WidgetConfiguration', backref=('user'))
    repos = relation('Repo', backref=('user'))

    def __getitem__(self, key):
        for r in self.repos:
            if r.name == key:
                return r

        raise KeyError("No such repo associated with %s" % self.username)

    def repo_by_name(self, repo_name):
        return self[repo_name]


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
