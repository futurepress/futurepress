import unittest

from basic_tests import (
    TestSetup,
    TestBookQuery,
    TestAuthorQuery,
    TestUserLogin,
    TestHomePage,
    TestBasicFeed
    )

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestBookQuery))
    suite.addTest(unittest.makeSuite(TestAuthorQuery))
    suite.addTest(unittest.makeSuite(TestUserLogin))
    suite.addTest(unittest.makeSuite(TestHomePage))
    suite.addTest(unittest.makeSuite(TestBasicFeed))

    return suite