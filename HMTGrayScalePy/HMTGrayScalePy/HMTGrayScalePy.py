import numpy
from numpy import *

#General TODOs
#make the origin of the SE its center point (or approx.)

#internet
def rolling_window_lastaxis(a, window):
    """Directly taken from Erik Rigtorp's post to numpy-discussion.
    <http://www.mail-archive.com/numpy-discussion@scipy.org/msg29450.html>"""
    if window < 1:
       raise ValueError, "`window` must be at least 1."
    if window > a.shape[-1]:
       raise ValueError, "`window` is too long."
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return numpy.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def rolling_window(a, window):
    if not hasattr(window, '__iter__'):
        return rolling_window_lastaxis(a, window)
    for i, win in enumerate(window):
        if win > 1:
            a = a.swapaxes(i, -1)
            a = rolling_window_lastaxis(a, win)
            a = a.swapaxes(-2, i)
    return a

#complement of array - so far only works with uint8 arrays
def complement(X):
    max = X.ravel().max()
    tipo = uint8

    #TODO: complete for other cases (ex.  float)
    if max == 1:
        tipo = bool
            
    return numpy.invert(X, dtype=tipo)

#intersection between 2 arrays of any type
def intersection(X,Y):
    return minimum(X,Y).astype(X.dtype)

#binary erosion between X and B
#TODO: smart implementation.  the one used here is the easiest one to do
#TODO: X.shape fails for 1D arrays
def binaryErodeUsingCounting(X, B):
    hX,wX = X.shape 
    hB,wB = B.shape 
    numberOfOnesInB = count_nonzero(B)
    resultImage = zeros(X.shape)
    for x in range(1,hX - 1): #not workin with borders
        for y in range(1,wX - 1): #not workin with borders
            numberOfMatches = 0
            for i in range(-(hB - 1) / 2,(hB + 1) / 2):
                for j in range(-(wB - 1) / 2,(wB + 1) / 2):
                    if B[abs(-(hB - 1) / 2 - i),abs(-(wB - 1) / 2 - j)] == 1 and X[x + i,y + j] == 1:
                       numberOfMatches+=1
            if numberOfMatches == numberOfOnesInB:
                resultImage[x,y] = 1
    return resultImage

#erosion between X and binary B using rank-order
def erode(X, B):

    if len(X.shape) == 1:
        X = expand_dims(X,0)

    if len(B.shape) == 1:
        B = expand_dims(B,0)

    #testing for 1x1 structuring element binary case
    if B.shape[0] == 1 and B.shape[1] == 1:
        return X

    resultImage = zeros(X.shape)
    windows = rolling_window(X,B.shape)
    for x in range(int(floor(B.shape[0] / 2)), int(floor(X.shape[0] - B.shape[0] / 2))):
        for y in range(int(floor(B.shape[1] / 2)), int(floor(X.shape[1] - B.shape[1] / 2))):
            
            resultImage[x,y] = rankOrder(windows[x - 1,y - 1],B,0)
    return resultImage

#binary hit-or-miss based on erode operation
def binhmt(X, Bfg, Bbg):

    if Bfg.shape != Bbg.shape:
        raise Exception('SEs with different shapes')

    if sum(intersection(Bfg, Bbg).ravel()) != 0:
        raise Exception('SEs with intersection not empty')

    return intersection(erode(X, Bfg), erode(complement(X), Bbg))

#rank order operation: takes input array X and mask array B and return the k-th
#element (starting from 0 index)
def rankOrder(X, B, k):
    temp = X.ravel()[B.ravel() > 0].ravel()
    temp.sort()

    if(k >= len(temp)):
       k = len(temp)-1

    return temp[k]

#Khosravi and Schafer Hit-Or-Miss Transform
#M.  Khosravi e R.  W.  Schafer.  Template matching based on a grayscale
#hit-or-miss transform.  IEEE Transactions on Image Processing, 5(6):1060
#{1066.  ISSN 1057-7149.  doi: 10.1109/83.503921.  Citado na pag.  1, 21, 22,
#26
def ksHMT(f,B):    
    #TODO: check types

    if len(f.shape) == 1:
        f = expand_dims(f,0)

    if len(B.shape) == 1:
        B = expand_dims(B,0)

    resultImage = zeros(f.shape)
    windows = rolling_window(f,B.shape)
    
    for x in range(int(floor(B.shape[0] / 2)), int(floor(f.shape[0] - B.shape[0] / 2))):
        for y in range(int(floor(B.shape[1] / 2)), int(floor(f.shape[1] - B.shape[1] / 2))):

            resultImage[x,y] = rankOrder(windows[x - 1,y - 1],B,0) - rankOrder(windows[x - 1,y - 1],B,B.ravel().shape[0])
    return resultImage
    
    return