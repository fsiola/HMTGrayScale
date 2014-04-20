from HMT import *
from Utils import *
from ia870 import *

def main():
    path = "ArtificialImages"
    files = ["diagonal.png",
             "linear.png",
             "radial.png",
             "radialDifferentSizes.png",
             "radialSameSize.png"]

    for image in files:
        loadedImage = openImage(path + '\\' + image)
        loadedSE = array([[0,128,255,128,0],[0,255,255,255,0],[0,128,255,128,0]])
        showImage(loadedImage)
        showImage(ksHMT(loadedImage, loadedSE))
        showImage(suHMT(loadedImage, loadedSE, ianeg(loadedSE)))
        showImage(bHMT(loadedImage, loadedSE, ianeg(loadedSE)))
        showImage(rHMT(loadedImage, loadedSE, ianeg(loadedSE)))
        showImage(rgHMT(loadedImage, loadedSE, ianeg(loadedSE)))
        
if __name__ == "__main__":
    main()
