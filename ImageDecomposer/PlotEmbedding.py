
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
from ReadImage import ImageDisplay
from Histogram import HistoDisplay

_DEBUGGING = False


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.imageDisp = ImageDisplay()
        self.histoDisp = HistoDisplay()
        self.cc_rgb = ColorCube('rgb')
        self.cc_hsv = ColorCube('hsv')

        self.index = 0

        self.histoDisp.SetImageData(self.imageDisp.GetCurrentData())

        self.NextImageButton.clicked.connect(self.inc)
        self.PreviousImageButton.clicked.connect(self.dec)
        self.GrayCardButton.clicked.connect(self.displayGrayCard)
        self.GradientButton.clicked.connect(self.displayGradient)

        self.Histo_All_Check.toggled.connect(self.CheckAll)
        self.Histo_R_Check.toggled.connect(self.CheckR)
        self.Histo_G_Check.toggled.connect(self.CheckG)
        self.Histo_B_Check.toggled.connect(self.CheckB)
        self.Histo_L_Check.toggled.connect(self.CheckL)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        '''====================================================='''
        '''================== Image Display ===================='''
        layoutImage = self.Image_Area.layout()
        if layoutImage is None:
            layoutImage = QVBoxLayout(self.Image_Area)
        ax_img = self.imageDisp.displayImage()
        canvas_image = FigureCanvas(ax_img.figure)
        layoutImage.addWidget(self.imageDisp)
        self.show()

        '''====================================================='''
        '''================ Histogram Display =================='''
        layoutHisto = self.histoFrame.layout()
        if layoutHisto is None:
            layoutHisto = QVBoxLayout(self.histoFrame)
        ax_hist = self.histoDisp.UpdateHist()
        canvas_hist = FigureCanvas(ax_hist.figure)
        layoutHisto.addWidget(self.histoDisp)
        self.show()

        '''====================================================='''
        '''================== RGB Color Cube ==================='''
        self.cc_rgb.mode = 'rgb'
        layout_rgb = self.RGB_Area.layout()
        if layout_rgb is None:
            layout_rgb = QVBoxLayout(self.RGB_Area)
        ax_rgb = self.cc_rgb.ShowPlot()
        canvas_rbg = FigureCanvas(ax_rgb.figure)
        ax_rgb.mouse_init()
        layout_rgb.addWidget(canvas_rbg)

        '''====================================================='''
        '''================== HSV Color Cube ==================='''
        self.cc_hsv.mode = 'hsv'
        layout_hsv = self.HSV_Area.layout()
        if layout_hsv is None:
            layout_hsv = QVBoxLayout(self.HSV_Area)
        ax_hsv = self.cc_hsv.ShowPlot()
        canvas_hsv = FigureCanvas(ax_hsv.figure)
        ax_hsv.mouse_init()
        layout_hsv.addWidget(canvas_hsv)


    def inc(self):
        self.imageDisp.nextImage()
        self.UpdateImages()
        
    def dec(self):
        self.imageDisp.lastImage()
        self.UpdateImages()

    def displayGrayCard(self):
        self.imageDisp.displayGrayCard()
        self.UpdateImages()

    def displayGradient(self):
        self.imageDisp.displayGradient()
        self.UpdateImages()

    def UpdateImages(self):
        self.histoDisp.SetImageData(self.imageDisp.GetCurrentData())
        self.histoDisp.UpdateHist()
        
    def CheckAll(self):
        if self.Histo_All_Check.isChecked():
            self.histoDisp.DisplayAll()
            self.UpdateImages()
    def CheckR(self):
        if self.Histo_R_Check.isChecked():
            self.histoDisp.DisplayOnlyR()
            self.UpdateImages()
    def CheckG(self):
        if self.Histo_G_Check.isChecked():
            self.histoDisp.DisplayOnlyG()
            self.UpdateImages()
    def CheckB(self):
        if self.Histo_B_Check.isChecked():
            self.histoDisp.DisplayOnlyB()
            self.UpdateImages()
    def CheckL(self):
        if self.Histo_L_Check.isChecked():
            self.histoDisp.DisplayOnlyL()
            self.UpdateImages()



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