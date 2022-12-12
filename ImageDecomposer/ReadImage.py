
import PIL.Image as img
from pillow_lut import load_cube_file
import os, os.path

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import image
from matplotlib import cm

import PyQt5.QtWidgets as QtWidgets


# LUTs downloaded from https://www.rocketstock.com/free-after-effects-templates/35-free-luts-for-color-grading-videos/

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
        self.baselineImageIndex = 21 # Change this for directly load certain image
        self.grayCard = None
        self.gradient = None 
        self.displayingGrayCard = False 
        self.displayingGradient = False 
        self.selectedImage = None 
        self.processedImage = None 

        self.imageDisplaySize = 2

        # Section for LUT
        self.lutFormat = '.cube'
        self.enableArrow = True 
        self.lutPath = './/Images//LUTs'
        self.lutPaths = []
        self.lutStrength = 0
        self.lutPivot = 0
        self.luts = []
        self.lutIndex = 0 
        

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

        self._applyLutByDegree()
        self.UpdateImage()
       

    def _readImagePaths(self):
        # Read image paths 
        for f in os.listdir(self.baselinePath):
            ext = os.path.splitext(f)[1]
            if ext.lower() in self.validFormat:
                self.imagePaths.append(os.path.join(self.baselinePath, f))

        # Read lut paths 
        for f in os.listdir(self.lutPath):
            ext = os.path.splitext(f)[1]
            if ext.lower() in self.lutFormat:
                self.lutPaths.append(os.path.join(self.lutPath, f))


    def _readBaselineImages(self):
        # Read image data
        for name, file in enumerate(self.imagePaths):
            im = img.open(file).convert("RGB")
            self.baselineImages.append(im)  
        self.selectedImage = self.baselineImages[self.baselineImageIndex]

        # Read LUT data 
        for name, file in enumerate(self.lutPaths):
            lut = load_cube_file(file)
            self.luts.append(lut)


    def _readGs(self):
        self.grayCard = img.open(self.grayCardPath).convert("RGB")
        self.gradient = img.open(self.gradientPath).convert("RGB")


    def _applyLutByDegree(self):
        selectedLut = self.luts[self.lutIndex]
        fullApply = self.selectedImage.filter(selectedLut)
        # Apply partial lut using numpy 
        self.processedImage = np.asarray(fullApply) * self.lutStrength + \
            np.asarray(self.selectedImage)* (1 - self.lutStrength)
        # Convert back to image 
        self.processedImage = img.fromarray(np.uint8(self.processedImage)).convert('RGB')

    def SetLutComparison(self, boolFlag):
        self.enableArrow = boolFlag 
        if (self.enableArrow):
            self._applyLutByDegree()
        self.UpdateImage()

    def GetCurrentData(self):
        if self.enableArrow:
            self._applyLutByDegree()
            return [np.asarray(self.processedImage), np.asarray(self.selectedImage)]
        else:
            return [np.asarray(self.selectedImage), None]

    def nextImage(self):
        self.baselineImageIndex += 1
        if(self.baselineImageIndex == len(self.baselineImages)):
            self.baselineImageIndex = 0
        self.displayingGrayCard = False 
        self.displayingGradient = False
        self.selectedImage = self.baselineImages[self.baselineImageIndex]

        self.UpdateImage()

    def lastImage(self):
        self.baselineImageIndex -= 1
        if(self.baselineImageIndex == -len(self.baselineImages)):
            self.baselineImageIndex = 0
        self.displayingGrayCard = False 
        self.displayingGradient = False
        self.selectedImage = self.baselineImages[self.baselineImageIndex]

        self.UpdateImage()

    def displayGrayCard(self):
        self.axes.clear()
        self.axes.axis('off')

        self.selectedImage = self.grayCard
        self.axes.imshow(np.asarray(self.selectedImage))
        self.displayingGrayCard = True 
        self.displayingGradient = False

        self.draw()

    def displayGradient(self):
        self.axes.clear()
        self.axes.axis('off')

        self.selectedImage = self.gradient
        self.axes.imshow(np.asarray(self.selectedImage))
        self.displayingGradient = True
        self.displayingGrayCard = False 

        self.draw()

    def UpdateImage(self):
        self.axes.clear()
        self.axes.axis('off')


        if (self.enableArrow):
            self.axes.imshow(np.asarray(self.processedImage))
        else:
            self.axes.imshow(np.asarray(self.selectedImage))
        self.draw()


    def displayImage(self):

        self.UpdateImage()
        
        return self.axes




#def openAndConvert(dirFileNames=[], filesNames=[], outDir = './/OutputImages//', targetFormat ="png"):
#    '''Given the files, open them and convert to another format and then save'''
#    if not os.path.exists(outDir):
#        os.makedirs(outDir)
#    for name, file in enumerate(dirFileNames):
#        im = img.open(file).convert("RGB")
#        noExtName = filesNames[name][:-4]
#        print(filesNames[name][:-4])
#        im.save(outDir + noExtName + '.' + targetFormat)
#def getImages(path='.//Images//Baseline'):
#    dirFileNames = []
#    filesNames = []
#    valid_images = [".jpg"]
#    for f in os.listdir(path):
#        ext = os.path.splitext(f)[1]
#        if ext.lower() not in valid_images:
#            continue
#        dirFileNames.append(os.path.join(path, f))
#        filesNames.append(f)
#    return dirFileNames, filesNames
#if __name__ == '__main__':
#    dirFileNames, filesNames = getImages()
#    openAndConvert(dirFileNames=dirFileNames, filesNames=filesNames)