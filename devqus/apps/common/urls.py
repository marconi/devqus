# -*- coding: utf-8 -*-


def includeme(config):
    config.add_route('home', '/')
    config.add_route('stream', '/stream')
    config.add_route('post', '/post')
    config.add_route('socketio', '/socket.io/*remaining')
