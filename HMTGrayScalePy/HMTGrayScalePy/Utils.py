from PIL import Image
from numpy import *

def openImage(path):
    img = Image.open(path).convert('L')
    img = asarray(img)
    img.dtype = 'uint8' #force grayscale
    return img

def saveImage(img,title='image'):    
    img.dtype='uint8'
    Image.fromarray(img).save('ResultImage\\' + title + '.png')
    return 'ResultImage\\' + title + '.png'

def showImage(img,title='image'):
    Image.fromarray(img).show(title)