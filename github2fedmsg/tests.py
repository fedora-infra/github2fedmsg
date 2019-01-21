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

import unittest
import transaction

from pyramid import testing
from sqlalchemy import create_engine

from .models import DBSession, Base, Repo
from .views import home, widget_view

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            repo = Repo(name='testrepo', description="Test Repo", language="cobol")
            DBSession.add(repo)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_home(self):
        request = testing.DummyRequest()
        request.user = None
        result = home(request)
        self.assertEqual(result, {})

    def test_widget_view(self):
        request = testing.DummyRequest()
        request.user = None
        result = widget_view(request)
        self.assertEqual(result, {'widget': None})
