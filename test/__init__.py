import unittest

from basic_tests import TestSetup, TestDBQuery

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    suite.addTest(unittest.makeSuite(TestDBQuery))
    return suite