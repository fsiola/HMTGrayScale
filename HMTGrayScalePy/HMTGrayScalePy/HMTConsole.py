from HMT import *
from Utils import *

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
    print "\tt-toogle open/close result images (actual: " , openWindowAfterOperation , ")"
    print "\ts-toogle save result images (actual: " , saveImageAfterOperation , ")"
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
        if(fileNameFG != ''): seFG = openImage(fileNameFG)
        fileNameBG = raw_input('se bg file location: (empty for skip) ')            
        if(fileNameBG != ''): seBG = openImage(fileNameBG)
    except:
        print 'error: ', sys.exc_info()[0]

def loadImage():
    global loadedImage
    try:
        fileNameImage = raw_input('image file location: ')            
        if(fileNameImage == ''): fileNameImage = 'C:\Users\Felipe\Documents\GitHub\HMTGrayScale\HMTGrayScalePy\HMTGrayScalePy\TestImages\\binarySquare.png'
        loadedImage = openImage(fileNameImage)        
    except:
        print 'error: ', sys.exc_info()[0]

def createSEs():
    global seFG, seBG
    try:
        funcFG = raw_input('type function to create se fg: ')
        if(funcFG == '' and seFG == None): funcFG = 'iasebox(10)'
        if(funcFG != ''): seFG = eval(funcFG)
        funcBG = raw_input('type function to create se bg: ')
        if(funcBG == '' and seBG == None): funcBG = 'iasecross(10)'
        if(funcBG != ''): seBG = eval(funcBG)
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
            showImage(ksHMTResult, 'ksHTM')

        if(op == 'su' or op == 'a'):
            showImage(suHMTResult, 'suHTM')

        if(op == 'ba' or op == 'a'):
            showImage(bHMTResult, 'baHTM')

        if(op == 'ro' or op == 'a'):
            showImage(rHMTResult, 'roHTM')

        if(op == 'rg' or op == 'a'):
            showImage(rgHMTResult, 'rgHTM')
    except:
        print 'error: ', sys.exc_info()[0]

def saveHMTResult(op):
    global ksHMTResult, suHMTResult, bHMTResult, rHMTResult, rgHMTResult
    try:
        if(op == 'ks' or op == 'a'):
            saveImage(ksHMTResult, 'ksHTM')

        if(op == 'su' or op == 'a'):
            saveImage(suHMTResult, 'suHTM')

        if(op == 'ba' or op == 'a'):
            saveImage(bHMTResult, 'baHTM')

        if(op == 'ro' or op == 'a'):
            saveImage(rHMTResult, 'roHTM')

        if(op == 'rg' or op == 'a'):
            saveImage(rgHMTResult, 'rgHTM')
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
            img = erode(loadedImage, seFG)
            if(saveImageAfterOperation): 
                saveImage(img, 'erode')
            if(openWindowAfterOperation): 
                showImage(img, 'erode')

        elif(option == 'd'):
            img = dilate(loadedImage, seFG)
            if(saveImageAfterOperation): 
                saveImage(img, 'dilate')
            if(openWindowAfterOperation): 
                showImage(img, 'dilate')

        elif(option == 'ds'): #use like creating SEs in AdessoWiki - for FG and BG
            createSEs()
            if(saveImageAfterOperation): 
                saveImage(seFG, 'seFG')
                saveImage(seBG, 'seBG')
            if(openWindowAfterOperation): 
                showImage(seFG, 'seFG')
                showImage(seBG, 'seBG')
            
        elif(option == 'ls'): #for FG and BG
            openSEs()
            if(saveImageAfterOperation): 
                saveImage(seFG, 'seFG')
                saveImage(seBG, 'seBG')
            if(openWindowAfterOperation): 
                showImage(seFG, 'seFG')
                showImage(seBG, 'seBG')
                                   
        elif(option == 'li'): 
            loadImage()
            if(saveImageAfterOperation): 
                saveImage(loadedImage, 'image')
            if(openWindowAfterOperation):
                showImage(loadedImage)
                
        elif(option == 'ks' or option == 'su' or option == 'ba' or option == 'ro' or option == 'rg' or option == 'a'): 
            executeHMT(option)           
            if(saveImageAfterOperation): 
                saveHMTResult(option)
            if(openWindowAfterOperation): 
                openHMTResult(option)

        else:
            print option, 'is not a valid command'            
            help()

        option = raw_input('option: ')

if __name__ == "__main__":
    main()
