# -*- coding: utf-8 -*-

import simplejson as json

from pyramid.events import BeforeRender, NewRequest, subscriber, NewResponse
from pyramid.i18n import get_localizer, TranslationStringFactory
from pyramid.threadlocal import get_current_request
from pyramid.httpexceptions import HTTPForbidden
from pyramid.exceptions import ConfigurationError

from devqus.libs import helpers


tsf = TranslationStringFactory('devqus')


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request = event.get('request')
    if request is None:
        request = get_current_request()

    globs = dict(h=helpers)

    if request is not None:
        globs['_'] = request.translate
        globs['localizer'] = request.localizer
        try:
            globs['session'] = request.session
        except ConfigurationError:
            pass

    def url(*args, **kwargs):
        """ route_url shorthand """
        return request.route_url(*args, **kwargs)

    globs['url'] = url
    event.update(globs)


@subscriber(NewRequest)
def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)

    def auto_translate(string, **kwargs):
        return localizer.translate(tsf(string, **kwargs))

    request.localizer = localizer
    request.translate = auto_translate
