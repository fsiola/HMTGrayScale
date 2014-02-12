import numpy
from numpy import *

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

    #TODO: complete for other cases (ex. float)
    if max == 1:
        tipo = bool
            
    return numpy.invert(X, dtype=tipo)

#intersection between 2 arrays of any type
def intersection(X,Y):
    return minimum(X,Y).astype(X.dtype)

#binary erosion between X and B 
#TODO: smart implementation. the one used here is the easiest one to do
#TODO: X.shape fails for 1D arrays
def binaryErodeUsingCounting(X, B):
    hX,wX = X.shape 
    hB,wB = B.shape 
    numberOfOnesInB = count_nonzero(B)
    resultImage = zeros(X.shape)
    for x in range(1,hX-1): #not workin with borders
        for y in range(1,wX-1): #not workin with borders
            numberOfMatches = 0
            for i in range(-(hB-1)/2,(hB+1)/2):
                for j in range(-(wB-1)/2,(wB+1)/2):
                    if B[abs(-(hB-1)/2 - i),abs(-(wB-1)/2 - j)] == 1 and X[x+i,y+j] == 1:
                       numberOfMatches+=1
            if numberOfMatches == numberOfOnesInB:
                resultImage[x,y]=1
    return resultImage

#erosion between X and binary B using rank-order 
def erode(X, B):

    #testing for 1x1 structuring element binary case
    if B.shape[0] == 1 and B.shape[1] == 1:
        return X

    resultImage = zeros(X.shape)
    windows = rolling_window(X,B.shape)
    for x in range(int(X.shape[0]-floor(X.shape[0])), int(floor(X.shape[0]-1))): 
        if x == int(X.shape[0]-floor(X.shape[0])): #border condition
            continue
        for y in range(int(X.shape[0]-floor(X.shape[1])), int(floor(X.shape[1]-1))):
            if y == int(X.shape[0]-floor(X.shape[1])):
                continue
            
            resultImage[x,y] = rankOrder(windows[x-1,y-1],B,0)
    return resultImage

#binary hit-or-miss based on erode operation
def binhmt(X, Bfg, Bbg):
    return intersection(erode(X, Bfg), erode(complement(X), Bbg))

#rank order operation: takes input array X and mask array B and return the k-th element (starting from 0 index)
def rankOrder(X, B, k):
    temp = X.ravel()[B.ravel()>0].ravel()
    temp.sort()
    return temp[k]