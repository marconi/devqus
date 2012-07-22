# -*- coding: utf-8 -*-

import redisco

from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)

    redisco.connection_setup(host=settings.get('redis.host', 'localhost'),
                             port=int(settings.get('redis.port', 6379)),
                             db=int(settings.get('redis.db', 0)))

    # init session
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # templating
    config.include('pyramid_jinja2')

    # include app routes
    config.include('devqus.settings')

    config.add_static_view('static', 'static')  # cache_max_age=3600
    config.scan()
    return config.make_wsgi_app()
