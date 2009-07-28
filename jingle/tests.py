import unittest

from repoze.bfg import testing

# class ViewIntegrationTests(unittest.TestCase):
#     """ These tests are integration tests for the view.  These test
#     the functionality the view *and* its integration with the rest of
#     the repoze.bfg framework.  They cause the entire environment to be
#     set up and torn down as if your application was running 'for
#     real'.  This is a heavy-hammer way of making sure that your tests
#     have enough context to run properly, and it tests your view's
#     integration with the rest of BFG.  You should not use this style
#     of test to perform 'true' unit testing as tests will run faster
#     and will be easier to write if you use the testing facilities
#     provided by bfg and only the registrations you need, as in the
#     above ViewTests.
#     """
#     def setUp(self):
#         """ This sets up the application registry with the
#         registrations your application declares in its configure.zcml
#         (including dependent registrations for repoze.bfg itself).
#         """
#         testing.cleanUp()
#         import jingle
#         import zope.configuration.xmlconfig
#         zope.configuration.xmlconfig.file('configure.zcml',
#                                           package=jingle)

#     def tearDown(self):
#         """ Clear out the application registry """
#         testing.cleanUp()

#     def test_my_view(self):
#         from jingle.views import view_page
#         context = testing.DummyModel()
#         request = testing.DummyRequest()
#         result = view_page(context, request)
#         self.assertEqual(result.status, '200 OK')
#         body = result.app_iter[0]
#         self.failUnless('Welcome to' in body)
#         self.assertEqual(len(result.headerlist), 2)
#         self.assertEqual(result.headerlist[0],
#                          ('Content-Type', 'text/html; charset=UTF-8'))
#         self.assertEqual(result.headerlist[1], ('Content-Length',
#                                                 str(len(body))))

class InternalFunctionalTests(unittest.TestCase):
    def test_schema_registration(self):
        from copy import deepcopy
        from formencode.validators import UnicodeString
        from jingle.schemas import Schema
        from jingle.schemas import registry
        class TestSchema(Schema):
            title = UnicodeString(default=u'', not_empty=True)
        
        # this gets populated when the application is initialised so no we can use it directly for testing
        registry.register('test', TestSchema())
        self.failUnless(isinstance(registry.lookup('test'), TestSchema))
        self.failUnless('title' in registry.lookup('test').fields)
        



