
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

def ScaledImage(inImage,lower=0,upper=255,maxVal=255,invert=True):
    greyFac=maxVal/(upper-lower)
    img=np.clip(np.floor(greyFac*(inImage-lower)),0,maxVal)
    if invert:
      img=maxVal-img
    return(img)


def PercentileScaledImage(inImage,lowerPerc=0.1,upperPerc=99.9,maxVal=255,invert=True):
    lower,upper=np.percentile(inImage,(lowerPerc,upperPerc))
    return(ScaledImage(inImage,lower=lower,upper=upper,maxVal=maxVal,invert=invert))

def PercentileScaledImageToImage(inImage,scaleRef,lowerPerc=0.1,upperPerc=99.9,maxVal=255,invert=True):
    lower,upper=np.percentile(scaleRef,(lowerPerc,upperPerc))
    return(ScaledImage(inImage,lower=lower,upper=upper,maxVal=maxVal,invert=invert))

def SaveImageAndMarkdown(imagePath,theImage,descript):
  print("\n\n"+descript+"\n\n")
  ok=cv.imwrite(imagePath, theImage)
  print("\n\n![]("+imagePath+")\n\n")
  print("\n\nView full image ["+imagePath+"]("+imagePath+")\n\n")
 
def SavePlotAndMarkdown(imagePath,descript):
  print("\n\n"+descript+"\n\n")
  plt.savefig(imagePath);
  print("\n<center>\n![]("+imagePath+"){width=90%}\n</center>\n")
  print("\n\nView full image ["+imagePath+"]("+imagePath+")\n\n")
  
def CompareSurfaces(img1,desc1,img2,desc2,TL=(0,0),BR=(100,100)):
  subImage1 = img1[TL[1]:BR[1],TL[0]:BR[0]]
  subImage2 = img2[TL[1]:BR[1],TL[0]:BR[0]]
  plotMin=np.min((np.min(subImage1),np.min(subImage2)))
  plotMax=np.max((np.max(subImage1),np.max(subImage2)))
  
  # create the x and y coordinate arrays (here we just use pixel indices)
  xx, yy = np.mgrid[0:subImage1.shape[0], 0:subImage1.shape[1]]
  
  # set up a figure twice as wide as it is tall
  fig = plt.figure(figsize=plt.figaspect(0.5))
  
  #===============
  #  First subplot
  #===============
  # set up the axes for the first plot
  ax = fig.add_subplot(1, 2, 1, projection='3d')
  ax.set_title(desc1)
  surf = ax.plot_surface(xx, yy, subImage1, rstride=1, cstride=1, cmap=plt.cm.jet,
                       linewidth=0, antialiased=False)
  ax.set_zlim(plotMin, plotMax)
  #fig.colorbar(surf, shrink=0.5, aspect=10)

  #===============
  # Second subplot
  #===============
  # set up the axes for the second plot
  ax = fig.add_subplot(1, 2, 2, projection='3d')
  ax.set_title(desc2)
  
  surf = ax.plot_surface(xx, yy, subImage2, rstride=1, cstride=1, cmap=plt.cm.jet,
                       linewidth=0, antialiased=False)
  ax.set_zlim(plotMin, plotMax)
