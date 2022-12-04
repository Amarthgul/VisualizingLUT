# Visualizing LUT

Give LUTs a visible profile. 

------------------------------------------

## ImageDecomposer

Python project for reading and outputing images as data sheets 

* Images 

  Folder of several sequences which shall be read and converted into data sheets.
  
  RGB array `(R_VLAUE, G_VALUE, B_VALUE)`
  
  RGBL array `(R_VLAUE, G_VALUE, B_VALUE, Brightness)`
  
  R channel distribution (0-255): `(0, 3), (1, 10), ..., (255, 0)`

* ImageDecomposer.py
  
  Main program 

  (This is not the case during development, currently the `PlotEmbedding.py` is where
  the plots are being drawn)

* UI_MainWindow.py

  The GUI translated from `UI_MainWindow.ui`. The `.ui` file is made can can be edited with QT Designer.

* PlotEmbedding.py

  Display the PyQt UI and with plot embeddings 



## Visualization.html

The main file for making and displaying the anaylsis 

# Logs 

* 29th Nov (Amarth)
  
  Split decomposer into serveral files and added the color cube plotter.

  RGB to HSV: https://www.rapidtables.com/convert/color/rgb-to-hsv.html 

* 25th Nov (Amarth)

  Added a graphic user interface. 

  The GUI is created using QT Designer, interfaced with Python following 
  this [toturial](https://www.pythonguis.com/tutorials/first-steps-qt-creator/). 
  Simply enter `pyuic5 UI_MainWindow.ui -o UI_MainWindow.py` after updating the `.ui`
  to generate the py file. 
