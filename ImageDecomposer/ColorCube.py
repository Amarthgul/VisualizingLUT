import colorsys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ColorCube():
    

    def __init__(self):
        self.mode = 'rgb'
        self.plotSize = 6.5
        self.step = 8
        self.pointSize = 240
        self.pointOpacity = 0.5
        self.fontSize = 15 

    def ShowPlot(self):
        plt.figure(figsize = (self.plotSize, self.plotSize))
        ax3D = plt.axes([0.05, 0.05, 0.9, 0.9], projection = '3d')

        # First remove fill
        ax3D.w_xaxis.set_pane_color((.0, .0, .0, 1.0))
        ax3D.w_yaxis.set_pane_color((.0, .0, .0, 1.0))
        ax3D.w_zaxis.set_pane_color((.0, .0, .0, 1.0))

        if self.mode is 'rgb':
            start = 0;
            end = 255;

            for zValue in np.linspace(start, end, self.step):
                for xValue in np.linspace(start, end, self.step):
                    for yValue in np.linspace(start, end, self.step):
                        color = '#%02x%02x%02x' % (int(xValue), int(yValue), int(zValue));
                        ax3D.scatter(xValue, yValue, zValue, c = color, s = self.pointSize)
            ax3D.set_xlabel('$Red$', fontsize = self.fontSize)    
            ax3D.set_ylabel('$Green$', fontsize = self.fontSize)    
            ax3D.set_zlabel('$Blue$', fontsize = self.fontSize) 

        elif self.mode is 'hsv':
            for hue in np.linspace(0, 360, step):
                for sat in np.linspace(0, 1, step):
                    for val in np.linspace(0, 1, step):
                        color = cls.hsv_to_rgb([hue / 360.0, sat, val]).reshape(1,-1)
                        ax3D.scatter(hue, sat, val, c = color, s = self.pointSize)
            ax3D.set_xlabel('$Hue$', fontsize = self.fontSize)    
            ax3D.set_ylabel('$Saturation$', fontsize = self.fontSize)    
            ax3D.set_zlabel('$Value$', fontsize = self.fontSize)

        plt.show()



def main():
    CC = ColorCube()
    CC.ShowPlot()


if __name__ == "__main__":
    main() 
