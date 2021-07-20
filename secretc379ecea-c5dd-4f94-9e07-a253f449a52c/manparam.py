
import os 
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pywt
import matplotlib.colors as colors
import skimage as sk

from matplotlib import cm
from math import sqrt
from skimage.feature import blob_dog, blob_log, blob_doh

# Simple rowMultiplication used in pad 
rowMult= lambda Mat,theRow,xv,yv: Mat[theRow,0]*xv+Mat[theRow,1]*yv+Mat[theRow,2]

def gridBorders(theSums,perc):
  percen=np.percentile(theSums,perc)
  matchingX=np.arange(0,len(theSums))[theSums<percen]
  arr=np.array(matchingX[0])
  for i in np.arange(1,len(matchingX)):
    if matchingX[i]-matchingX[i-1]!=1:
      arr=np.append(arr,[matchingX[i-1],matchingX[i]])
  arr=np.append(arr,matchingX[i])
  return(arr)



numPads=123 # got this from counting peaks in a subArea. image 488
interpad=5  # got this from measuring between peaks in a subArea. image 488
min_sigma=1
max_sigma=3
threshFac=0.1
# TL,TR,BR,BL
# manually selected from FC3344_LOBE_LANEA_0--Stage20--488 image. The points were created by clicking on pad centres so the grid is widened by interpad.
patches={
"Patch 1":np.array([[461-interpad,621-interpad],[1082+interpad,625-interpad],[1077+interpad,1246+interpad],[457-interpad,1241+interpad]],np.int32),
"Patch 2":np.array([[1150-interpad,626-interpad],[1771+interpad,630-interpad],[1767+interpad,1252+interpad],[1145-interpad,1246+interpad]],np.int32),
"Patch 3":np.array([[456-interpad,1310-interpad],[1077+interpad,1314-interpad],[1072+interpad,1935+interpad],[450-interpad,1932+interpad]],np.int32),
"Patch 4":np.array([[1145-interpad,1315-interpad],[1766+interpad,1319-interpad],[1763+interpad,1942+interpad],[1141-interpad,1936+interpad]],np.int32)
}
