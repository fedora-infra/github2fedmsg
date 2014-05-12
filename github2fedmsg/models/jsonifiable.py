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

import datetime
import time

from sqlalchemy.orm import (
    class_mapper,
)
from sqlalchemy.orm.properties import RelationshipProperty


class JSONifiable(object):
    """ A mixin for sqlalchemy models providing a .__json__ method. """

    def __json__(self, seen=None):
        """ Returns a dict representation of the object.

        Recursively evaluates .__json__() on its relationships.
        """

        if not seen:
            seen = []

        properties = list(class_mapper(type(self)).iterate_properties)
        relationships = [
            p.key for p in properties if type(p) is RelationshipProperty
        ]
        attrs = [
            p.key for p in properties if p.key not in relationships
        ]

        d = dict([(attr, getattr(self, attr)) for attr in attrs])

        for attr in relationships:
            d[attr] = self._expand(getattr(self, attr), seen)

        if hasattr(self, 'avatar'):
            d['avatar'] = self.avatar

        # Serialize datetime objects
        for k, v in d.items():
            if isinstance(v, datetime.datetime):
                d[k] = time.mktime(v.timetuple())

        return d

    def _expand(self, relation, seen):
        """ Return the __json__() or id of a sqlalchemy relationship. """

        if hasattr(relation, 'all'):
            relation = relation.all()

        if hasattr(relation, '__iter__'):
            return [self._expand(item, seen) for item in relation]

        if not relation:
            return []

        if type(relation) not in seen:
            return relation.__json__(seen + [type(self)])
        else:
            return self._primary(relation)

    def _primary(self, obj):
        """ This is an ugly hack, and can be done much more nicely by
        introspecting primary keys...
        """

        if hasattr(obj, 'id'):
            return obj.id
        else:
            return obj.username
