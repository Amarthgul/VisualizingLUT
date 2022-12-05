
import PIL.Image as img
import os, os.path

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import image


class Lumetri(FigureCanvas):
    '''
    This class is for the lumetri vector.
    Lumetri vector is a RadViz graph, and in this case the axis are R, G, and B. 
    '''
    def __init__(self, parent=None, width=1, height=1, dpi=100):

        self.imageData = None
        self.pixelLimit = 20000
        self.colorDepth = 255 
        self.radius = 1
        self.showCircle = False 
        self.pointRGB = np.array([
                [0, self.radius],
                [-(np.sqrt(3) / 2)*self.radius, -0.5],
                [ (np.sqrt(3) / 2)*self.radius, -0.5],
                [-(np.sqrt(3) / 2)*self.radius,  0.5], #Yellow 
                [0, -self.radius], # Cyan
                [(np.sqrt(3) / 2)*self.radius,   0.5] # Megenta
            ])
        self.pointColorRGB = np.array([
                '#ff0000', '#00ff00', '#0000ff',
                '#ffff00', '#ff00ff', '#00ffff'
            ])
        self.pixelPointSize = .4
        self.backgroundColor = (.2, .2, .2, .1)
        
        self.fig = Figure(figsize=(width, height))
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.clear()
        self.axes.axis('off')

        if __name__ == "__main__":
            self._readSampleImage()
        else: 
            plt.draw()

        super(Lumetri, self).__init__(self.fig)

    def _readSampleImage(self):
        imgPath = './/Images//Baseline//baseline_09.jpg'
        im = img.open(imgPath).convert("RGB")
        self.SetImageData(np.asarray(im))

    def SetImageData(self, data):
        self.imageData = data

    def CalculatedRadViz(self, ImageData):
        '''
        Given image data in RGB array, calculates the corresponding 2D locations
        on the RadViz plot. 
        '''
        imageWidth = ImageData.shape[0]
        imageHeight = ImageData.shape[1]
        totalPixel = imageWidth * imageHeight
        pixelColors = ImageData.reshape(totalPixel, 3)

        pixelColors = np.array(pixelColors, dtype = 'float')
        # Regulate color, reduce 8 bits to 0-1
        if np.max(pixelColors) > 1: 
            pixelColors /= self.colorDepth

        # Regulate data size
        if totalPixel > self.pixelLimit:
            selectIndex = np.random.choice(np.arange(totalPixel), self.pixelLimit, 
                                           replace=False) 
            totalPixel = self.pixelLimit 
            pixelColors = pixelColors[selectIndex, :]

        # Calculate the 2D points 
        dataPoints = np.zeros((totalPixel, 2))
        dataPoints += np.matmul(np.transpose(np.array([pixelColors[:, 0]])), 
                                    np.array([self.pointRGB[0]]))
        dataPoints += np.matmul(np.transpose(np.array([pixelColors[:, 1]])), 
                                    np.array([self.pointRGB[1]]))
        dataPoints += np.matmul(np.transpose(np.array([pixelColors[:, 2]])), 
                                    np.array([self.pointRGB[2]]))
        
        return (pixelColors, dataPoints)

    def UpdateLumetri(self):
        self.axes.clear()
        self.axes.axis('off')
        
        (pixelColors, dataPoints) = self.CalculatedRadViz(self.imageData)

        if self.showCircle:
            circle1 = plt.Circle((0, 0), self.radius, 
                             color = self.backgroundColor, 
                             linewidth=0, zorder=0 )
            self.axes.add_patch(circle1)

        # The RGB dots 
        self.axes.scatter(self.pointRGB[:, 0], self.pointRGB[:, 1], c = self.pointColorRGB, 
                   zorder=1)
        # image pixel dots 
        self.axes.scatter(dataPoints[:, 0], dataPoints[:, 1], 
                   c = pixelColors, s = self.pixelPointSize, 
                   zorder=1)

        plt.xlim(-1.02, 1.02)
        plt.ylim(-1.02, 1.02)

        

        if __name__ == '__main__':
            plt.show()
        else:
            self.draw()

