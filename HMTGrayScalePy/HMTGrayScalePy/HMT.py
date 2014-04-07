import sys
from numpy import *
from scipy.ndimage import *
from ia636 import *
from ia870 import *
from PIL import Image

import matplotlib.pyplot as plt

def open(path):
    img = Image.open(path).convert('L')
    img = asarray(img)
    img.dtype = 'uint8'
    return img

def save(img,title='image'):
    Image.fromarray(img).save('ResultImage\\' + title + '.png')

def show(img,title='image'):
    Image.fromarray(img).show(title)
    
def erode():
    global loadedImage, seFG
    return iaero(loadedImage, seFG)

def dilate():
    global loadedImage, seFG
    return iadil(loadedImage, seFG)

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
    dilFBbg = iadil(f, bbg)

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
    dilFBbg = iadil(f, bbg)

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
    dilFBbg = iadil(f, bbg)

    maxValue = max(max(eroFBfg.ravel()), max(dilFBbg.ravel())) + 1

    resultImage = zeros(f.shape)

    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            if(eroFBfg[x][y] >= dilFBbg[x][y] != maxValue):
                resultImage[x][y] = eroFBfg[x][y]
            else:
                resultImage[x][y] = maxValue

    return resultImage    

#Raducana and Grana Hit-Or-Miss Transformation
def rgHMT(f, bfg, bbg):
    #[RGHMT_b(f)](x) = sup_{t \in t_max} (x \in HMT_b_t(CSt(f))

    if len(f.shape) == 1:
        f = expand_dims(f,0)

    maxF = max(f.ravel())

    resultImage = zeros(f.shape)

    for t in range(maxF):
        tempF = zeros(f.shape)
        tempBfg = zeros(bfg.shape)
        tempBbg = zeros(bbg.shape)

        tempF[where(f == t)] = True
        tempBfg[where(bfg == t)] = True
        tempBbg[where(bbg == t)] = True

        tempBinHMT = binary_hit_or_miss(tempF, tempBfg, tempBbg)

        #not sure here
        resultImage += tempBinHMT
    return resultImage

##########################################################################

#variables
openWindowAfterOperation = True
saveImageAfterOperation = True
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
    print "\s-toogle save result images (actual: " , saveImageAfterOperation , ")"
    print "\te-erode image"
    print "\td-dilate image"
    print "\tds-define se"
    print "\tls-load se"
    print "\tli-load image"
    print "\tks-ksHMT - Khosravi and Schafer Hit-Or-Miss Transformation"
    print "\tsu-suHMT - Soille Unconstrained Hit-Or-Miss Transformation"
    print "\tba-bHMT - Barat Hit-or-Miss Transformation"
    print "\tro-rHMT - Ronse Hit-Or-Miss Transformation"
    print "\trg-rgHMT - Raducana and Grana Hit-Or-Miss Transformation"
    print "\ta-run all HMT implementations"
    print "\tdemo-run demo for all sample imafes in all HMT implementations"
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
    global loadedImage
    try:
        fileNameImage = raw_input('image file location: ')            
        if(fileNameImage == ''): fileNameImage = 'C:\Users\Felipe\Documents\GitHub\HMTGrayScale\HMTGrayScalePy\HMTGrayScalePy\TestImages\\binarySquare.png'
        loadedImage = open(fileNameImage)
        if(openWindowAfterOperation):
            show(loadedImage)
    except:
        print 'error: ', sys.exc_info()[0]

def executeHMT(op):
    global loadedImage, seFG, seBG, ksHMTResult, suHMTResult, bHMTResult, rHMTResult, rgHMTResult
    try:
        if(op == 'ks' or op == 'a'):
            print 'executing ksHMT'
            ksHMTResult = ksHMT(loadedImage, seFG)

        if(op == 'su' or op == 'a'):
            print 'executing suHMT'
            suHMTResult = suHMT(loadedImage, seFG, seBG)

        if(op == 'ba' or op == 'a'):
            print 'executing baHMT'
            bHMTResult = bHMT(loadedImage, seFG, seBG)

        if(op == 'ro' or op == 'a'):
            print 'executing roHMT'
            rHMTResult = rHMT(loadedImage, seFG, seBG)

        if(op == 'rg' or op == 'a'):
            print 'executing rgHMT'
            rgHMTResult = rgHMT(loadedImage, seFG, seBG)
    except:
        print 'error: ', sys.exc_info()[0]

