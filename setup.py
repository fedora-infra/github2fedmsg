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

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'fedmsg',
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_mako',
    'zope.sqlalchemy',
    'weberror',
    'velruse',
    'tw2.core',
    ]

setup(name='github2fedmsg',
      version='0.3.5',
      description='Pubsubhubbub app that rebroadcasts GH events over fedmsg',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Ralph Bean',
      author_email='rbean@redhat.com',
      url='https://github.com/fedora-infra/github2fedmsg',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='github2fedmsg',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = github2fedmsg:main
      [console_scripts]
      initialize_github2fedmsg_db = github2fedmsg.scripts.initializedb:main
      """,
      )

