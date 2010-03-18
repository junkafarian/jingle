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
        



