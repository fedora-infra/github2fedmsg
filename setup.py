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
    'alembic',
    'tw2.core',
    ]

setup(name='github2fedmsg',
      version='0.2.2',
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

