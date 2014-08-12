import sys
from numpy import *
from ia636 import *
from ia870 import *
from PIL import Image

#Khosravi and Schafer Hit-Or-Miss Transformation
#input: image and gray level se
#output: image result with values from -255 to 0, where higher values (closer to 0) are better matches
def ksHMT(f, bfg):

    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(bfg.shape) == 1:
        bfg = expand_dims(bfg,0)
        
    eroFBfg = iaero(int32(f), bfg)
    eroMFMBfg = iaero(ianeg(int32(f)), ianeg(int32(bfg)))
    
    resultImage = eroFBfg + eroMFMBfg + 1
    resultImage[resultImage > 20000] = -255 #fixing overflow
    resultImage[resultImage < -255] = 0 #fixing overflow
    
    return resultImage

#KSHMT for showing in screen (adapting values for input since KSHMT return negative values)
#input: image and gray level se - (calls ksHMT)
#output: image result inversed with values from 0 to 255, where higher values are better matches
def ksHMTforShow(f, bfg):
    return ksHMT(f, bfg) + 255

#KSHMT for showing in screen (adapting values for input since KSHMT return negative values)
#input: image result from ksHMT
#output: image result inversed with values from 0 to 255, where higher values are better matches
def ksHMTforShow(ksHMTresult):
    return ksHMTresult + 255

#Soille Unconstrained Hit-Or-Miss Transformation
#input: image and gray level ses
#output: image result  with values from 0 to 255, where higher values are better matches
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

    bbg = iasereflect(ianeg(bbg))

    eroFBfg = iaero(int32(f), bfg)
    dilFBbg = iadil(int32(f), bbg)

    eroFBfg = int16(eroFBfg)
    dilFBbg = int16(dilFBbg)

    resultImage = zeros(f.shape, dtype='int16')

    resultImage = eroFBfg - dilFBbg
    resultImage[resultImage<0]=0
    
    return resultImage

#Barat Hit-or-Miss Transformation
#input: image and gray level ses
#output: image result  with values from -255 to 255, where lower values are better matches
def bHMT(f, bfg, bbg):
    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(bfg.shape) == 1:
        bfg = expand_dims(bfg,0)

    if len(bbg.shape) == 1:
        bbg = expand_dims(bbg,0)

    #bbg = iasereflect(ianeg(bbg))

    eroFBfg = iaero(int32(f), bfg)
    dilFBbg = iadil(int32(f), bbg)

    eroFBfg[eroFBfg == sys.maxint] = -255 #fixing overflow
    eroFBfg[eroFBfg < -255] = 0 #fixing overflow    

    dilFBbg[dilFBbg == sys.maxint] = -255 #fixing overflow
    dilFBbg[dilFBbg < -255] = 0 #fixing overflow    

    eroFBfg = int16(eroFBfg)
    dilFBbg = int16(dilFBbg)

    resultImage = zeros(f.shape, dtype='int16')

    resultImage = dilFBbg - eroFBfg
    
    resultImage[resultImage < -255] = 0 #fixing overflow    

    if(max(resultImage.ravel()) > 255):
        resultImage = resultImage - (max(resultImage.ravel())-255)

    resultImage[resultImage > 255] = 255 #fixing overflow    

    return resultImage    

#BHMT for showing in screen
#input: image and gray level ses
#output: image result inversed with values from 0 to 255, where higher values are better matches
def bHMTforShow(f, bfg, bbg):
    return (bHMT(f, bfg, bbg) + 255)/2

#BHMT for showing in screen
#input: image result from BHMT
#output: image result inversed with values from 0 to 255, where higher values are better matches
def bHMTforShow(bHMTresult):
    return (bHMTresult + 255)/2

#Ronse Hit-Or-Miss Transformation
#input: image and gray level ses
#output: image result  with values from -255 to 255, where higher values are better matches
def rHMT(f, bfg, bbg):
    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(bfg.shape) == 1:
        bfg = expand_dims(bfg,0)

    if len(bbg.shape) == 1:
        bbg = expand_dims(bbg,0)

    #bbg = iasereflect(ianeg(bbg))

    eroFBfg = iaero(int32(f), int32(bfg))
    dilFBbg = iadil(int32(f), int32(bbg))

