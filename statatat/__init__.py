from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
#from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import authenticated_userid
from sqlalchemy import engine_from_config

import statatat.models
import statatat.traversal

# TODO -- replace this with pyramid_beaker
crappy_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
authn_policy = AuthTktAuthenticationPolicy(secret='verysecret')
#authz_policy = ACLAuthorizationPolicy()


def get_user(request):
    """ A utility property hanging on 'request' """
    username = authenticated_userid(request)
    query = statatat.models.User.query.filter_by(username=username)
    if username and query.count() > 0:
        return query.one()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    statatat.models.DBSession.configure(bind=engine)
    config = Configurator(
        settings=settings,
        root_factory=statatat.traversal.make_root,
        session_factory=crappy_session_factory,
        authentication_policy=authn_policy,
        #authorization_policy=authz_policy,
    )
    # Make it so we can do "request.user" in templates.
    config.set_request_property(get_user, 'user', reify=True)

    config.include('velruse.providers.github')
    config.add_github_login_from_settings()

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('logout', '/logout')
    config.add_route('webhook', '/webhook')
    config.add_route('stats', '/stats')
    config.scan()
    return config.make_wsgi_app()
