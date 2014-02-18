import unittest
import numpy.testing
from HMTGrayScalePy import *
from numpy import *

class Test_HMTGrayScalePyTests(unittest.TestCase):

    #x = [[0 1 0]
    #      [1 1 1]
    #      [0 1 0]]
    #r = [[1 0 1]
    #      [0 0 0]
    #      [1 0 1]]
    def test_complement_binary(self):
        x = array([[0,1,0],[1,1,1],[0,1,0]])
        r = complement(x)
        numpy.testing.assert_array_equal(r, array([[1,0,1],[0,0,0],[1,0,1]]))

    #x = [[0 1 0]
    #      [1 2 1]
    #      [0 1 0]]
    #r = [[255 254 255]
    #      [254 253 254]
    #      [255 254 255]]
    def test_complement_uint8(self):
        x = array([[0,1,0],[1,2,1],[0,1,0]])
        r = complement(x)
        numpy.testing.assert_array_equal(r, array([[255,254,255],[254,253,254],[255,254,255]]))

    #x= [[0 0 1 1 0]
    #    [1 1 1 1 1]
    #    [0 1 0 1 0]
    #    [0 1 1 1 1]
    #    [0 1 0 1 0]]
    #bfg= [[0 1 0]
    #      [1 1 1]
    #      [0 1 0]]
    #bfg= [[1 0 1]
    #      [0 0 0]
    #      [1 0 1]]
    #r= [[ 0.  0.  0.  0.  0.]
    #    [ 0.  0.  0.  0.  0.]
    #    [ 0.  0.  0.  0.  0.]
    #    [ 0.  0.  0.  1.  0.]
    #    [ 0.  0.  0.  0.  0.]]
    def test_binhtm_Case1(self):
        x = array([[0,0,1,1,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,1,1,1],[0,1,0,1,0]])
        bfg = array([[0,1,0],[1,1,1],[0,1,0]])
        bbg = array([[1,0,1],[0,0,0],[1,0,1]])
        r = binhmt(x,bfg,bbg)
        numpy.testing.assert_array_equal(r, array([[0.,0.,0.,0.,0.],[0.,0.,0.,0.,0.],[0.,0.,0.,0.,0.],[0.,0.,0.,1.,0.],[0.,0.,0.,0.,0.]]))

    #x= [[0 0 1 1 0]
    #    [1 1 1 1 1]
    #    [0 1 0 1 0]
    #    [0 1 1 1 1]
    #    [0 1 0 1 0]]
    #bfg= [[0 1 0]
    #      [1 1 1]
    #      [0 1 0]]
    #bfg= [[1]]
    #expected error: SEs with different shapes
    def test_binhtm_Case2_SEsWithDifferentShapes_raisesException(self):
        x = array([[0,0,1,1,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,1,1,1],[0,1,0,1,0]])
        bfg = array([[0,1,0],[1,1,1],[0,1,0]])
        bbg = array([[1]])
        self.assertRaisesRegexp(Exception, "SEs with different shapes", binhmt, x, bfg, bbg)

        
    #x= [[0 0 1 1 0]
    #    [1 1 1 1 1]
    #    [0 1 0 1 0]
    #    [0 1 1 1 1]
    #    [0 1 0 1 0]]
    #bfg= [[0 1 0]
    #      [1 1 1]
    #      [0 1 0]]
    #bfg= [[1 0 1]
    #      [0 1 0]
    #      [1 0 1]]
    #expected error: SEs with intersection not empty
    def test_binhtm_Case3_SEsWithIntersectionNotEmpty_raisesException(self):
        x = array([[0,0,1,1,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,1,1,1],[0,1,0,1,0]])
        bfg = array([[0,1,0],[1,1,1],[0,1,0]])
        bbg = array([[1,0,1],[0,1,0],[1,0,1]])
        self.assertRaisesRegexp(Exception, "SEs with intersection not empty", binhmt, x, bfg, bbg)


    #x= [[0.0 0.0 1.0 2.0 0.0]
    #    [1.0 1.0 2.0 2.0 2.0]
    #    [0.0 1.0 0.0 2.0 0.0]
    #    [0.0 1.0 1.0 1.0 1.0]
    #    [0.0 1.0 0.0 1.0 0.0]]
    #b= [[0 1 0]
    #    [1 1 1]
    #    [0 1 0]]
    #r= [[ 0.  0.  0.  0.  0.]
    #    [ 0.  0.  0.  2.  0.]
    #    [ 0.  0.  0.  0.  0.]
    #    [ 0.  0.  0.  1.  0.]
    #    [ 0.  0.  0.  0.  0.]]
    def test_erode_GrayLevel_Case1(self):
        x = array([[0,0,1,2,0],[1,1,2,2,2],[0,1,0,2,0],[0,1,1,1,1],[0,1,0,1,0]])
        b = array([[0,1,0],[1,1,1],[0,1,0]])
        r = erode(x,b)
        numpy.testing.assert_array_equal(r, array([[0.,0.,0.,0.,0.],[0.,0.,0.,2.,0.],[0.,0.,0.,0.,0.],[0.,0.,0.,1.,0.],[0.,0.,0.,0.,0.]]))
    
    #x= [[0.0 1.0 1.0 1.0 0.0]]
    #b= [[1 1 1]]
    #r= [[ 0.  0.  1.  0.  0.]]
    def test_erode_SimpleArray(self):
        x = array([[0,1,1,1,0]])
        b = array([[1,1,1]])
        r = erode(x,b)
        numpy.testing.assert_array_equal(r, array([[0.,0.,1.,0.,0.]]))
        

    #x= [0.0 1.0 1.0 1.0 0.0]
    #b= [1 1 1]
    #r= [[ 0.  0.  1.  0.  0.]]
    def test_erode_1DArraysConverted(self):
        x = array([0,1,1,1,0])
        b = array([1,1,1])
        r = erode(x,b)
        numpy.testing.assert_array_equal(r, array([[0.,0.,1.,0.,0.]]))
            

    #x= [[0 0 1 1 0]
    #    [1 1 1 1 1]
    #    [0 1 0 1 0]
    #    [0 1 1 1 1]
    #    [0 1 0 1 0]]
    #b= [[0 1 0]
    #    [1 1 1]
    #    [0 1 0]]
    #r= [[ 0.  0.  0.  0.  0.]
    #    [ 0.  0.  0.  1.  0.]
    #    [ 0.  0.  0.  0.  0.]
    #    [ 0.  0.  0.  1.  0.]
    #    [ 0.  0.  0.  0.  0.]]
    def test_erode_Binary_Case1(self):
        x = array([[0,0,1,1,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,1,1,1],[0,1,0,1,0]])
        b = array([[0,1,0],[1,1,1],[0,1,0]])
        r = erode(x,b)
        numpy.testing.assert_array_equal(r, array([[0.,0.,0.,0.,0.],[0.,0.,0.,1.,0.],[0.,0.,0.,0.,0.],[0.,0.,0.,1.,0.],[0.,0.,0.,0.,0.]]))
        

    #x= [[0 0 1 1 0]
    #    [1 1 1 1 1]
    #    [0 1 0 1 0]
    #    [0 1 1 1 1]
    #    [0 1 0 1 0]]
    #b= [[1]]
    #r= [[ 0.  0.  1.  1.  0.]
    #    [ 1.  1.  1.  1.  1.]
    #    [ 0.  1.  0.  1.  0.]
    #    [ 0.  1.  1.  1.  0.]
    #    [ 0.  1.  0.  1.  0.]]
    def test_erode_Binary_Case2(self):
        x = array([[0,0,1,1,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,1,1,1],[0,1,0,1,0]])
        b = array([[1]])
        r = erode(x,b)
        numpy.testing.assert_array_equal(r, array([[0,0,1,1,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,1,1,1],[0,1,0,1,0]]))


    #x= [0 2 3 1 2]
    #b= [1 1 1 1 1]
    #k= 1
    #r= 1
    def test_rankOrder_Case1(self):
        x = array([0, 2, 3, 1, 2])
        b = array([1, 1, 1, 1, 1])
        k = 1
        r = rankOrder(x,b,k)
        numpy.testing.assert_equal(r, 1)

    #x= [0 2 3 1 2]
    #b= [1 0 1 1 0]
    #k= 2
    #r= 3
    def test_rankOrder_Case2(self):
        x = array([0, 2, 3, 1, 2])
        b = array([1, 0, 1, 1, 0])
        k = 2
        r = rankOrder(x,b,k)
        numpy.testing.assert_equal(r, 3)


    #f= [0 1 1 1 0 1 0 1 1 1 0]
    #b= [0 1 0]
    #e= [-1 -3 -3 -2 -3 0 -3 -2 -3 -3 -1]
    def test_ksHMT_Case1(self):
        x = array([0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0])
        b = array([0, 1, 0])
        e = array([-3, -3, -2, -3, 0, -3, -2, -3, -3])
        r = ksHMT(x,b)        
        numpy.testing.assert_equal(r, e)



if __name__ == '__main__':
    unittest.main()
