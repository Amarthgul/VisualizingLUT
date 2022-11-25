

import PIL.Image as img
import os

# For GUI to display 
from UI_MainWindow import Ui_MainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic



_DEBUGGING = False


def Main():  
    if _DEBUGGING:
        print("CSE 5544")
        
    else:
        app = QtWidgets.QApplication(sys.argv)

        class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
            def __init__(self, *args, obj=None, **kwargs):
                super(MainWindow, self).__init__(*args, **kwargs)
                self.setupUi(self)

        window = MainWindow()
        window.show()
        app.exec()


if __name__ == '__main__':
    Main()

# The following are from another script and has little to do with CSE5544 project.
# They are put here merely as reference or placeholder 

# Although the image finding functions may be of help

def getCurrentFolder():
    current = str(os.path.abspath(__file__))
    for itera in range(len(current) - 1, 0, -1):
        if current[itera] == '\\':
            dir = current[0: itera] #Get current directory
            break;
    return dir

def findWebp():
    '''Find webp fomat files'''
    files = os.listdir(getCurrentFolder())

    webps = []
    for f in files:
        print(f.lower()[-4:])
        if f.lower()[-4:] == "webp":
            webps.append(f)

    return webps

def openAndConvert(fileNames = [], targetFormat ="png"):
    '''Given the files, open them and convert to another format and then save'''

    outDir = getCurrentFolder() + '\\OutputImages\\'
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for name in fileNames:
        im = img.open(name).convert("RGB")
        noExtName = name[:-5]
        im.save(outDir + noExtName + '.' + targetFormat)


