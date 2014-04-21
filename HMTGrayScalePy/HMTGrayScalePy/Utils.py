from PIL import Image
from numpy import *
import webbrowser

def openImage(path):
    img = Image.open(path).convert('L')
    img = asarray(img)
    img.dtype = 'uint8' #force grayscale
    return img

def saveImage(img,title='image'):    
    img = uint8(img)
    Image.fromarray(img).save('ResultImage\\' + title + '.png')
    return 'ResultImage\\' + title + '.png'

def showImage(img,title='image'):
    Image.fromarray(img).show(title)

def saveAndShowImage(img, title='image'):
    webbrowser.open(saveImage(img, title))

def diffBetweenImages(original, calculated):
    return original == calculated