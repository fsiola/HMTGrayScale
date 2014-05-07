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

    ses = ["se.png"]

    for image in files:
        #for se in ses:
            loadedImage = openImage(path + '\\' + image)
            #loadedSE =
            #array([[0,128,255,128,0],[0,255,255,255,0],[0,128,255,128,0]])
            #loadedSE = iasedisk(5)
            #loadedSE[loadedSE==1]=255
            #loadedSE = openImage(path + '\\' + se)
            #se = 'default'
            #loadedSE = array([[0,128,255,128,0],[255,255,255,255,255],[0,128,255,128,0]])
            #loadedSEBG = array([[100,10,0,10,100],[0,0,0,0,0],[100,10,0,10,100]])
            se = 'SEFGOriginalPlus10SEBGOriginalMinus10'
            loadedSE = loadedImage.copy()
            loadedSE[loadedSE < 245] = loadedSE[loadedSE < 245] + 10
            loadedSEBG = loadedImage.copy()
            loadedSEBG[loadedSEBG > 10] = loadedSEBG[loadedSEBG > 10] - 10

            saveAndShowImage(loadedImage, image + '_' + se + '_originalImage')
        
            #ksHMT
            ksHMTResult = ksHMT(loadedImage, loadedSE)
            saveAndShowImage(ksHMTforShow(ksHMTResult),image + '_' + se + '_ksHMTImage')
            print diffBetweenImages(loadedImage, ksHMTResult)

            #suHMT
            suHMTResult = suHMT(loadedImage, loadedSE, loadedSEBG)
            saveAndShowImage(suHMTResult, image + '_' + se + '_suHMTImage')
            print diffBetweenImages(loadedImage, suHMTResult)

            #bHMT
            bHMTResult = bHMT(loadedImage, loadedSE, loadedSEBG)
            saveAndShowImage(bHMTResult, image + '_' + se + '_bHMTImage')
            print diffBetweenImages(loadedImage, bHMTResult)
        
            #rHMT
            rHMTResult = rHMT(loadedImage, loadedSE, loadedSEBG)
            saveAndShowImage(rHMTResult, image + '_' + se + '_rHMTImage')
            print diffBetweenImages(loadedImage, bHMTResult)

            #rgHMT
            rgHMTResult = rgHMT(loadedImage, loadedSE, loadedSEBG)
            saveAndShowImage(rgHMTResult, image + '_' + se + '_rgHMTImage')
            print diffBetweenImages(loadedImage, rgHMTResult)
        
if __name__ == "__main__":
    main()
