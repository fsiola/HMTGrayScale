import unittest
import numpy.testing
from HMT import *
from scipy import misc

PATH_BINARY_SQUARE = "C:\\Users\\Felipe\\Documents\\GitHub\\HMTGrayScale\\HMTGrayScalePy\\HMTGrayScalePy\\TestImages\\binarySquare.png"
PATH_CRAYON_SQUARE = "C:\\Users\\Felipe\\Documents\\GitHub\\HMTGrayScale\\HMTGrayScalePy\\HMTGrayScalePy\\TestImages\\crayonSquare.png"
PATH_GRAY_SQUARE = "C:\\Users\\Felipe\\Documents\\GitHub\\HMTGrayScale\\HMTGrayScalePy\\HMTGrayScalePy\\TestImages\\graySquare.png"
PATH_NATURED_SQUARE = "C:\\Users\\Felipe\\Documents\\GitHub\\HMTGrayScale\\HMTGrayScalePy\\HMTGrayScalePy\\TestImages\\naturedSquare.png"
PATH_OIL_SQUARE = "C:\\Users\\Felipe\\Documents\\GitHub\\HMTGrayScale\\HMTGrayScalePy\\HMTGrayScalePy\\TestImages\\oilSquare.png"
PATH_WATER_SQUARE = "C:\\Users\\Felipe\\Documents\\GitHub\\HMTGrayScale\\HMTGrayScalePy\\HMTGrayScalePy\\TestImages\\waterSquare.png"

class Test_HMTImageTests(unittest.TestCase):

    def test_ksHMT_image_binarySquare(self):
        img = open(PATH_BINARY_SQUARE)

        bfg = array([[0,0,0],
                     [0,1,1]])

        result = ksHMT(img, bfg)
        show(result)
        numpy.testing.assert_array_equal(result, array([0]))

if __name__ == '__main__':
    unittest.main()

