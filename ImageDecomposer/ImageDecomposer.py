import PIL.Image as img
import os

# For GUI to display 
from UI_MainWindow import Ui_MainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic



_DEBUGGING = False

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Too connect a method to a botton:
        # self.NAME.clicked.connect(self.onClick)
            

def Main():  
    if _DEBUGGING:
        print("CSE 5544")
        
    else:
        app = QtWidgets.QApplication(sys.argv)

        window = MainWindow()
        window.show()
        app.exec()


if __name__ == '__main__':
    Main()



