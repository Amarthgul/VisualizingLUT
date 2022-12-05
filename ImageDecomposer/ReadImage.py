
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

class ImageDisplay(FigureCanvas):
    '''
    This class is for displaying the image, corresponds to the "Image_Area" in UI. 
    '''
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.validFormat = ['.jpg', '.JPG']
        self.baselinePath = './/Images//Baseline'
        self.grayCardPath = './/Images//graycard.jpg'
        self.gradientPath = './/Images//gradient.jpg'
        self.imagePaths = []        # In format of ['//Image//Basline//imageXX.jpg', ...] 
        self.baselineImages = []    # An array of image data 
        self.baselineImageIndex = 0
        self.grayCard = None
        self.gradient = None 
        self.displayingGrayCard = False 
        self.displayingGradient = False 

        self.imageDisplaySize = 2

        self._readImagePaths()
        self._readBaselineImages()
        self._readGs()

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.clear()
        self.axes.axis('off')
        plt.draw()

        super(ImageDisplay, self).__init__(self.fig)
        

    def _readImagePaths(self):
        for f in os.listdir(self.baselinePath):
            ext = os.path.splitext(f)[1]
            if ext.lower() in self.validFormat:
                self.imagePaths.append(os.path.join(self.baselinePath, f))

    def _readBaselineImages(self):
        for name, file in enumerate(self.imagePaths):
            im = img.open(file).convert("RGB")
            self.baselineImages.append(im)

    def _readGs(self):
        self.grayCard = img.open(self.grayCardPath).convert("RGB")
        self.gradient = img.open(self.gradientPath).convert("RGB")

    def GetCurrentData(self):
        if self.displayingGradient:
            return np.asarray(self.gradient)
        if self.displayingGrayCard:
            return np.asarray(self.grayCard)
        else:
            return np.asarray(self.baselineImages[self.baselineImageIndex])

    def nextImage(self):
        self.baselineImageIndex += 1
        if(self.baselineImageIndex == len(self.baselineImages)):
            self.baselineImageIndex = 0
        self.displayingGrayCard = False 
        self.displayingGradient = False
        self.UpdateImage()

    def lastImage(self):
        self.baselineImageIndex -= 1
        if(self.baselineImageIndex == -len(self.baselineImages)):
            self.baselineImageIndex = 0
        self.displayingGrayCard = False 
        self.displayingGradient = False
        self.UpdateImage()

    def displayGrayCard(self):
        self.axes.clear()
        self.axes.axis('off')
        self.axes.imshow(np.asarray(self.grayCard))
        self.displayingGrayCard = True 
        self.displayingGradient = False
        self.draw()

    def displayGradient(self):
        self.axes.clear()
        self.axes.axis('off')
        self.axes.imshow(np.asarray(self.gradient))
        self.displayingGradient = True
        self.displayingGrayCard = False 
        self.draw()

    def UpdateImage(self):
        self.axes.clear()
        self.axes.axis('off')
        self.axes.imshow(np.asarray(self.baselineImages[self.baselineImageIndex]))
        self.draw()

    def displayImage(self, index = 0):
        self.axes.clear()
        self.axes.axis('off')
        self.axes.imshow(np.asarray(self.baselineImages[self.baselineImageIndex]))
        self.draw()
        return self.axes




def openAndConvert(dirFileNames=[], filesNames=[], outDir = './/OutputImages//', targetFormat ="png"):
    '''Given the files, open them and convert to another format and then save'''

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for name, file in enumerate(dirFileNames):
        im = img.open(file).convert("RGB")
        noExtName = filesNames[name][:-4]
        print(filesNames[name][:-4])
        im.save(outDir + noExtName + '.' + targetFormat)


def getImages(path='.//Images//Baseline'):
    dirFileNames = []
    filesNames = []
    valid_images = [".jpg"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        dirFileNames.append(os.path.join(path, f))
        filesNames.append(f)

    return dirFileNames, filesNames

if __name__ == '__main__':
    dirFileNames, filesNames = getImages()
    openAndConvert(dirFileNames=dirFileNames, filesNames=filesNames)