def openHMTResult(op):
    global ksHMTResult, suHMTResult, bHMTResult, rHMTResult, rgHMTResult
    try:
        if(op == 'ks' or op == 'a'):
            show(ksHMTResult, 'ksHTM')

        if(op == 'su' or op == 'a'):
            show(suHMTResult, 'suHTM')

        if(op == 'ba' or op == 'a'):
            show(bHMTResult, 'baHTM')

        if(op == 'ro' or op == 'a'):
            show(rHMTResult, 'roHTM')

        if(op == 'rg' or op == 'a'):
            show(rgHMTResult, 'rgHTM')
    except:
        print 'error: ', sys.exc_info()[0]

def saveHMTResult(op):
    global ksHMTResult, suHMTResult, bHMTResult, rHMTResult, rgHMTResult
    try:
        if(op == 'ks' or op == 'a'):
            save(ksHMTResult, 'ksHTM')

        if(op == 'su' or op == 'a'):
            save(suHMTResult, 'suHTM')

        if(op == 'ba' or op == 'a'):
            save(bHMTResult, 'baHTM')

        if(op == 'ro' or op == 'a'):
            save(rHMTResult, 'roHTM')

        if(op == 'rg' or op == 'a'):
            save(rgHMTResult, 'rgHTM')
    except:
        print 'error: ', sys.exc_info()[0]

def createSEs():
    global seFG, seBG
    try:
        funcFG = raw_input('type function to create se fg: ')
        if(funcFG == ''): funcFG = 'iasebox(10)'
        seFG = eval(funcFG)
        funcBG = raw_input('type function to create se bg: ')
        if(funcBG == ''): funcBG = 'iasecross(10)'
        seBG = eval(funcBG)
    except:
        print 'error: ', sys.exc_info()[0]
        
def demo():
    global loadedImage, seFG, seBG

    try:
        createSEs()

        files = array(['TestImages\\binarySquare.png',
                       'TestImages\\crayonSquare.png',
                       'TestImages\\graySquare.png',
                       'TestImages\\naturedSquare.png',
                       'TestImages\\oilSquare.png',
                       'TestImages\\waterSquare.png'])

        for file in files:
            print 'executing ', file
            loadedImage = open(file)
            show(loadedImage, file)
            executeHMT('a')           
            openHMTResult('a')
    except:
        print 'error: ', sys.exc_info()[0]

def main():

    option = 'h'

    #main loop
    while(option != 'x'):
        if(option == 'h'):
            help()

        elif(option == 'demo'):
            demo()

        elif(option == 't'):
            global openWindowAfterOperation
            openWindowAfterOperation = not openWindowAfterOperation
            help()

        elif(option == 's'):
            global saveImageAfterOperation
            saveImageAfterOperation = not saveImageAfterOperation
            help()

        elif(option == 'e'):
            img = erode()
            show(img, 'erode')

        elif(option == 'd'):
            img = dilate()
            show(img, 'dilate')

        elif(option == 'ds'): #use like creating SEs in AdessoWiki - for FG and BG
            createSEs()
            
        elif(option == 'ls'): #for FG and BG
            openSEs()
                                   
        elif(option == 'li'): 
            openImage()
                
        elif(option == 'ks' or option == 'su' or option == 'ba' or option == 'ro' or option == 'rg' or option == 'a'): 
            executeHMT(option)           
            if(saveImageAfterOperation): 
                saveHMTResult(option)
            if(openWindowAfterOperation): 
                openHMTResult(option)

        else:
            print 'not a valid command'            
            help()

        option = raw_input('option: ')


if __name__ == "__main__":
    main()
