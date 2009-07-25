import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

setup(name='jingle',
      version='0.1dev',
      description='jingle',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg zope',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'repoze.bfg',
            'repoze.zodbconn',
            'repoze.tm',
            'ZODB3',
            'repoze.component',
            'formencode',
            'Jinja2',
            ],
      tests_require=[
            'repoze.bfg',
            ],
      test_suite="jingle",
      entry_points = """\
      [paste.app_factory]
      app = jingle.root:app
      """
      )

