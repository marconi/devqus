import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid==1.3.2',
    'SQLAlchemy==0.7.7',
    'transaction==1.3.0',
    'pyramid_tm==0.5',
    'pyramid_debugtoolbar==1.0.2',
    'zope.sqlalchemy==0.7.1',
    'waitress==0.8.1',
    'pyramid_jinja2==1.3',
    'WTForms==1.0.1',
    'pyramid_beaker==0.6.1',
    'pyScss==1.1.3',
    'simplejson==2.5.2',
]

setup(name='devqus',
      version='0.0',
      description='devqus',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='devqus',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = devqus:main
      [console_scripts]
      initialize_devqus_db = devqus.scripts.initializedb:main
      """,
      )
