import unittest

from collective.dancefloor.tests.base import DanceFloorTestCase
from collective.dancefloor.interfaces import *

class TestDanceFloorSchemaextender(DanceFloorTestCase):
    """ Test the schema extension
    """

    def afterSetUp(self):
        pass

    def beforeTearDown(self):
        pass

    def test_it(self):
        self.assertEqual(1+1, 2)


def test_suite():
    suite = unittest.TestSuite(TestDanceFloorSchemaextender)
    suite.addTest(unittest.makeSuite())
    return suite

# vim: set ft=python ts=4 sw=4 expandtab :