#    eroFBfg = int16(eroFBfg)
#    dilFBbg = int16(dilFBbg)

    resultImage = zeros(f.shape, dtype='int32')

    maxValue = max(max(max(eroFBfg.ravel()), max(dilFBbg.ravel())) + 1, 255)

    resultImage = zeros(f.shape)

    resultImage = eroFBfg
    resultImage[resultImage >= dilFBbg] = maxValue
    resultImage[resultImage < 0] = 0 #fixing overflow
    
    return resultImage    

#Raducana and Grana Hit-Or-Miss Transformation
#input: image and gray level ses
#output: image result  with values from 0 to 255, where higher values are better matches
def rgHMT(f, bfg, bbg):
    #[RGHMT_b(f)](x) = sup_{t \in t_max} (x \in HMT_b_t(CSt(f))

    if len(f.shape) == 1:
        f = expand_dims(f,0)

    maxF = int(max(f.ravel()))

    resultImage = zeros(f.shape, dtype = 'int32')

    #bbg = ianeg(bbg)

    for t in range(maxF):
        tempF = zeros(f.shape)
        tempBfg = zeros(bfg.shape)
        tempBbg = zeros(bbg.shape)

        tempF = bool_(tempF)
        tempBfg = bool_(tempBfg)
        tempBbg = bool_(tempBbg)

        tempF[where(f <= t)] = True
        tempBfg[where(bfg <= t)] = True
        tempBbg[where(bbg <= t)] = True
        tempBbg[where(iaintersec(tempBfg,tempBbg) == True)] = False #removing intersecs (?)

        try:
            tempBinHMT = iasupgen(tempF, iase2hmt(tempBfg, tempBbg))
        except:
            tempBinHMT = bool_(zeros(tempF.shape))

        #not sure here
        resultImage += int32(tempBinHMT)

    resultImage = ianeg(int32(resultImage-255+f)) #diference between result and f
    return resultImage

######### POHMT

#returns markers
def poHMT(f, bfg, bbg, P):
    f = int16(f)
    bfg = int16(bfg)
    bbg = int16(bbg)   

    result = zeros(f.shape, dtype='int16')
    #assuming 2d arrays
    for x in range(f.shape[0]): #TODO: correct border
        for y in range(f.shape[1]):#TODO: correct border
            result[x][y] = poHMTint(f, bfg, bbg, x, y, P)

    return result

def poHMTint(f, bfg, bbg, x, y, P):
    if(po(f, bfg, bbg, x, y) >= P):
        return 255
    else:
        return 0

def po(f, bfg, bbg, x, y):
    maxV = 0
    for t in range(255):
        maxV = max(maxV, min(poFG(f, bfg, x, y,t), poBG(f, bbg, x, y, t)))        

def poFG(f, bfg, x, y, t):
    return (oFG(f, bfg, x, y, t)/(bfg.size))*100

def poBG(f, bbg, x, y, t):
    return (oBG(f, bbg, x, y, t)/(bbg.size))*100

def oFG(f, bfg, x, y, t):
    #assuming 2d arrays
    result = 0
    for a in range(bfg.shape[0]):
        for b in range(bfg.shape[1]):
            if ((x+a < f.shape[0] and y+b < f.shape[1])):
               if((f[x+a][y+b] + bfg[a][b]) >= t):
                    result+=1
    return result

def oBG(f, bbg, x, y, t):
    #assuming 2d arrays
    result = 0
    for a in range(bbg.shape[0]):
        for b in range(bbg.shape[1]):
            if ((x+a < f.shape[0] and y+b < f.shape[1])):
                if((f[x+a][y+b] + bbg[a][b]) < t):
                    result+=1
    return result


##########################################################################
def erode(img, se):
    return iaero(img, se)

def dilate(img, se):
    return iadil(img, se)
##########################################################################