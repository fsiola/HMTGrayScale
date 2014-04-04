import sys
from numpy import *
from scipy.ndimage import *
from ia636 import *
from ia870 import *

from scipy import misc
import matplotlib.pyplot as plt

def open(path):
    img = misc.imread(path,1)
    img.dtype = 'uint8'
    return img

def show(img):
    plt.imshow(img)
    plt.show()

#Khosravi and Schafer Hit-Or-Miss Transformation
def ksHMT(f, bfg):
    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(bfg.shape) == 1:
        bfg = expand_dims(bfg,0)
        
    eroFBfg = iaero(f, bfg)
    eroMFMBfg = iaero(ianeg(f), ianeg(bfg))

    resultImage = zeros(f.shape)

    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            resultImage[x][y] = eroFBfg[x][y] - eroMFMBfg[x][y]

    return resultImage

#Soille Unconstrained Hit-Or-Miss Transformation
def suHMT(f,bfg, bbg):
    #[SUHMT_b(f)](x) = card {t : (Bfg)x esta contido em CSt(f) e (Bbg)x esta
    #contido em (CSt(f))^c}
    #[SUHMT_b(f)](x) = [erosao_{Bfg}(f)](x) - [dil_{Bbg}(f)](x) se dil <= ero
    #                  0 cc.

    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(bfg.shape) == 1:
        bfg = expand_dims(bfg,0)

    if len(bbg.shape) == 1:
        bbg = expand_dims(bbg,0)

    bbg = ianeg(bbg)

    eroFBfg = iaero(f, bfg)
    dilBbg = iadil(f, bbg)

    resultImage = zeros(f.shape)

    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            resultImage[x][y] = max(eroFBfg[x][y] - dilFBbg[x][y], 0)

    return resultImage

#Barat Hit-or-Miss Transformation
def bHMT(f, bfg, bbg):
    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(bfg.shape) == 1:
        bfg = expand_dims(bfg,0)

    if len(bbg.shape) == 1:
        bbg = expand_dims(bbg,0)

    bbg = ianeg(bbg)

    eroFBfg = iaero(f, bfg)
    dilBbg = iadil(f, bbg)

    resultImage = zeros(f.shape)

    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            resultImage[x][y] = dilFBbg[x][y] - eroFBfg[x][y]

    return resultImage    

#Ronse Hit-Or-Miss Transformation
def rHMT(f, bfg, bbg):
    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(bfg.shape) == 1:
        bfg = expand_dims(bfg,0)

    if len(bbg.shape) == 1:
        bbg = expand_dims(bbg,0)

    bbg = ianeg(bbg)

    eroFBfg = iaero(f, bfg)
    dilBbg = iadil(f, bbg)

    maxValue = max(eroFBfg, max(dilBbg)) + 1

    resultImage = zeros(f.shape)

    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            if(ero[x][y] >= dilBbg[x][y] != maxvalue):
                resultImage[x][y] = eroFBfg[x][y]
            else:
                resultImage[x][y] = maxValue

    return resultImage    

#Raducana and Grana Hit-Or-Miss Transformation
def rgHMT(f, bfg, bbg):
    #[RGHMT_b(f)](x) = sup_{t \in t_max} (x \in HMT_b_t(CSt(f))

    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(b.shape) == 1:
        b = expand_dims(b,0)

    maxF = max(f.ravel())

    resultImage = zeros(f.shape)

    for t in range(maxF):
        tempF = zeros(f.shape)
        tempBfg = zeros(bfg.shape)
        tempBbg = zeros(bbg.shape)

        for x in range(f.shape[0]):
            for y in range(f.shape[1]):
                if(f[x][y] == t):
                    tempImage[x][y] = 1

        for x in range(bfg.shape[0]):
            for y in range(bfg.shape[1]):
                if(bfg[x][y] == t):
                    tempBfg[x][y] = 1

        for x in range(bbg.shape[0]):
            for y in range(bbg.shape[1]):
                if(bbg[x][y] == t):
                    tempBbg[x][y] = 1

        tempBinHMT = binary_hit_or_miss(tempF, tempBfg, tempBbg)

        #not sure here
        resultImage += tempBinHMT
    return resultImage

