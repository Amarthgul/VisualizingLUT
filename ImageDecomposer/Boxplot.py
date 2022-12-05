
import PIL.Image as img
import os, os.path

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import image



import PyQt5.QtWidgets as QtWidgets


class boxplotDisplay(FigureCanvas):
    '''
    This class is for displaying the Boxplot.
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
        self.axes.clear()
        self.axes.axis('off')

        if __name__ == "__main__":
            self._readSampleImage()
        else:
            plt.draw()

        super(boxplotDisplay, self).__init__(self.fig)

    def _readSampleImage(self):
        imgPath = './/Images//Baseline//baseline_09.jpg'
        im = img.open(imgPath).convert("RGB")
        self.SetImageData(np.asarray(im))

    def SetImageData(self, data):
        self.imageData = data
        self.R = self.imageData[..., 0]
        self.G = self.imageData[..., 1]
        self.B = self.imageData[..., 2]
        self.L = self.imageData[..., 0]  # TODO: find a way to implement this L channel
        self.channels = [self.R, self.G, self.B, self.L]


    def DisplayAll(self):
        '''
        This method changes the display flag, marking all the channels .
        '''
        self.channelFlags = [False, False, False, False]

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

    def UpdateBoxplot(self):
        '''
        Updates the boxplot.
        Iterate through channels, plot the channels that has been marked true for display.
        '''

        self.axes.clear()
        self.axes.axis('off')
        n = 0
        for i in range(self.channelCount):
            if self.channelFlags[i]:
                self.axes.boxplot(self.channels[i].ravel(),
                                  vert=False,
                                  boxprops=dict(color=self.channelColors[i]),
                                  capprops=dict(color=self.channelColors[i]),
                                  whiskerprops=dict(color=self.channelColors[i]),
                                  medianprops=dict(color=self.channelColors[i]),
                                  flierprops={'marker': '.', 'markersize': 0.5})
            else:
                n += 1

        if n == 4:
            self.axes = self.axes.boxplot([self.channels[0].ravel(),
                                           self.channels[1].ravel(),
                                           self.channels[2].ravel(),
                                           self.channels[3].ravel()],
                                          vert=False,
                                          flierprops={'marker': '.', 'markersize': 0.5})
            self.axes['medians'][0].set(color=self.channelColors[0])
            self.axes['medians'][1].set(color=self.channelColors[1])
            self.axes['medians'][2].set(color=self.channelColors[2])
            self.axes['medians'][3].set(color=self.channelColors[3])
            self.axes['boxes'][0].set(color=self.channelColors[0])
            self.axes['boxes'][1].set(color=self.channelColors[1])
            self.axes['boxes'][2].set(color=self.channelColors[2])
            self.axes['boxes'][3].set(color=self.channelColors[3])
        else:
            n = 0


        if __name__ == '__main__':
            plt.show()
        else:
            self.draw()

        return self.axes


if __name__ == '__main__':
    box = boxplotDisplay()
    box.UpdateBoxplot()
