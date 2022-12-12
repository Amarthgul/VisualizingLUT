# Visualizing LUT

Give LUTs a visible profile. 

<p align="center">
	<img src="https://github.com/Amarthgul/VisualizingLUT/blob/main/ImageDecomposer/Images/Resources/vScCf8g.png">
</p>

------------------------------------------

## ImageDecomposer

UI: 

* `UI_MainWindow.ui`

  This file is created and modified in QT Designer. 

* `UI_MainWindow.py`

  PyQt5 GUI translated from `UI_MainWindow.ui`

Plot Classes: 

* HistoDisplay

  Containing both the histogram and box graph. 

  When `All` is selected, all 4 channels will be sidplayed. 

  When a single channel is selected, the channel shall be isolated, with a box plot
  on top, showing the median and deviance. 

* ColorCube

  Display RGB and HSV color cube. Currently they can be rotated around but cannot be updated.  

* Lumetri

  RadViz graph based on the RGB value of the pixels. 

  This shows which hue the pixel is closer to. 

* ~~boxplotDisplay~~

  This class has been merged into HistoDisplay for faster computation 


# Logs 

* 4th Dec (Evelyn & Amarth)

  Added boxgraph, histogram, and lumetri

* 29th Nov (Amarth)
  
  Split decomposer into serveral files and added the color cube plotter.

  RGB to HSV: https://www.rapidtables.com/convert/color/rgb-to-hsv.html 

* 25th Nov (Amarth)

  Added a graphic user interface. 

  The GUI is created using QT Designer, interfaced with Python following 
  this [toturial](https://www.pythonguis.com/tutorials/first-steps-qt-creator/). 
  Simply enter `pyuic5 UI_MainWindow.ui -o UI_MainWindow.py` after updating the `.ui`
  to generate the py file. 