##########################################################################

#variables
openWindowAfterOperation = True
fileNameImage = ''
fileNameFG = ''
fileNameBG = ''
seFG = None
seBG = None
loadedImage = None
ksHMTResult = None
suHMTResult = None
bHMTResult = None
rHMTResult = None
rgHMTResult = None



#console helpers
def help():
    print "HMT grey-erosion - type desired action"
    print "\to-toogle open/close result images (actual: " , openWindowAfterOperation , ")"
    print "\tds-define se"
    print "\tls-load se"
    print "\tli-load image"
    print "\tks-ksHMT - Khosravi and Schafer Hit-Or-Miss Transformation"
    print "\tsu-suHMT - Soille Unconstrained Hit-Or-Miss Transformation"
    print "\tba-bHMT - Barat Hit-or-Miss Transformation"
    print "\tro-rHMT - Ronse Hit-Or-Miss Transformation"
    print "\trg-rgHMT - Raducana and Grana Hit-Or-Miss Transformation"
    print "\ta-run all HMT implementations"
    print "\th-repeat this message"
    print "\tx-exit"

def openSEs():
    try:
        fileNameFG = raw_input('se fg file location: ')            
        seFG = open(fileNameFG)
        fileNameBG = raw_input('se bg file location: (empty for skip) ')            
        if(fileNameBG != ''):
            seBG = open(fileNameBG)
    except:
        print 'error: ', sys.exc_info()[0]

def openImage():
    try:
        fileNameImage = raw_input('image file location: ')            
        loadedImage = open(fileNameImage)
        if(openWindowAfterOperation):
            show(loadedImage)
    except:
        print 'error: ', sys.exc_info()[0]

def executeHMT(op):
    try:
        if(op == 'ks' or op == 'a'):
            ksHMTResult= ksHMT(loadedImage, seFG)

        if(op == 'su' or op == 'a'):
            suHMTResult= suHMT(loadedImage, seFG, seBG)

        if(op == 'ba' or op == 'a'):
            bHMTResult= bHMT(loadedImage, seFG, seBG)

        if(op == 'ro' or op == 'a'):
            rHMTResult= rHMT(loadedImage, seFG, seBG)

        if(op == 'rg' or op == 'a'):
            rgHMTResult= rgHMT(loadedImage, seFG, seBG)
    except:
        print 'error: ', sys.exc_info()[0]

def openHMTResult(op):
    try:
        if(op == 'ks' or op == 'a'):
            show(ksHMTResult)

        if(op == 'su' or op == 'a'):
            show(suHMTResult)

        if(op == 'ba' or op == 'a'):
            show(bHMTResult)

        if(op == 'ro' or op == 'a'):
            show(rHMTResult)

        if(op == 'rg' or op == 'a'):
            show(rgHMTResult)
    except:
        print 'error: ', sys.exc_info()[0]


def main():
    option = 'h'

    #main loop
    while(option != 'x'):
        if(option == 'h'):
            help()

        elif(option == 't'):
            global openWindowAfterOperation
            openWindowAfterOperation = not openWindowAfterOperation
            help()

        elif(option == 'ds'): #use like creating SEs in Adesso - for FG and BG
            print 'not implemented yet' 
            
        elif(option == 'ls'): #for FG and BG
            openSEs()
                                   
        elif(option == 'li'): 
            openImage()
            
        elif(option == 'ks' or option == 'su' or option == 'ba' or option == 'ro' or option == 'rg' or option == 'a'): 
            executeHMT(option)           
            if(openWindowAfterOperation): 
                openHMTResult(option)

        else:
            print 'not a valid command'            
            help()

        option = raw_input('option: ');


if __name__ == "__main__":
    main()