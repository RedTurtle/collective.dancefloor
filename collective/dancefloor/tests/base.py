from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import collective.dancefloor
    zcml.load_config('configure.zcml', collective.dancefloor)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.dancefloor')

setup_product()
ptc.setupPloneSite(products=['collective.dancefloor'])


class DanceFloorTestCase(ptc.PloneTestCase):
    """DanceFloorTestCase
    """


class DanceFloorFunctionalTestCase(ptc.FunctionalTestCase):
    """DanceFloorFunctionalTestCase
    """

# vim: set ft=python ts=4 sw=4 expandtab :
