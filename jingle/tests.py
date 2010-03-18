import unittest

from repoze.bfg import testing

class InternalFunctionalTests(unittest.TestCase):
    def test_schema_registration(self):
        from copy import deepcopy
        from formencode.validators import UnicodeString
        from jingle.schemas import Schema
        from jingle.schemas import registry
        class TestSchema(Schema):
            behaviour = 'test'
            title = UnicodeString(default=u'', not_empty=True)
        
        # this gets populated when the application is initialised so no we can use it directly for testing
        self.failUnless(isinstance(registry.lookup('test'), TestSchema))
        self.failUnless('title' in registry.lookup('test').fields)
        

from nose.tools import assert_true, with_setup
from webtest import TestApp
from os.path import dirname, join

config_path = join(dirname(dirname(__file__)), 'etc', 'test.ini')
app = TestApp('config:' + config_path)
registry = app.app.application.application.registry

def test_reset_root():
    from repoze.bfg.interfaces import ISettings
    settings = registry.getUtility(ISettings)
    
    from repoze.zodbconn.finder import PersistentApplicationFinder
    from jingle.models import AppMaker, Root
    get_root = PersistentApplicationFinder(settings.get('zodb_uri'), lambda x: AppMaker('test')(x, reset=True))
    environ = {}
    root = get_root(environ)
    assert_true(
        isinstance(root, Root),
        u'root object should be a Root() object'
    )
    del environ


