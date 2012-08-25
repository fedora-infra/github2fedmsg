from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from moksha.api.widgets import get_moksha_socket

from .models import (
    DBSession,
    MyModel,
)


def with_moksha_socket(func):
    """ Decorator that injects a moksha socket. """
    def wrapper(request):
        d = func(request)
        d['moksha_socket'] = get_moksha_socket(request.registry.settings)
        return d
    return wrapper


@view_config(route_name='home', renderer='index.mak')
@with_moksha_socket
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one':one, 'project':'statatat'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_statatat_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(context='velruse.AuthenticationComplete', renderer='json')
def github_login_complete_view(request):
    return {"access": "granted"}

@view_config(context='velruse.AuthenticationDenied', renderer='json')
def login_denied_view(request):
    return {'result': 'denied'}
