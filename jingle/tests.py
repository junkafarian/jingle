import unittest

from repoze.bfg import testing

class ViewTests(unittest.TestCase):

    """ These tests are unit tests for the view.  They test the
    functionality of *only* the view.  They register and use dummy
    implementations of repoze.bfg functionality to allow you to avoid
    testing 'too much'"""

    def setUp(self):
        """ cleanUp() is required to clear out the application registry
        between tests (done in setUp for good measure too)
        """
        testing.cleanUp()
        
    def tearDown(self):
        """ cleanUp() is required to clear out the application registry
        between tests
        """
        testing.cleanUp()

    def test_my_view(self):
        from largebluejingle.views import my_view
        context = testing.DummyModel()
        request = testing.DummyRequest()
        renderer = testing.registerDummyRenderer('templates/mytemplate.pt')
        response = my_view(context, request)
        renderer.assert_(project='largeblue.jingle')

class ViewIntegrationTests(unittest.TestCase):
    """ These tests are integration tests for the view.  These test
    the functionality the view *and* its integration with the rest of
    the repoze.bfg framework.  They cause the entire environment to be
    set up and torn down as if your application was running 'for
    real'.  This is a heavy-hammer way of making sure that your tests
    have enough context to run properly, and it tests your view's
    integration with the rest of BFG.  You should not use this style
    of test to perform 'true' unit testing as tests will run faster
    and will be easier to write if you use the testing facilities
    provided by bfg and only the registrations you need, as in the
    above ViewTests.
    """
    def setUp(self):
        """ This sets up the application registry with the
        registrations your application declares in its configure.zcml
        (including dependent registrations for repoze.bfg itself).
        """
        testing.cleanUp()
        import largebluejingle
        import zope.configuration.xmlconfig
        zope.configuration.xmlconfig.file('configure.zcml',
                                          package=largebluejingle)

    def tearDown(self):
        """ Clear out the application registry """
        testing.cleanUp()

    def test_my_view(self):
        from largebluejingle.views import my_view
        context = testing.DummyModel()
        request = testing.DummyRequest()
        result = my_view(context, request)
        self.assertEqual(result.status, '200 OK')
        body = result.app_iter[0]
        self.failUnless('Welcome to' in body)
        self.assertEqual(len(result.headerlist), 2)
        self.assertEqual(result.headerlist[0],
                         ('Content-Type', 'text/html; charset=UTF-8'))
        self.assertEqual(result.headerlist[1], ('Content-Length',
                                                str(len(body))))

