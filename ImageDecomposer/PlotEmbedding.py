
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
from LumetriVector import Lumetri 
#from Boxplot import boxplotDisplay

_DEBUGGING = False


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.enableLutComparison = False 

        self.imageDisp = ImageDisplay()
        self.histoDisp = HistoDisplay()
        self.lumetri = Lumetri()
        self.cc_rgb = ColorCube('rgb')
        self.cc_hsv = ColorCube('hsv')
        self.ax_rgb = None 

        #self.displayGradient()

        self.updateArrow()

        # Feed image data to all modules 
        self.histoDisp.SetImageData(self.imageDisp.GetCurrentData())
        self.cc_hsv.SetImageData(self.imageDisp.GetCurrentData())
        self.cc_rgb.SetImageData(self.imageDisp.GetCurrentData())
        self.lumetri.SetImageData(self.imageDisp.GetCurrentData())
        self.lumetri.UpdateLumetri()
        

        # Connect interactive buttons 
        self.ArrowButton.clicked.connect(self.toggleArrow)
        self.GrayCardButton.clicked.connect(self.displayGrayCard)
        self.GradientButton.clicked.connect(self.displayGradient)

        self.LUTSlider.valueChanged.connect(self.updateSlider)

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
        #canvas_hist = FigureCanvas(ax_hist.figure)
        layoutHisto.addWidget(self.histoDisp)
        self.show()

        '''====================================================='''
        '''============= Lumetri Vector Display ================'''
        layoutLumetri = self.Lumetri_Area.layout()
        if layoutLumetri is None:
            layoutLumetri = QVBoxLayout(self.Lumetri_Area)
        ax_lumetri = self.histoDisp.UpdateHist()
        #canvas_lumetri = FigureCanvas(ax_lumetri.figure)
        layoutLumetri.addWidget(self.lumetri)
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


    def updateArrow(self):
        self.imageDisp.SetLutComparison(self.enableLutComparison)
        self.histoDisp.SetLutComparison(self.enableLutComparison)
        self.cc_hsv.SetLutComparison(self.enableLutComparison)
        self.cc_rgb.SetLutComparison(self.enableLutComparison)
        self.lumetri.SetLutComparison(self.enableLutComparison)
        self.lumetri.SetLutComparison(self.enableLutComparison)

    def toggleArrow(self):
        self.enableLutComparison = not self.enableLutComparison

        self.updateArrow()

        self.UpdateEntireImage()
        self.UpdatePartialImage()

    def updateSlider(self):
        if self.enableLutComparison:
            value = 1 + self.LUTSlider.value() / 10
            self.lumetri.SetLutScale(value)
            self.lumetri.UpdateLumetri()

    def displayGrayCard(self):
        self.imageDisp.displayGrayCard()
        self.UpdateEntireImage()
        self.UpdatePartialImage()

    def displayGradient(self):
        self.imageDisp.displayGradient()
        self.UpdateEntireImage()
        self.UpdatePartialImage()

    def UpdateEntireImage(self):
        '''
        Update method for when the image itself is altered. 
        '''
        self.imageDisp.UpdateImage()
        self.histoDisp.SetImageData(self.imageDisp.GetCurrentData())
        self.lumetri.SetImageData(self.imageDisp.GetCurrentData())
        self.lumetri.UpdateLumetri()
        


    def UpdatePartialImage(self):
        '''
        Update method for when the image is not changed, only selecting different channel. 
        '''
        self.histoDisp.SetImageData(self.imageDisp.GetCurrentData())
        self.histoDisp.UpdateHist()
        
    def CheckAll(self):
        if self.Histo_All_Check.isChecked():
            self.histoDisp.DisplayAll()
            #self.boxplotDisp.DisplayAll()
            self.UpdatePartialImage()


    def CheckR(self):
        if self.Histo_R_Check.isChecked():
            self.histoDisp.DisplayOnlyR()
            #self.boxplotDisp.DisplayOnlyR()
            self.UpdatePartialImage()

    def CheckG(self):
        if self.Histo_G_Check.isChecked():
            self.histoDisp.DisplayOnlyG()
            #self.boxplotDisp.DisplayOnlyG()
            self.UpdatePartialImage()

    def CheckB(self):
        if self.Histo_B_Check.isChecked():
            self.histoDisp.DisplayOnlyB()
            #self.boxplotDisp.DisplayOnlyB()
            self.UpdatePartialImage()

    def CheckL(self):
        if self.Histo_L_Check.isChecked():
            self.histoDisp.DisplayOnlyL()
            #self.boxplotDisp.DisplayOnlyL()
            self.UpdatePartialImage()



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
