
import PIL.Image as img
import os, os.path

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import PyQt5.QtWidgets as QtWidgets

class ImageDisplay(FigureCanvas):
    '''
    This class is for displaying the image, corresponds to the "Image_Area" in UI. 
    '''
    def __init__(self):
        self.validFormat = ['.jpg', '.JPG']
        self.baselinePath = './/Images//Baseline'
        self.imagePaths = []        # In format of ['//Image//Basline//imageXX.jpg', ...] 
        self.baselineImages = []    # An array of image data 
        self.baselineImageIndex = 0

        self.imageDisplaySize = 2

        self._readImagePaths()
        self._readBaselineImages()

        fig = Figure()
        self.fig = fig
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def _readImagePaths(self):
        for f in os.listdir(self.baselinePath):
            ext = os.path.splitext(f)[1]
            if ext.lower() in self.validFormat:
                self.imagePaths.append(os.path.join(self.baselinePath, f))
        print(self.imagePaths)

    def _readBaselineImages(self):
        for name, file in enumerate(self.imagePaths):
            im = img.open(file).convert("RGB")
            self.baselineImages.append(im)

    def nextImage(self):
        self.baselineImageIndex += 1
        self.UpdateImage()

    def lastImage(self):
        self.baselineImageIndex -= 1
        self.UpdateImage()

    def UpdateImage(self):
        #self.axes.cla()
        #self.axes.axis('off')
        self.axes.imshow(np.asarray(self.baselineImages[self.baselineImageIndex % len(self.baselineImages)]))
        
        return self.axes

    def displayImage(self, index = 0):
        self.fig = Figure(figsize = (self.imageDisplaySize, self.imageDisplaySize))
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')

        self.axes.imshow(np.asarray(self.baselineImages[self.baselineImageIndex % len(self.baselineImages)]))

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