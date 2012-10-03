import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'weberror',
    'velruse',

    'requests <= 0.14.0',
    # This breaks with the latest "requests"
    # https://github.com/copitux/python-github3/issues/26
    'pygithub3',

    'moksha.hub',
    'moksha.wsgi',

    'tw2.core <= 2.1.1',   # only because 2.1.2 is busted
    'tw2.forms <= 2.1.1',  # only because 2.1.2 is busted
    'tw2.bootstrap.forms',
    'tw2.d3',
    ]

setup(name='statatat',
      version='0.0',
      description='statatat',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='statatat',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = statatat:main
      [console_scripts]
      initialize_statatat_db = statatat.scripts.initializedb:main
      """,
      )

