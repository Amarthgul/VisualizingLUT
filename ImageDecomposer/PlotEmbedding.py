
# This file is for testing plot embedding in PyQt5
import os
import sys


import pandas as pd

from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (QFileDialog, 
                             QDialog, QApplication, QWidget, QMainWindow, 
                             QAction, QVBoxLayout, QSizePolicy)


import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from UI_MainWindow import Ui_MainWindow
from ColorCube import ColorCube 



_DEBUGGING = False

#class MplCanvas(FigureCanvas):

#    def __init__(self, parent=None, width=5, height=4, dpi=100):
#        fig = Figure(figsize=(width, height), dpi=dpi)
#        self.axes = fig.add_subplot(111)
#        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        cc_rgb = ColorCube()
        cc_rgb.mode = 'rgb'
        layout_rgb = self.RGB_Area.layout()
        if layout_rgb is None:
            layout_rgb = QVBoxLayout(self.RGB_Area)
        ax_rgb = cc_rgb.ShowPlot()
        canvas_rbg = FigureCanvas(ax_rgb.figure)
        ax_rgb.mouse_init()
        layout_rgb.addWidget(canvas_rbg)

        cc_hsv = ColorCube()
        cc_hsv.mode = 'hsv'
        layout_hsv = self.HSV_Area.layout()
        if layout_hsv is None:
            layout_hsv = QVBoxLayout(self.HSV_Area)
        ax_hsv = cc_hsv.ShowPlot()
        canvas_hsv = FigureCanvas(ax_hsv.figure)
        ax_hsv.mouse_init()
        layout_hsv.addWidget(canvas_hsv)



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
