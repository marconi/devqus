# -*- coding: utf-8 -*-

import os
import pkg_resources
from scss import Scss

from pyramid.settings import asbool


def scss(request, path):
    settings = request.registry.settings
    cache = asbool(settings['css_cache'])
    compress = asbool(settings['css_compress'])
    new_css_filename = 'local.css'

    asset_path = pkg_resources.resource_filename('devqus', 'static' + path)
    asset_prefix = os.path.dirname(path)
    new_path = os.path.join(os.path.dirname(asset_path), new_css_filename)

    asset_modified = int(os.stat(asset_path).st_mtime)
    assetc_modified = None
    if os.path.exists(new_path):
        assetc_modified = int(os.stat(new_path).st_mtime)

    # if the asset has changed recently than the compiled one,
    # then we know it has been modified.
    if not assetc_modified or asset_modified > assetc_modified:

        # Create parser object
        scss_compiler = Scss(scss_opts={'compress': compress,
                                        'cache': cache})
        asset = scss_compiler.compile(open(asset_path).read())

        f = open(new_path, 'w')
        f.write(asset)
        f.close()

    less_asset = os.path.join(asset_prefix, new_css_filename)
    return assets_url(request, less_asset)


def assets_url(request, path):
    """ Return a versioned URL for an asset.

    The versioning scheme consists in basing the version number upon the file's
    last modified time and appending it to the given path as a query string.
    """
    asset_path = pkg_resources.resource_filename('devqus', 'static' + path)
    modified = int(os.stat(asset_path).st_mtime)
    return "%s?v=%d" % (request.static_url('devqus:static' + path), modified)
