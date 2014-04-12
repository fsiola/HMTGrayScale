import ImageQt
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from GUI import *

from HMT import *
from Utils import *

#variables
openWindowAfterOperation = True
saveImageAfterOperation = True
fileNameImage = ''
fileNameFG = ''
fileNameBG = ''
seFG = None
seBG = None
loadedImage = None
ksHMTResult = None
suHMTResult = None
bHMTResult = None
rHMTResult = None
rgHMTResult = None


def loadImage():
    global loadedImage
    try:
        filePath = str(ui.txtFileName.text())
        if(filePath == ''): filePath = 'C:\Users\Felipe\Documents\GitHub\HMTGrayScale\HMTGrayScalePy\HMTGrayScalePy\TestImages\\binarySquare.png'
        loadedImage = openImage(filePath)

        #show image
        pixmap = QtGui.QPixmap(filePath, '1')
        ui.lblImage.setPixmap(pixmap)

        ui.tabWidget.setCurrentIndex(0)

    except:
        print 'error: ', sys.exc_info()[0]

def generateSEFG():
    global seFG
    try:
        funcFG = str(ui.txtSEFG.text())
        if(funcFG == ''): funcFG = 'iasebox(10)'
        seFG = eval(funcFG)
        
        if len(seFG.shape) == 1:
            seFG = expand_dims(seFG,0)

        temp = seFG
        title = 'seFG'

        #expand se
        if(seFG.dtype == 'bool'):
            temp = iaseshow(seFG, 'expand')
            temp.dtype = 'uint8'
            temp[temp == 1] = 255

            
        pixmap = QtGui.QPixmap(saveImage(temp,title), '1')
        ui.lblSEFGImage.setPixmap(pixmap)
        ui.tabWidget.setCurrentIndex(1)
        
    except:
        print 'error: ', sys.exc_info()[0]

def generateSEBG():
    global seBG
    try:
        funcBG = str(ui.txtSEBG.text())
        if(funcBG == ''): funcBG = 'iasecross(10)'
        
        seBG = eval(funcBG)
        
        if len(seBG.shape) == 1:
            seBG = expand_dims(seBG,0)

        temp = seBG
        title = 'seBG'       

        #expand se
        if(seBG.dtype == 'bool'):
            temp = iaseshow(seBG, 'expand')
            temp.dtype = 'uint8'
            temp[temp == 1] = 255
            
        pixmap = QtGui.QPixmap(saveImage(temp,title), '1')
        ui.lblSEBGImage.setPixmap(pixmap)
        ui.tabWidget.setCurrentIndex(2)        
    except:
        print 'error: ', sys.exc_info()[0]

def executeKSHMT():
    global ksHMTResult, loadedImage, seFG
    ksHMTResult = ksHMT(loadedImage, seFG)    
    pixmap = QtGui.QPixmap(saveImage(ksHMTResult,'kshtm'), '1')
    ui.lblKSHMTImage.setPixmap(pixmap)
    ui.tabWidget.setCurrentIndex(3)

def executeSUHMT():
    global suHMTResult, loadedImage, seFG, seBG
    suHMTResult = suHMT(loadedImage, seFG, seBG)
    pixmap = QtGui.QPixmap(saveImage(suHMTResult,'suhmt'), '1')
    ui.lblSUHMTImage.setPixmap(pixmap)
    ui.tabWidget.setCurrentIndex(4)

def executeBAHMT():
    global bHMTResult, loadedImage, seFG, seBG
    bHMTResult = bHMT(loadedImage, seFG, seBG)
    pixmap = QtGui.QPixmap(saveImage(bHMTResult,'bahmt'), '1')
    ui.lblKSHMTImage.setPixmap(pixmap)
    ui.tabWidget.setCurrentIndex(5)

def executeROHMT():
    global rHMTResult, loadedImage, seFG, seBG
    rHMTResult =rHMT(loadedImage, seFG, seBG)
    pixmap = QtGui.QPixmap(saveImage(rHMTResult,'rohmt'), '1')
    ui.lblKSHMTImage.setPixmap(pixmap)
    ui.tabWidget.setCurrentIndex(6)

def executeRGHMT():
    global rgHMTResult, loadedImage, seFG, seBG
    rgHMTResult = rgHMT(loadedImage, seFG, seBG)
    pixmap = QtGui.QPixmap(saveImage(rgHMTResult,'rghmt'), '1')
    ui.lblKSHMTImage.setPixmap(pixmap)
    ui.tabWidget.setCurrentIndex(7)

def executeALLHMT():
    global rgHMTResult
    executeKSHMT()
    executeSUHMT()
    executeBAHMT()
    executeROHMT()
    executeRGHMT()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(Form)

    app.connect(ui.btnLoadImage, SIGNAL("clicked()"), loadImage)
    app.connect(ui.btnSEFG, SIGNAL("clicked()"), generateSEFG)
    app.connect(ui.btnSEBG, SIGNAL("clicked()"), generateSEBG)

    app.connect(ui.btnKSHMT, SIGNAL("clicked()"), executeKSHMT)
    app.connect(ui.btnSUHMT, SIGNAL("clicked()"), executeSUHMT)
    app.connect(ui.btnBAHMT, SIGNAL("clicked()"), executeBAHMT)
    app.connect(ui.btnROHMT, SIGNAL("clicked()"), executeROHMT)
    app.connect(ui.btnRGHMT, SIGNAL("clicked()"), executeRGHMT)
    app.connect(ui.btnAll, SIGNAL("clicked()"), executeALLHMT)
    
    Form.show()
    sys.exit(app.exec_())

