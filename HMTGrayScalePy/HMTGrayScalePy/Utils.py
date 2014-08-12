from PIL import Image
from numpy import *
import webbrowser
import os
from HMT import *
import cv2
from skimage import *

def openImage(path):
    img = Image.open(path).convert('L')
    img = asarray(img)
    img.dtype = 'uint8' #force grayscale
    return img

def saveImage(img,title='image',path='ResultImage'):    
    img = uint8(img)
    Image.fromarray(img).save(path + '\\' + os.path.splitext(title)[0] + '.png')
    return path + '\\' + title + '.png'

def showImage(img,title='image'):
    Image.fromarray(img).show(title)

def noise(img):
    return img + util.random_noise(img, 's&p')

def saveAndShowImage(img, title='image'):
    webbrowser.open(saveImage(img, title))

def diffBetweenImages(original, calculated):
    return all(original == calculated)

def createHMTL(fileName, resultPath):
    createdPage = open(resultPath + "\\" + fileName + ".html", "w")
    createdPage.write("<html><head><title>")
    createdPage.write(fileName)
    createdPage.write("</title></head><body><h1>")
    createdPage.write(fileName)
    createdPage.write("</h1>")
    return createdPage

def addImageToHMTL(img, name, path, createdPage):
    savedPath = saveImage(img,name,path)
    createdPage.write("<h2>Name: " + name + "</h2><img src='" + name + ".png' alt='" + name + "' /><br />")

def finishHTML(createdPage):
    createdPage.write("</body></html>")
    createdPage.close()

def runExperiment(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderSE = initialFolder + "\\SEs"
    folderSEFG = folderSE + "\\FG"
    folderSEBG = folderSE + "\\BG"
    folderSEGeneral = folderSE + "\\General"
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            #TODO
            #running for general SEs using negation to generate seBG from seFG
            #if(runGeneralSEs):

            #running for seFG versus all seBG in folder
            #TODO LOOP TRHOUGH SEBG FOLDER
            for seFG in next(os.walk(folderSEFG))[2]:

                print "\tEvaluation with seFG : " + seFG 
                loadedSEFG = openImage(folderSEFG + "\\" + seFG)
                seFGFileName = os.path.splitext(seFG)[0]
                currentHMTL.write("<hr>")                

                for seBG in next(os.walk(folderSEBG))[2]: #TODO: filter for start of seFG name
                    print "\t\tEvaluation with seBG : " + seBG 
                    loadedSEBG = openImage(folderSEBG + "\\" + seBG) 
                    seBGFileName = os.path.splitext(seBG)[0]
                    currentHMTL.write("<hr>")                
                    
                    for image in os.listdir(folder):
                        print "\t\t\tEvaluation image : " + image
                        imageFileName = os.path.splitext(image)[0]

                        loadedImage = openImage(folder + "\\" + image)                    
                        addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                        addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                        addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                        addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                        addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                        ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                        addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                        addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)


                        addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                        #RG looks broke
                        #addImageToHMTL(rgHMT(loadedImage, loadedFGSE,
                        #loadedBGSE), "RGHMT_"+image+"_SE_"+seFG , resultPath,
                        #currentHMTL)

                        #POHMT is taking forever to calculate
                        #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                        #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                        #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment2(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)



