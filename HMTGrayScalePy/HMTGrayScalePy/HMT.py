from numpy import *
from scipy.ndimage import *
from ia636 import *
from ia870 import *

#Khosravi and Schafer Hit-Or-Miss Transformation
def ksHMT(f, b):
    erosionFB = iaero(f, b)
    fMinus = ianeg(f)
    bMinus = ianeg(b)
    erosionFMinusBMinus = iaero(fMinus, bMinus)
    result = erosionFB + erosionFMinusBMinus
    return result

#Soille Unconstrained Hit-Or-Miss Transformation
def suHMT(f,bfg, bbg):
    #[SUHMT_b(f)](x) = card {t : (Bfg)x esta contido em CSt(f) e (Bbg)x esta contido em (CSt(f))^c}
    #[SUHMT_b(f)](x) = [erosao_{Bfg}(f)](x) - [dil_{Bbg}(f)](x)     se dil <= ero
    #                  0  cc.

    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(bfg.shape) == 1:
        bfg = expand_dims(bfg,0)

    if len(bbg.shape) == 1:
        bbg = expand_dims(bbg,0)

    eroFBfg = iaero(f, bfg)
    dilBbg = iadil(f, bbg)

    resultImage = zeros(f.shape)

    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            if(dilFBbg[x][y] <= eroFBfg[x][y]):
                resultImage[x][y] = ero[x][y] - dilFBbg[x][y]

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