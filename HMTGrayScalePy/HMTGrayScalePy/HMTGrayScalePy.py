from numpy import *

#complement of array - so far only works with uint8 arrays
#TODO: switch over max value in array
def complement(X):
    return numpy.invert(X, dtype=uint8)

#intersection between 2 arrays of any type
def intersection(X,Y):
    return minimum(X,Y).astype(X.dtype)

#binary erosion between X and B 
#TODO: smart implementation. the one used here is the easiest one to do
#TODO: X.shape fails for 1D arrays
def binaryErode(X, B):
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

#binary hit-or-miss based on erode operation
def binhmt(X, Bfg, Bbg):
    return intersection(binaryErode(X, Bfg), binaryErode(complement(X), Bbg))

a = array([[0,0,1,1,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,1,1,1],[0,1,0,1,0]])
b = array([[0,1,0],[1,1,1],[0,1,0]])
print a
print b
print binaryErode(a,b)

