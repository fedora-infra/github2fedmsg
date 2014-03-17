github2fedmsg
-------------

A bot broadcasts every action made on your repo hosted on github on the
`fedmsg <http://www.fedmsg.com>`_ message bus.

Status:  *Pre-Alpha*.

It is a webapp that monitors github repositories you subscribe it to.  When
new actions (commits, pull-request, tickets) are made, it brodcasts a message
on the `fedmsg`_ message bus.

It is written in Python on the Pyramid framework, and uses `velruse
<http://velruse.rtfd.org>`_ to talk with github.  It adds a webhook callback
back to itself on repositories you ask it to monitor.  When one of those
callbacks fire, github2fedmsg adds a work item to a redis queue with `retask
<http://retask.rtfd.org>`_.

A separate worker process picks tasks off the redis queue to perform the
fork, clone, tidy, push, pull-request work flow.

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

Go off and `register your development application with github
<https://github.com/settings/applications>`_.  Save the oauth tokens and add the
secret one to a new file you create called ``github2fedmsg/githubsecrets.py``::

    secret_oauth_token = "SECRET_STRING_GOES_HERE"

Now, in two different terminals, start the webapp and the worker process.  In
the first::

  $ workon github2fedmsg
  $ pserve development.ini

In the second::

  $ workon github2fedmsg
  $ python github2fedmsg/worker.py
