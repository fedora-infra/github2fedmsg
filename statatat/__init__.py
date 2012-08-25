from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
#from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from .models import DBSession

# TODO -- replace this with pyramid_beaker
crappy_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
authn_policy = AuthTktAuthenticationPolicy(secret='verysecret')
#authz_policy = ACLAuthorizationPolicy()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(
        settings=settings,
        session_factory=crappy_session_factory,
        authentication_policy=authn_policy,
        #authorization_policy=authz_policy,
    )

    config.include('velruse.providers.github')
    config.add_github_login_from_settings()

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()