def runExperiment3QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[255,255,0,0,0],[255,255,0,0,0],[0,0,0,0,0],[0,0,0,255,255],[0,0,0,255,255]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,40,40],[0,0,0,40,40],[0,0,0,0,0],[40,40,0,0,0],[40,40,0,0,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment4QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[128,128,0,0,0],[128,128,0,0,0],[0,0,0,0,0],[0,0,0,128,128],[0,0,0,128,128]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,40,40],[0,0,0,40,40],[0,0,0,0,0],[40,40,0,0,0],[40,40,0,0,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment5QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[1,1,0,0,0],[1,1,1,1,1],[1,1,1,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment6QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[250,250,0,0,0],[250,250,0,0,0],[250,250,0,0,0],[250,250,250,250,250],[250,250,250,250,250]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,120,120],[0,0,0,120,120],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment7QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = array([[250,250,0,0,0],[250,250,0,0,0],[250,250,0,0,0],[250,250,250,250,250],[250,250,250,250,250]])
    bg = iasereflect(ianeg(array([[0,0,0,120,120],[0,0,0,120,120],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment8QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = array([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(array([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment9QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = array([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
        
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                addImageToHMTL(ksHMTResult, imageFileName + "_KSHMT_SEFG_" + seFGFileName, resultPath, currentHMTL)
                addImageToHMTL(ianeg(iagray(iathreshad(ksHMTResult,100))), imageFileName + "_KSHMT_SEFG_" + seFGFileName+"_THRESH100", resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment10QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment11QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment12QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]]))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment13QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = array([[100,100,0,0,0],[100,100,0,0,0],[0,0,0,0,0],[0,0,0,100,100],[0,0,0,100,100]])
    bg = ianeg(array([[0,0,0,100,100],[0,0,0,100,100],[0,0,0,0,0],[100,100,0,0,0],[100,100,0,0,0]]))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment14QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment15QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#SUHMT
def runExperiment16QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                    
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTResult, imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_DOUBLE_KSHMT_THRESH_50", resultPath, currentHMTL)

                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                addImageToHMTL(ianeg(cv2.adaptiveThreshold(uint8(suHMT(loadedImage, loadedSEFG, loadedSEBG)),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#SUHMT with adaptive thrshold and resize to 0.3
def runExperiment17QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                    
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTResult, imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_DOUBLE_KSHMT_THRESH_50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                addImageToHMTL(ianeg(cv2.adaptiveThreshold(uint8(suHMT(loadedImage, loadedSEFG, loadedSEBG)),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#SUHMT with adaptive thrshold and resize to 0.3 dilate with disk 10x10
def runExperiment18QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                    
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTResult, imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_DOUBLE_KSHMT_THRESH_50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                resultImage = ianeg(cv2.adaptiveThreshold(uint8(suHMT(loadedImage, loadedSEFG, loadedSEBG)),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                addImageToHMTL(resultImage, imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH_RESIZE", resultPath, currentHMTL)

                resultImage2 = iadil(resultImage,iasedisk(10))
                addImageToHMTL(resultImage2, imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH_RESIZE_DILATE10x10", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#SUHMT with adaptive thrshold and resize to 0.3 dilate with disk 10x10 and iaedgeoff
def runExperiment18aQrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                    
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTResult, imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_DOUBLE_KSHMT_THRESH_50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                resultImage = ianeg(cv2.adaptiveThreshold(uint8(suHMT(loadedImage, loadedSEFG, loadedSEBG)),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                addImageToHMTL(resultImage, imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH_RESIZE", resultPath, currentHMTL)

                resultImage2 = iadil(resultImage,iasedisk(10))
                addImageToHMTL(resultImage2, imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH_RESIZE_DILATE10x10", resultPath, currentHMTL)

                resultImage3 = iaedgeoff(resultImage2)
                addImageToHMTL(resultImage3, imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH_RESIZE_DILATE10x10_EDGEOFF", resultPath, currentHMTL)


                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


#RHMT with thresh 50
def runExperiment19QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#RHMT with ataptive thresh and resize to 0.3
def runExperiment20QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                addImageToHMTL(ianeg(cv2.adaptiveThreshold(uint8(rHMT(loadedImage, loadedSEFG, loadedSEBG)),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)
#RHMT with otsu thresh and resize to 0.3 and gaussian blur and adaptive thresh
def runExperiment21QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage  =rHMT(loadedImage, loadedSEFG, loadedSEBG)
                addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                resultImage3 = ianeg(cv2.adaptiveThreshold(resultImage2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                addImageToHMTL(resultImage3, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_ADAPTIVETHRESHNEG", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#RHMT with resize to 0.3 and gaussian blur and otsu thresh
def runExperiment22QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage  =rHMT(loadedImage, loadedSEFG, loadedSEBG)
                addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                resultImage3 = ianeg(cv2.adaptiveThreshold(resultImage2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                addImageToHMTL(resultImage3, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_ADAPTIVETHRESHNEG", resultPath, currentHMTL)

                resultImage4 = ianeg(cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
                addImageToHMTL(resultImage4, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSUNEG", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#BHMT with resize to 0.3
def runExperiment23QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage  =bHMT(loadedImage, loadedSEFG, loadedSEBG)

                addImageToHMTL(resultImage, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                #resultImage  =rHMT(loadedImage, loadedSEFG, loadedSEBG)
                #addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                #addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                #resultImage3 = ianeg(cv2.adaptiveThreshold(resultImage2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                #addImageToHMTL(resultImage3, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_ADAPTIVETHRESHNEG", resultPath, currentHMTL)

                #resultImage4 = ianeg(cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
                #addImageToHMTL(resultImage4, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSUNEG", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#BHMT with resize to 0.3 with gaussian blur and otsu
def runExperiment24QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage = bHMT(loadedImage, loadedSEFG, loadedSEBG)
                addImageToHMTL(resultImage, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                addImageToHMTL(resultImage2, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                resultImage3 = cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
                addImageToHMTL(resultImage3, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSU", resultPath, currentHMTL)

                #loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                #resultImage  =rHMT(loadedImage, loadedSEFG, loadedSEBG)
                #addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                #addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                #resultImage3 = ianeg(cv2.adaptiveThreshold(resultImage2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                #addImageToHMTL(resultImage3, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_ADAPTIVETHRESHNEG", resultPath, currentHMTL)

                #resultImage4 = ianeg(cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
                #addImageToHMTL(resultImage4, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSUNEG", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#BHMT with resize to 0.3 with gaussian blur and otsu
def runExperiment25QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage = (bHMT(loadedImage, loadedSEFG, loadedSEBG) + 255)/2
                addImageToHMTL(resultImage, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                addImageToHMTL(resultImage2, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                resultImage3 = cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
                addImageToHMTL(resultImage3, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSU", resultPath, currentHMTL)

                #loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                #resultImage  =rHMT(loadedImage, loadedSEFG, loadedSEBG)
                #addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                #addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                #resultImage3 = ianeg(cv2.adaptiveThreshold(resultImage2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                #addImageToHMTL(resultImage3, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_ADAPTIVETHRESHNEG", resultPath, currentHMTL)

                #resultImage4 = ianeg(cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
                #addImageToHMTL(resultImage4, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSUNEG", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#BHMT with resize to 0.3 with gaussian blur and otsu using only neg values
def runExperiment26QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage = bHMT(loadedImage, loadedSEFG, loadedSEBG)
                resultImage[resultImage > 0] = 0
                resultImage *= -1
                addImageToHMTL(resultImage, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                addImageToHMTL(resultImage2, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                resultImage3 = cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
                addImageToHMTL(resultImage3, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSU", resultPath, currentHMTL)

                #loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                #resultImage  =rHMT(loadedImage, loadedSEFG, loadedSEBG)
                #addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                #addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                #resultImage3 = ianeg(cv2.adaptiveThreshold(resultImage2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                #addImageToHMTL(resultImage3, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_ADAPTIVETHRESHNEG", resultPath, currentHMTL)

                #resultImage4 = ianeg(cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
                #addImageToHMTL(resultImage4, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSUNEG", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#BHMT with resize to 0.3 with gaussian blur and otsu using neg values an dilate 10 disk
def runExperiment27QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage = bHMT(loadedImage, loadedSEFG, loadedSEBG)
                resultImage[resultImage > 0] = 0
                resultImage *= -1
                addImageToHMTL(resultImage, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                addImageToHMTL(resultImage2, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                resultImage3 = cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
                addImageToHMTL(resultImage3, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSU", resultPath, currentHMTL)

                resultImage4 = iadil(resultImage3, iasedisk(10))
                addImageToHMTL(resultImage4, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSU_DILATE10x10", resultPath, currentHMTL)

                #loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                #resultImage  =rHMT(loadedImage, loadedSEFG, loadedSEBG)
                #addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                #addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                #resultImage3 = ianeg(cv2.adaptiveThreshold(resultImage2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                #addImageToHMTL(resultImage3, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_ADAPTIVETHRESHNEG", resultPath, currentHMTL)

                #resultImage4 = ianeg(cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
                #addImageToHMTL(resultImage4, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSUNEG", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#KSHMT with resize to 0.3 using neg values an dilate 10 disk
def runExperiment28QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = array([[255,255,0,0,0],[255,255,0,0,0],[0,0,0,0,0],[0,0,0,255,255],[0,0,0,255,255]])
    bg = iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage = ksHMT(loadedImage, loadedSEFG)
                resultImage *= -1
                resultImage[resultImage > 255] = 255
                resultImage = ianeg(uint8(resultImage))                
                resultImage[resultImage != 0] = 255
                addImageToHMTL(resultImage, imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_GOODVALUES" , resultPath, currentHMTL)

                resultImage2 = iadil(resultImage, iasedisk(10))
                addImageToHMTL(resultImage2, imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_NEGVALUES_DILATE10DISK" , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                #resultImage = bHMT(loadedImage, loadedSEFG, loadedSEBG)
                #resultImage[resultImage > 0] = 0
                #resultImage *= -1
                #addImageToHMTL(resultImage, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                #addImageToHMTL(resultImage2, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                #resultImage3 = cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
                #addImageToHMTL(resultImage3, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSU", resultPath, currentHMTL)

                #resultImage4 = iadil(resultImage3, iasedisk(10))
                #addImageToHMTL(resultImage4, imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSU_DILATE10x10", resultPath, currentHMTL)

                #loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                #resultImage  =rHMT(loadedImage, loadedSEFG, loadedSEBG)
                #addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #resultImage2 = cv2.GaussianBlur(uint8(resultImage), (5,5),0)
                #addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR", resultPath, currentHMTL)

                #resultImage3 = ianeg(cv2.adaptiveThreshold(resultImage2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                #addImageToHMTL(resultImage3, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_ADAPTIVETHRESHNEG", resultPath, currentHMTL)

                #resultImage4 = ianeg(cv2.threshold(resultImage2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
                #addImageToHMTL(resultImage4, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_WITHGAUSSIANBLUR_OTSUNEG", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#RHMT
def runExperiment29QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = array([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = array([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage = rHMT(loadedImage, loadedSEFG, loadedSEBG)
                resultImage[resultImage < 0] = 0
                resultImage[resultImage != 0] = 255
                resultImage = uint8(resultImage)
                
                addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_POSVALUES", resultPath, currentHMTL)

                resultImage2 = iadil(resultImage, iasedisk(10))
                addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_POSVALUES_DILATEDISK10", resultPath, currentHMTL)

                #RGHMT takes forever
                #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#RGHMT
def runExperiment30QrCode(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False, runGeneralSEs=False):
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    fg = array([[255,255,0,0,0],[255,255,0,0,0],[0,0,0,0,0],[0,0,0,255,255],[0,0,0,255,255]])
    bg = array([[0,0,0,255,255],[0,0,0,255,255],[0,0,0,0,0],[255,255,0,0,0],[255,255,0,0,0]])

    
    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:

        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
        
        for folder in imageFolders:
            print "Evaluating images in folder : " + folder 
        
            loadedSEFG = fg
            seFGFileName = "default"

            loadedSEBG = bg
            seBGFileName = "default"
                                
            for image in os.listdir(folder):
                print "\t\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                #addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
                #addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #ksHMTResult = ksHMT(loadedImage, loadedSEFG)
                #addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(suHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_THRESH50", resultPath, currentHMTL)

                #addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)
                #addImageToHMTL(iagray(iathreshad(bHMT(loadedImage, loadedSEFG, loadedSEBG), uint8(50))), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_THRESH50", resultPath, currentHMTL)

                #loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                #resultImage = rHMT(loadedImage, loadedSEFG, loadedSEBG)
                #resultImage[resultImage < 0] = 0
                #resultImage[resultImage != 0] = 255
                #resultImage = uint8(resultImage)
                
                #addImageToHMTL(resultImage, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_POSVALUES", resultPath, currentHMTL)

                #resultImage2 = iadil(resultImage, iasedisk(10))
                #addImageToHMTL(resultImage2, imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName +"_POSVALUES_DILATEDISK10", resultPath, currentHMTL)

                #RGHMT takes forever
                loadedImage = cv2.resize(loadedImage, (0,0), fx=0.3, fy=0.3)
                resultImage = rgHMT(loadedImage, loadedSEFG, loadedSEBG)
                addImageToHMTL(resultImage, imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

                #POHMT is taking forever to calculate
                #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
                #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
                #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment3(experimentName, initialFolder, resultPath="ResultImage"):

    fg = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
    bg = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    folder = initialFolder

    try:

        print "Evaluating images in folder : " + folder 
        
        loadedSEFG = fg
        seFGFileName = "default"

        loadedSEBG = bg
        seBGFileName = "default"
                                
        for image in os.listdir(folder):
            print "\t\t\tEvaluation image : " + image
            imageFileName = os.path.splitext(image)[0]

            loadedImage = openImage(folder + "\\" + image)                    
            addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

            addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

            ksHMTResult = ksHMT(loadedImage, loadedSEFG)
            addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

            addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #RGHMT takes forever
            #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #POHMT is taking forever to calculate
            #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
            #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
            #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment4(experimentName, initialFolder, resultPath="ResultImage"):

    fg = iabinary([[0,128,128,128,0],[0,128,128,128,0],[0,0,0,0,0],[0,0,0,0,0],[0,128,128,128,0],[0,128,128,128,0]])
    bg = iasereflect(ianeg(iabinary([[0,20,20,20,0],[0,20,20,20,0],[0,0,0,0,0],[0,0,0,0,0],[0,20,20,20,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    folder = initialFolder

    try:

        print "Evaluating images in folder : " + folder 
        
        loadedSEFG = fg
        seFGFileName = "default"

        loadedSEBG = bg
        seBGFileName = "default"
                                
        for image in os.listdir(folder):
            print "\t\t\tEvaluation image : " + image
            imageFileName = os.path.splitext(image)[0]

            loadedImage = openImage(folder + "\\" + image)                    
            addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

            addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

            ksHMTResult = ksHMT(loadedImage, loadedSEFG)
            addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

            addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #RGHMT takes forever
            #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #POHMT is taking forever to calculate
            #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
            #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
            #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment5(experimentName, initialFolder, resultPath="ResultImage"):

    fg = iabinary([[0,128,128,128,0],[0,128,128,128,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,128,128,128,0]])
    bg = iasereflect(ianeg(iabinary([[0,20,20,20,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,20,20,20,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    folder = initialFolder

    try:

        print "Evaluating images in folder : " + folder 
        
        loadedSEFG = fg
        seFGFileName = "default"

        loadedSEBG = bg
        seBGFileName = "default"
                                
        for image in os.listdir(folder):
            print "\t\t\tEvaluation image : " + image
            imageFileName = os.path.splitext(image)[0]

            loadedImage = openImage(folder + "\\" + image)                    
            addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

            addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

            ksHMTResult = ksHMT(loadedImage, loadedSEFG)
            addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

            addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #RGHMT takes forever
            #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #POHMT is taking forever to calculate
            #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
            #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
            #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment6(experimentName, initialFolder, resultPath="ResultImage"):

    fg = iabinary([[0,128,128,128,0],[0,128,128,128,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,128,128,128,0]])
    bg = iasereflect(ianeg(iabinary([[0,20,20,20,0],[0,200,200,200,0],[0,200,200,200,0],[0,200,200,200,0],[0,200,200,200,0],[0,20,20,20,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    folder = initialFolder

    try:

        print "Evaluating images in folder : " + folder 
        
        loadedSEFG = fg
        seFGFileName = "default"

        loadedSEBG = bg
        seBGFileName = "default"
                                
        for image in os.listdir(folder):
            print "\t\t\tEvaluation image : " + image
            imageFileName = os.path.splitext(image)[0]

            loadedImage = openImage(folder + "\\" + image)                    
            addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

            addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

            ksHMTResult = ksHMT(loadedImage, loadedSEFG)
            addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

            addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #RGHMT takes forever
            #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #POHMT is taking forever to calculate
            #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
            #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
            #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)



def runExperiment7(experimentName, initialFolder, resultPath="ResultImage"):

    fg = array([[0,128,128,128,0],[0,128,128,128,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,128,128,128,0]])
    bg = iasereflect(ianeg(array([[0,128,128,128,0],[0,128,128,128,0],[0,128,128,128,0],[0,128,128,128,0],[0,128,128,128,0],[0,128,128,128,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    folder = initialFolder

    try:

        print "Evaluating images in folder : " + folder 
        
        loadedSEFG = fg
        seFGFileName = "default"

        loadedSEBG = bg
        seBGFileName = "default"
                                
        for image in os.listdir(folder):
            print "\t\t\tEvaluation image : " + image
            imageFileName = os.path.splitext(image)[0]

            loadedImage = openImage(folder + "\\" + image)                    
            addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

            addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

            ksHMTResult = ksHMT(loadedImage, loadedSEFG)
            addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

            addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #RGHMT takes forever
            #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #POHMT is taking forever to calculate
            #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
            #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
            #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)



        
def runExperiment8(experimentName, initialFolder, resultPath="ResultImage"):

    fg = array([[0,1,1,1,0],[0,1,1,1,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,1,1,1,0]])
    bg = iasereflect(ianeg(array([[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    folder = initialFolder

    try:

        print "Evaluating images in folder : " + folder 
        
        loadedSEFG = fg
        seFGFileName = "default"

        loadedSEBG = bg
        seBGFileName = "default"
                                
        for image in os.listdir(folder):
            print "\t\t\tEvaluation image : " + image
            imageFileName = os.path.splitext(image)[0]

            loadedImage = openImage(folder + "\\" + image)                    
            addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

            addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

            ksHMTResult = ksHMT(loadedImage, loadedSEFG)
            addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

            addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #RGHMT takes forever
            #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #POHMT is taking forever to calculate
            #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
            #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
            #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


def runExperiment9(experimentName, initialFolder, resultPath="ResultImage"):

    fg = array([[0,20,20,20,0],[0,20,20,20,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,20,20,20,0]])
    bg = iasereflect(ianeg(array([[0,20,20,20,0],[0,20,20,20,0],[0,20,20,20,0],[0,20,20,20,0],[0,20,20,20,0],[0,20,20,20,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    folder = initialFolder

    try:

        print "Evaluating images in folder : " + folder 
        
        loadedSEFG = fg
        seFGFileName = "default"

        loadedSEBG = bg
        seBGFileName = "default"
                                
        for image in os.listdir(folder):
            print "\t\t\tEvaluation image : " + image
            imageFileName = os.path.splitext(image)[0]

            loadedImage = openImage(folder + "\\" + image)                    
            addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

            addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

            ksHMTResult = ksHMT(loadedImage, loadedSEFG)
            addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

            addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #RGHMT takes forever
            #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #POHMT is taking forever to calculate
            #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
            #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
            #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

def runExperiment10(experimentName, initialFolder, resultPath="ResultImage"):

    fg = iabinary([[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0]])
    bg = iasereflect(ianeg(iabinary([[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0]])))

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    folder = initialFolder

    try:

        print "Evaluating images in folder : " + folder 
        
        loadedSEFG = fg
        seFGFileName = "default"

        loadedSEBG = bg
        seBGFileName = "default"
                                
        for image in os.listdir(folder):
            print "\t\t\tEvaluation image : " + image
            imageFileName = os.path.splitext(image)[0]

            loadedImage = openImage(folder + "\\" + image)                    
            addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

            addImageToHMTL(erode(loadedImage, loadedSEFG), imageFileName + "_Erosion_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(erode(loadedImage, loadedSEBG), imageFileName + "_Erosion_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(dilate(loadedImage, loadedSEFG), imageFileName + "_Dilate_SEFG_" + seFGFileName , resultPath, currentHMTL)
            addImageToHMTL(dilate(loadedImage, loadedSEBG), imageFileName + "_Dilate_SEBG_" + seBGFileName , resultPath, currentHMTL)

            ksHMTResult = ksHMT(loadedImage, loadedSEFG)
            addImageToHMTL(ksHMTforShow(ksHMTResult), imageFileName + "_KSHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

            addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            addImageToHMTL(rHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #RGHMT takes forever
            #addImageToHMTL(rgHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_RGHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

            #POHMT is taking forever to calculate
            #addImageToHMTL(poHMT(loadedImage, loadedFGSE,
            #loadedBGSE,75), "POHMT75_"+image+"_SE_"+seFG ,
            #resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

