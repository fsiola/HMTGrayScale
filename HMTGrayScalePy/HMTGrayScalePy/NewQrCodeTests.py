from Utils import *
from HMT import *


####Experimento que utiliza os SEs fornecidos pela profa Nina para executar com a definição de Soille nas imagens de QR-Code
####a ideia é rodar todas as imagens em cima do SEs original, sem reduzir a imagem
####depois aumentamos o tamanho do SE e rodamos em todas as imagens sem agrupar os resultados (isso 3 vezes)
def runExperiment1QrCode_SU(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False):
    resultPath = resultPath + "\\" + experimentName
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:
        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]
    

        #tamanhos originais
        fg1 = iabinary([[1,0,0],[1,0,0],[0,0,0],[0,0,1],[0,0,1]])
        bg1 = iasereflect(ianeg(iabinary([[0,0,1],[0,0,1],[0,0,0],[1,0,0],[1,0,0]])))

        fg2 = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
        bg2 = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

        fg3 = iabinary([[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1]])
        bg3 = iasereflect(ianeg(iabinary([[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0]])))

        arrayFGs = [fg1,fg2,fg3]
        arrayBGs = [bg1,bg2,bg3]
        
        for i in range(3):
            print "Evaluating with SEs images : ",i 

            for folder in imageFolders:
                print "\tEvaluating images in folder : " + folder 
        
                loadedSEFG = arrayFGs[i]
                seFGFileName = "size"+repr(i)

                loadedSEBG = arrayBGs[i]
                seBGFileName = "size"+repr(i)
                    
                for image in os.listdir(folder):
                    print "\t\tEvaluation image : " + image
                    imageFileName = os.path.splitext(image)[0]

                    loadedImage = openImage(folder + "\\" + image)                    
                    addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)
                    
                    addImageToHMTL(suHMT(loadedImage, loadedSEFG, loadedSEBG), imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  , resultPath, currentHMTL)

                    resultImage = ianeg(cv2.adaptiveThreshold(uint8(suHMT(loadedImage, loadedSEFG, loadedSEBG)),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                    addImageToHMTL(resultImage, imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH_RESIZE", resultPath, currentHMTL)

                    resultImage2 = iadil(resultImage,iasedisk(10))
                    addImageToHMTL(resultImage2, imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH_RESIZE_DILATE10x10", resultPath, currentHMTL)

                    resultImage3 = iaedgeoff(resultImage2)
                    addImageToHMTL(resultImage3, imageFileName + "_SUHMT_SEFG_" + seFGFileName + "_SEBG_" + seBGFileName  +"_ADAPTIVETHRESH_RESIZE_DILATE10x10_EDGEOFF", resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


####Experimento que utiliza os SEs fornecidos pela profa Nina para executar com a definição de Soille nas imagens de QR-Code
####a ideia é rodar todas as imagens em cima dos tres tamanhos de SEs, sem reduzir a imagem e fazer a soma das três, multiplicando por 85
def runExperiment2QrCode_SU(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False):
    resultPath = resultPath + "\\" + experimentName
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:
        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]    

        #tamanhos originais
        fg1 = iabinary([[1,0,0],[1,0,0],[0,0,0],[0,0,1],[0,0,1]])
        bg1 = iasereflect(ianeg(iabinary([[0,0,1],[0,0,1],[0,0,0],[1,0,0],[1,0,0]])))

        fg2 = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
        bg2 = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

        fg3 = iabinary([[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1]])
        bg3 = iasereflect(ianeg(iabinary([[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0]])))

        arrayFGs = [fg1,fg2,fg3]
        arrayBGs = [bg1,bg2,bg3]
        
        for folder in imageFolders:
            print "\tEvaluating images in folder : " + folder 
                    
            for image in os.listdir(folder):
                print "\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                partialImage = zeros(loadedImage.shape)
                    
                for i in range(3):
                    print "\t\t\tEvaluating with SEs images : ",i 
        
                    loadedSEFG = arrayFGs[i]                   
                    loadedSEBG = arrayBGs[i]
                    
                    resultImage = suHMT(loadedImage, loadedSEFG, loadedSEBG)
                    resultImage = ianeg(cv2.adaptiveThreshold(uint8(resultImage),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2))
                    resultImage = iadil(resultImage,iasedisk(10))
                    resultImage = iaedgeoff(resultImage)

                    partialImage += uint8(bool_(resultImage))

                addImageToHMTL(partialImage*85, imageFileName + "_SUHMT_SCALED_SES_COMBINED", resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)



####Experimento que utiliza os SEs fornecidos pela profa Nina para executar com a definição de Soille nas imagens de QR-Code
####a ideia é rodar todas as imagens em cima dos tres tamanhos de SEs, sem reduzir e sem threshold a imagem e fazer a soma das três, multiplicando por 85
def runExperiment3QrCode_SU(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False):
    resultPath = resultPath + "\\" + experimentName
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:
        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]    

        #tamanhos originais
        fg1 = iabinary([[1,0,0],[1,0,0],[0,0,0],[0,0,1],[0,0,1]])
        bg1 = iasereflect(ianeg(iabinary([[0,0,1],[0,0,1],[0,0,0],[1,0,0],[1,0,0]])))

        fg2 = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
        bg2 = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

        fg3 = iabinary([[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1]])
        bg3 = iasereflect(ianeg(iabinary([[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0]])))

        arrayFGs = [fg1,fg2,fg3]
        arrayBGs = [bg1,bg2,bg3]
        
        for folder in imageFolders:
            print "\tEvaluating images in folder : " + folder 
                    
            for image in os.listdir(folder):
                print "\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                partialImage = int16(zeros(loadedImage.shape))
                    
                for i in range(3):
                    print "\t\t\tEvaluating with SEs images : ",i 
        
                    loadedSEFG = arrayFGs[i]                   
                    loadedSEBG = arrayBGs[i]
                    
                    partialImage += int16(suHMT(loadedImage, loadedSEFG, loadedSEBG))                                   

                partialImage[partialImage > 255] = 255 #removing overflow
                partialImage = iaedgeoff(uint8(partialImage))
                partialImage = iadil(partialImage,iasedisk(10))                    
                addImageToHMTL(ianeg(partialImage), imageFileName + "_SUHMT_NOTHRESH_EDGEOFF_DILATED_NEG", resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)


####Experimento que utiliza os SEs fornecidos pela profa Nina para executar com a definição de Soille nas imagens de QR-Code
####a ideia é rodar todas as imagens em cima dos tres tamanhos de SEs, com 2 SEs disintitos, sem reduzir e sem threshold a imagem e fazer a soma das três, multiplicando por 42
def runExperiment4QrCode_SU(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False):
    resultPath = resultPath + "\\" + experimentName
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:
        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]    

        #tamanhos originais
        fg1 = iabinary([[1,0,0],[1,0,0],[0,0,0],[0,0,1],[0,0,1]])
        bg1 = iasereflect(ianeg(iabinary([[0,0,1],[0,0,1],[0,0,0],[1,0,0],[1,0,0]])))

        fg2 = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
        bg2 = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

        fg3 = iabinary([[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1]])
        bg3 = iasereflect(ianeg(iabinary([[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0]])))

        fg11 = iasereflect((iabinary([[1,0,0],[1,0,0],[0,0,0],[0,0,1],[0,0,1]])))
        bg11 = iasereflect(iasereflect(ianeg(iabinary([[0,0,1],[0,0,1],[0,0,0],[1,0,0],[1,0,0]]))))

        fg21 = iasereflect(iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]))
        bg21 = iasereflect(iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]]))))

        fg31 = iasereflect(iabinary([[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1]]))
        bg31 = iasereflect(iasereflect(ianeg(iabinary([[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0]]))))


        arrayFGs = [fg1,fg2,fg3,fg11,fg21,fg31]
        arrayBGs = [bg1,bg2,bg3,bg11,bg21,bg31]
        
        for folder in imageFolders:
            print "\tEvaluating images in folder : " + folder 
                    
            for image in os.listdir(folder):
                print "\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                partialImage = int16(zeros(loadedImage.shape))
                    
                for i in range(6):
                    print "\t\t\tEvaluating with SEs images : ",i 
        
                    loadedSEFG = arrayFGs[i]                   
                    loadedSEBG = arrayBGs[i]
                    
                    partialImage += int16(suHMT(loadedImage, loadedSEFG, loadedSEBG))                                   

                partialImage[partialImage > 255] = 255 #removing overflow
                partialImage = iaedgeoff(uint8(partialImage))
                partialImage = iadil(partialImage,iasedisk(10))                    
                addImageToHMTL(ianeg(partialImage), imageFileName + "_SUHMT_NOTHRESH_EDGEOFF_DILATED_NEG", resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)



