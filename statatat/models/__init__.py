from sqlalchemy import (
    Column,
    Integer,
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

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
Base.query = DBSession.query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    emails = Column(Text, nullable=False)
    widget_configurations = relation('WidgetConfiguration', backref=('user'))


class WidgetConfiguration(Base):
    __tablename__ = 'widget_configurations'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
