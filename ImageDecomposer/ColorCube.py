import colorsys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ColorCube(FigureCanvas):
    def __init__(self, mode='rgb'):
        self.mode = mode
        self.plotSize = 1
        self.step = 8
        
        self.gridOpacity = 0.15
        self.fontSize = 15 
        self.showLegend = False 
        self.useBlackBackground = False 
        self.pixelLimit = 1000
        self.colorDepth = 255
        self.pixelPointSize = 2
        self.imageData = None 
        self.pixelPos = []      # When RGB is used, self.pixelPos is the same as self.pixelColor
        self.pixelColor = [] 

        self.spatialAxes = [self.step, self.step, self.step]
        self.R = []
        self.G = []
        self.B = []
        self.cube = np.ones(self.spatialAxes, dtype=np.bool)
        self.RGBColor = []
        self.HSVColor = []

        self.lutComparison = False 

        self.initData()

        self.fig = Figure(figsize=(self.plotSize, self.plotSize))
        self.fig.clear()
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes.clear()
        self.axes.axis('off')
        self.ShowPlot()
        plt.draw()

        super(ColorCube, self).__init__(self.fig)

    def midpoints(self, x):
        sl = ()
        for i in range(x.ndim):
            x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
            sl += np.index_exp[:]
        return x

    def initData(self):
        '''
        Initilize data that will be repetitively used for the display of the cube. 
        '''
        spatialAxes = [self.step, self.step, self.step]
        self.R, self.G, self.B = np.indices((self.step+1, self.step+1, self.step+1)) / self.step
        rc = self.midpoints(self.R)
        gc = self.midpoints(self.G)
        bc = self.midpoints(self.B)
        # combine the color components
        self.RGBColor = np.zeros(self.cube.shape + (4,))
        self.RGBColor[..., 0] = rc
        self.RGBColor[..., 1] = gc
        self.RGBColor[..., 2] = bc
        self.RGBColor[..., 3] = self.gridOpacity

        colors3 = np.zeros(self.cube.shape + (3,))
        colors3[..., 0] = rc
        colors3[..., 1] = gc
        colors3[..., 2] = bc
        colors3 = matplotlib.colors.hsv_to_rgb(colors3)
        self.HSVColor = np.zeros(self.cube.shape + (4, ))
        self.HSVColor[..., 0] = colors3[..., 0]
        self.HSVColor[..., 1] = colors3[..., 1]
        self.HSVColor[..., 2] = colors3[..., 2]
        self.HSVColor[..., 3] = self.gridOpacity


    def SetImageData(self, data):
        self.imageData = data[0]
        self.ProcessImageData()

    def SetLutComparison(self, boolFlag):
        self.lutComparison = boolFlag 

    def ProcessImageData(self):
        imageWidth = self.imageData.shape[0]
        imageHeight = self.imageData.shape[1]
        totalPixel = imageWidth * imageHeight
        pixelColors = self.imageData.reshape(totalPixel, 3)

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

        self.pixelColor = pixelColors
        if self.mode == 'rgb':
            self.pixelPos = pixelColors
        elif self.mode == 'hsv':
            self.pixelPos =  matplotlib.colors.rgb_to_hsv(pixelColors)

    def UpdatePlot(self, axes):
        axes.clear()
        axes.axis('off')

        if self.mode == 'rgb':
            axes.voxels(self.R, self.G, self.B, self.cube,
                  facecolors=self.RGBColor,
                  linewidth=0)

        elif self.mode == 'hsv':
            axes.voxels(self.R, self.G, self.B, self.cube,
                  facecolors = self.HSVColor, 
                  linewidth = 0)

        if len(self.pixelColor) > 1:
            axes.scatter(self.pixelColor[:, 0], 
                                self.pixelColor[:, 1], 
                                self.pixelColor[:, 2], 
                                c = self.pixelColor, marker='o')

    def ShowPlot(self):
        '''
        Display the plot. If called externally, return the ax object. 
        '''
        self.axes.clear()
        self.axes.axis('off')

        if __name__ == "__main__":
            self.plotSize = 6 

        self.fig = Figure(figsize=(self.plotSize, self.plotSize))
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes.clear()
        self.axes.axis('off')

        # First remove fill
        self.axes.w_xaxis.set_pane_color((.0, .0, .0, 1.0))
        self.axes.w_yaxis.set_pane_color((.0, .0, .0, 1.0))
        self.axes.w_zaxis.set_pane_color((.0, .0, .0, 1.0))
        self.axes.axis('off')
        if self.useBlackBackground:
            self.axes.set_facecolor("black")

        if self.mode == 'rgb':
            self.axes.voxels(self.R, self.G, self.B, self.cube,
                  facecolors=self.RGBColor,
                  linewidth=0)
            if self.showLegend:
                self.axes.set_xlabel('$Red$', fontsize=self.fontSize)
                self.axes.set_ylabel('$Green$', fontsize=self.fontSize)
                self.axes.set_zlabel('$Blue$', fontsize=self.fontSize)

        elif self.mode == 'hsv':
            self.axes.voxels(self.R, self.G, self.B, self.cube,
                  facecolors = self.HSVColor, 
                  linewidth = 0)
            if self.showLegend:
                self.axes.set_xlabel('$Hue$', fontsize=self.fontSize)
                self.axes.set_ylabel('$Saturation$', fontsize=self.fontSize)
                self.axes.set_zlabel('$Value$', fontsize=self.fontSize)

        if len(self.pixelColor) > 1:
            self.axes.scatter(self.pixelPos[:, 0], 
                                self.pixelPos[:, 1], 
                                self.pixelPos[:, 2], 
                                c = self.pixelColor, marker='o')

        if __name__ == "__main__":
            plt.show()

        return self.axes



if __name__ == "__main__":
    CC = ColorCube()
    CC.ShowPlot()



'''
    Unused code 
    self.pointSize = 240
            start = 0;
            end = 255;
            for zValue in np.linspace(start, end, self.step):
                for xValue in np.linspace(start, end, self.step):
                    for yValue in np.linspace(start, end, self.step):
                        color = '#%02x%02x%02x' % (int(xValue), int(yValue), int(zValue));
                        self.axes.scatter(xValue, yValue, zValue, 
                                          c = color, 
                                          s = self.pointSize, 
                                          alpha = self.gridOpacity)

            for hue in np.linspace(0, 360, self.step):
                for sat in np.linspace(0, 1, self.step):
                    for val in np.linspace(0, 1, self.step):
                        color = colorsys.hsv_to_rgb(hue / 360.0, sat, val)
                        color = '#%02x%02x%02x' % (int(color[0] * end), 
                                                   int(color[1]* end), 
                                                   int(color[2]* end));
                        self.axes.scatter(hue, sat, val, 
                                          c = color, 
                                          s = self.pointSize, 
                                          alpha = self.gridOpacity)
'''