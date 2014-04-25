import unittest

from basic_tests import TestSetup, TestBookQuery, TestAuthorQuery

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestBookQuery))
    suite.addTest(unittest.makeSuite(TestAuthorQuery))
    return suite