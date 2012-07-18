# -*- coding: utf-8 -*-

from sqlalchemy import engine_from_config

from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings

from .apps.common.models import DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)

    # init session
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # templating
    config.include('pyramid_jinja2')

    # include app routes
    config.include('devqus.settings')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()
