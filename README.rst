github2fedmsg
-------------

A bot broadcasts every action made on your repo hosted on GitHub on the
`fedmsg <http://www.fedmsg.com>`_ message bus.

It is a web application that monitors GitHub repositories you subscribe it to.
When new actions (commits, pull-request, tickets) are made, it broadcasts a
message on the `fedmsg`_ message bus.

It is written in Python on the Pyramid framework, and uses `velruse
<http://velruse.rtfd.org>`_ to talk with GitHub.  It adds a webhook callback
back to itself on repositories you ask it to monitor.  When one of those
callbacks fire, github2fedmsg republishes the message it receives to the
`fedmsg`_ bus.

Hacking
-------

If you run into trouble with these instructions, feel free to open a ticket
or get in touch with me directly.

Fork and clone the following two repositories:

 - http://github.com/fedora-infra/github2fedmsg

Using `virtualenvwrapper <pypi.python.org/pypi/virtualenvwrapper>`_::

  $ cd github2fedmsg
  $ mkvirtualenv github2fedmsg
  $ python setup.py develop
  $ pip install waitress

Go off and `register your development application with GitHub
<https://github.com/settings/applications>`_.  Save the oauth tokens and add
the secret one to a new file you create called ``secret.ini``.  Use the example
``secret.ini.example`` file.


Create the database::

  $ initialize_github2fedmsg_db development.ini


Now, start the webapp::

  $ workon github2fedmsg
  $ pserve development.ini --reload
