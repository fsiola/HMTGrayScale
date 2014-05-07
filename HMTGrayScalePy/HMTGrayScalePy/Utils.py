from PIL import Image
from numpy import *
import webbrowser
import os
from HMT import *

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

                        addImageToHMTL(bHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_BHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName , resultPath, currentHMTL)

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

