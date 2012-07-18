

INSTALLED_APPS = (
    'devqus.apps.common',
)

def includeme(config):
    for app in INSTALLED_APPS:
        config.include('%s.urls' % app)