####Experimento que utiliza os SEs fornecidos pela profa Nina para executar com a definição de Soille nas imagens de QR-Code
####a ideia é rodar todas as imagens em cima dos tres tamanhos de SEs e rotacionalos, sem reduzir e sem threshold a imagem e fazer a soma das três
def runExperiment5QrCode_SU(experimentName, initialFolder, resultPath="ResultImage", runOnlyObjectImages=False):
    resultPath = resultPath + "\\" + experimentName
    folderOnlyObject = initialFolder + "\\OnlyObject"
    folderGeneralImages = initialFolder + "\\General"

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    print "Starting experiment : " + experimentName 
    currentHMTL = createHMTL(experimentName, resultPath)

    imageFolders = [folderGeneralImages]

    try:
        if(runOnlyObjectImages):
            imageFolders += [folderOnlyObject]    

        #tamanhos originais
        fg1 = iabinary([[1,0,0],[1,0,0],[0,0,0],[0,0,1],[0,0,1]])
        bg1 = iasereflect(ianeg(iabinary([[0,0,1],[0,0,1],[0,0,0],[1,0,0],[1,0,0]])))

        fg2 = iabinary([[1,1,0,0,0],[1,1,0,0,0],[0,0,0,0,0],[0,0,0,1,1],[0,0,0,1,1]])
        bg2 = iasereflect(ianeg(iabinary([[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])))

        fg3 = iabinary([[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1]])
        bg3 = iasereflect(ianeg(iabinary([[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0],[1,1,1,1,0,0,0,0,0,0]])))

        arrayFGs = [fg1,fg2,fg3]
        arrayBGs = [bg1,bg2,bg3]
        
        for folder in imageFolders:
            print "\tEvaluating images in folder : " + folder 
                    
            for image in os.listdir(folder):
                print "\t\tEvaluation image : " + image
                imageFileName = os.path.splitext(image)[0]

                loadedImage = openImage(folder + "\\" + image)                    
                addImageToHMTL(loadedImage, imageFileName + "_Original", resultPath, currentHMTL)

                partialImage = int16(zeros(loadedImage.shape))
                    
                for i in range(3):
                    print "\t\t\tEvaluating with SEs images : ",i 
        
                    for j in range(4): #360/90
                        print "\t\t\t\tEvaluation with SE rotated : ", j , " times"
                    
                        loadedSEFG, loadedSEBG = iainterot((arrayFGs[i],arrayBGs[i]),j*90)

                        partialImage += int16(suHMT(loadedImage, loadedSEFG, loadedSEBG))                                   

                maxValue = max(partialImage.ravel())
                partialImage = uint8(partialImage/(255.0/maxValue))
                partialImage[partialImage > 255] = 255 #removing overflow
                partialImage = iaedgeoff(uint8(partialImage))
                partialImage = iadil(partialImage,iasedisk(10))                    
                addImageToHMTL(ianeg(partialImage), imageFileName + "_SUHMT_NOTHRESH_EDGEOFF_DILATED_NEG", resultPath, currentHMTL)

    except:
        print 'error: ', os.sys.exc_info()[0]
        
    finally:
        finishHTML(currentHMTL)

#runExperiment1QrCode_SU("Experiment_1_QRCodeSU", "G:\\Felipe\\Mestrado\\QRCode",'G:\\Felipe\\Mestrado\\ExperimentResultsNew', False)
#runExperiment2QrCode_SU("Experiment_2_QRCodeSU", "G:\\Felipe\\Mestrado\\QRCode",'G:\\Felipe\\Mestrado\\ExperimentResultsNew', False)
#runExperiment3QrCode_SU("Experiment_3_QRCodeSU", "G:\\Felipe\\Mestrado\\QRCode",'G:\\Felipe\\Mestrado\\ExperimentResultsNew', False)
#runExperiment4QrCode_SU("Experiment_4_QRCodeSU", "G:\\Felipe\\Mestrado\\QRCode",'G:\\Felipe\\Mestrado\\ExperimentResultsNew', False)
runExperiment5QrCode_SU("Experiment_5_QRCodeSU", "G:\\Felipe\\Mestrado\\QRCode",'G:\\Felipe\\Mestrado\\ExperimentResultsNew', False)


