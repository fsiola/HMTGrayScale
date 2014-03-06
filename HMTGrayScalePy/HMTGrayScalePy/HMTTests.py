import unittest
import numpy.testing
from HMT import *
from numpy import *

class Test_HMTTests(unittest.TestCase):

    def test_ksHMT_Erosion_Case1(self):
        b = array([0,1,2,1,0])
        f = array([0,0,2,2,2,0,0,1,2,1,0,0,2,2,2,0,0])
        r = ksHMT(f,b)
        numpy.testing.assert_array_equal(r, array([0]))

    def test_suHMT_Case1(self):
        f = array([3,3,3,0,1,6,2,1,7,5,1,0,4,6,7,3,3,3])
        bfg = array([0,0,1,1,0,0])
        bbg = array([0,0,1,1,0,0])
        r = suHMT(f, bfg, bbg)
        numpy.testing.assert_array_equal(r, array([0]))

if __name__ == '__main__':
    unittest.main()
