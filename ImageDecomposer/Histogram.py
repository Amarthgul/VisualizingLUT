

import PIL.Image as img
import os, os.path

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import image
import colorsys

import PyQt5.QtWidgets as QtWidgets


class HistoDisplay(FigureCanvas):
    '''
    This class is for displaying the histogram. 
    '''
    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.imageData = None
        self.R = None
        self.G = None
        self.B = None
        self.L = None

        self.channelCount = 4
        self.channels = []
        self.channelFlags = [True, True, True, True]
        self.opacity = .25  
        self.channelColors = [(1, 0, 0, self.opacity),  # R
                              (0, 1, 0, self.opacity),  # G
                              (0, 0, 1, self.opacity),  # B
                              (0, 0, 0, self.opacity)]  # To be decided 
        
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.fig, self.axes = plt.subplots(
            2, figsize=(width, height), sharex = True,
            gridspec_kw={"height_ratios": (.15, .85)}  
        )
        self.axes[0].clear()
        self.axes[0].axis('off')
        self.axes[1].clear()
        self.axes[1].axis('off')

        self.lutComparison = False 

        if __name__ == "__main__":
            self._readSampleImage()
        else: 
            plt.draw()

        super(HistoDisplay, self).__init__(self.fig)

    def _readSampleImage(self):
        imgPath = './/Images//Baseline//baseline_09.jpg'
        im = img.open(imgPath).convert("RGB")
        self.SetImageData(np.asarray(im))

    def _calculateL(self, R, G, B):
        '''
        This one uses the definition of Y in YCbCr
        '''
        return 16.0 + (65.738 / 256) * R +\
            (129.057 / 256) * G +\
            (25.064 / 256) * B

    def SetImageData(self, data):
        self.imageData = data[0]
        self.R = self.imageData[..., 0]
        self.G = self.imageData[..., 1]
        self.B = self.imageData[..., 2]
        self.L = self._calculateL(self.R, self.G, self.B) 
        self.channels = [self.R, self.G, self.B, self.L]

    def SetLutComparison(self, boolFlag):
        self.lutComparison = boolFlag 


    def DisplayAll(self):
        '''
        This method changes the display flag, marking all the channels . 
        '''
        self.channelFlags = [True, True, True, True]

    def DisplayOnlyR(self):
        '''
        This method changes the display flag, marking only the Red channel. 
        '''
        self.channelFlags = [True, False, False, False]

    def DisplayOnlyG(self):
        '''
        This method changes the display flag, marking only the Green channel. 
        '''
        self.channelFlags = [False, True, False, False]

    def DisplayOnlyB(self):
        '''
        This method changes the display flag, marking only the Blue channel. 
        '''
        self.channelFlags = [False, False, True, False]

    def DisplayOnlyL(self):
        '''
        This method changes the display flag, marking only the L channel. 
        '''
        self.channelFlags = [False, False, False, True]


    def UpdateHist(self):
        '''
        Updates the histogram.
        Iterate through channels, plot the channels that has been marked true for display. 
        '''

        # Histogram 
        self.axes[0].clear()
        self.axes[0].axis('off')
        self.axes[1].clear()
        self.axes[1].axis('off')

        for i in range(self.channelCount):
            if self.channelFlags[i]:
                self.axes[1].hist(self.channels[i].ravel(), 
                               bins=256,
                               fc=self.channelColors[i])

        if False in self.channelFlags: # Not diaplying the 4 channels all together 
            for i in range(self.channelCount):
                if self.channelFlags[i]:
                    self.axes[0].boxplot(self.channels[i].ravel(),
                                      vert = False, sym = '', 
                                      widths = (.6))

        if __name__ == '__main__':
            plt.show()
        else:
            self.draw()

        return self.axes
        

if __name__ == '__main__':
    hist = HistoDisplay()
    hist.UpdateHist()
