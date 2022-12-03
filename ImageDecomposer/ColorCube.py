import colorsys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ColorCube(FigureCanvas):
    def __init__(self):
        self.mode = 'rgb'
        self.plotSize = 1
        self.step = 8
        self.pointSize = 240
        self.pointOpacity = 0.25
        self.fontSize = 15 
        self.showLegend = False 
        self.useBlackBackground = False 

        fig = Figure()
        self.fig = fig
        self.axes = fig.add_subplot(111, projection='3d')

    def ShowPlot(self):
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111, projection='3d')

        # First remove fill
        self.axes.w_xaxis.set_pane_color((.0, .0, .0, 1.0))
        self.axes.w_yaxis.set_pane_color((.0, .0, .0, 1.0))
        self.axes.w_zaxis.set_pane_color((.0, .0, .0, 1.0))
        self.axes.axis('off')
        if self.useBlackBackground:
            self.axes.set_facecolor("black")

        def midpoints(x):
            sl = ()
            for i in range(x.ndim):
                x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
                sl += np.index_exp[:]
            return x

        start = 0;
        end = 255;
        if self.mode is 'rgb':
            spatialAxes = [self.step, self.step, self.step]
            r, g, b= np.indices((self.step+1, self.step+1, self.step+1)) / 16.0
            rc = midpoints(r)
            gc = midpoints(g)
            bc = midpoints(b)
            cube = np.ones(spatialAxes, dtype=np.bool)
            # combine the color components
            colors = np.zeros(cube.shape + (4,))
            colors[..., 0] = rc
            colors[..., 1] = gc
            colors[..., 2] = bc
            colors[..., 3] = 0.2
            self.axes.voxels(r, g, b, cube,
                  facecolors = colors, 
                  linewidth = 0)

            if self.showLegend:
                self.axes.set_xlabel('$Red$', fontsize = self.fontSize)    
                self.axes.set_ylabel('$Green$', fontsize = self.fontSize)    
                self.axes.set_zlabel('$Blue$', fontsize = self.fontSize) 

        elif self.mode is 'hsv':
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
                                          alpha = self.pointOpacity)
            if self.showLegend:
                self.axes.set_xlabel('$Hue$', fontsize = self.fontSize)    
                self.axes.set_ylabel('$Saturation$', fontsize = self.fontSize)    
                self.axes.set_zlabel('$Value$', fontsize = self.fontSize)

        if __name__ == "__main__":
            plt.show()

        return self.axes



def main():
    CC = ColorCube()
    CC.ShowPlot()


if __name__ == "__main__":
    main() 



'''
    Unused code 

            for zValue in np.linspace(start, end, self.step):
                for xValue in np.linspace(start, end, self.step):
                    for yValue in np.linspace(start, end, self.step):
                        color = '#%02x%02x%02x' % (int(xValue), int(yValue), int(zValue));
                        self.axes.scatter(xValue, yValue, zValue, 
                                          c = color, 
                                          s = self.pointSize, 
                                          alpha = self.pointOpacity)
'''