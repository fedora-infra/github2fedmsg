from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
#from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import authenticated_userid
from sqlalchemy import engine_from_config

import pyramid_mako

import ConfigParser
import os

import github2fedmsg.models
import github2fedmsg.traversal
import github2fedmsg.custom_openid

# TODO -- replace this with pyramid_beaker
crappy_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
authn_policy = AuthTktAuthenticationPolicy(secret='verysecret')
#authz_policy = ACLAuthorizationPolicy()


def get_user(request):
    """ A utility property hanging on 'request' """
    username = authenticated_userid(request)
    query = github2fedmsg.models.User.query.filter_by(username=username)
    if username and query.count() > 0:
        return query.one()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # Load secret stuff from secret.ini.
    try:
        default_path = os.path.abspath("secret.ini")
        secret_path = settings.get('secret_config_path', default_path)
        # TODO: There is a better way to log this message than print.
        print "Reading secrets from %r" % secret_path
        parser = ConfigParser.ConfigParser()
        parser.read(secret_path)
        secret_config = dict(parser.items("github2fedmsg"))
        settings.update(secret_config)
        global_settings.update(secret_config)
    except Exception as e:
        # TODO: There is a better way to log this message than print.
        print 'Failed to load secret.ini.  Reason: %r' % str(e)

    engine = engine_from_config(settings, 'sqlalchemy.')
    github2fedmsg.models.DBSession.configure(bind=engine)

    config = Configurator(
        settings=settings,
        root_factory=github2fedmsg.traversal.make_root,
        session_factory=crappy_session_factory,
        authentication_policy=authn_policy,
        #authorization_policy=authz_policy,
    )

    # Make it so we can do "request.user" in templates.
    config.set_request_property(get_user, 'user', reify=True)

    config.include('pyramid_mako')
    config.add_mako_renderer('.mak')

    config.include('velruse.providers.github')
    config.add_github_login_from_settings()

    config.include('velruse.providers.openid')
    github2fedmsg.custom_openid.add_openid_login(
        config,
        realm=settings.get('velruse.openid.realm'),
        identity_provider=settings.get('velruse.openid.identifier'),
    )


    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('logout', '/logout')
    config.add_route('webhook', '/webhook')
    config.add_route('forget_github_token', '/forget_github_token')
    config.scan()
    return config.make_wsgi_app()
