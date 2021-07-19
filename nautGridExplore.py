import numpy as np
import matplotlib.pyplot as plt

import pywt
import pywt.data


# Load image
original = pywt.data.camera()

# Wavelet transform of image, and plot approximation and details
titles = ['Approximation', ' Horizontal detail',
          'Vertical detail', 'Diagonal detail']
coeffs2 = pywt.dwt2(original, 'bior1.3')
LL, (LH, HL, HH) = coeffs2
fig = plt.figure(figsize=(12, 3))
for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
origimg = cv.imread('C:/Users/david bramwell/Downloads/images/FC3344_LOBE_LANEA_0--Stage20--488.tif',cv.IMREAD_ANYDEPTH )

img = cv.bitwise_not(img)
flatImg = img.flatten()
uniqVals = np.unique(flatImg,return_counts=True)

lower,upper=np.percentile(origimg,(0.1,99.9))
greyFac=255/(upper-lower)
fimg=
img=255-np.uint8(np.clip(np.floor(greyFac*(origimg-lower)),0,255))

hist,bins = np.histogram(img.flatten(),256)
cdf = hist.cumsum()
cdf_normalized = cdf * float(hist.max()) / cdf.max()
plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256, color = 'r')
#plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()

equ = cv.equalizeHist(img)
cv.imshow('img',img)
cv.imshow('equ',equ)

clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)
cv.imshow('cl1',cl1)


ksize = 7
sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8
retval = cv.getGaussianKernel(7,sigma,cv.CV_32F)

colClahe=cv.cvtColor(cl1,cv.COLOR_GRAY2RGB)
# TL,TR,BR,BL

cropRect= np.array([[450,611],[1091,611],[1091,1257],[450,1257]],np.int32)

cropClahe=colClahe[450:1091,611:1257]
res = cv.resize(cropClahe,None,fx=2, fy=2, interpolation = cv.INTER_NEAREST)
cv.imshow('res',res)

estimatedRectSide=625
estimatedRectSide=estimatedRectSide*10

ptsRef=np.array([[0,0],[estimatedRectSide,0],[estimatedRectSide,estimatedRectSide],[0,estimatedRectSide]],np.int32)

pts=np.array([[461,621],[1081,625],[1077,1246],[457,1241]],np.int32)
M = cv.getAffineTransform(np.float32(pts[1:4]),np.float32(ptsRef[1:4]))

dst = cv.warpAffine(colClahe,M,(estimatedRectSide,estimatedRectSide))
numPads=123
sep=estimatedRectSide/numPads
for x in range(0,numPads):
 cv.circle(dst,(10+np.int32( np.floor(x*sep) ),60),3,(0,0,65535),1)

cv.imshow('dst',dst)
  

pts = pts.reshape((-1,1,2))
cv.polylines(colClahe,[pts],True,(0,65535,65535))
cropClahe=colClahe[611:1257,450:1091]

scaleFac=8
interpad=5
xoffset=(12*scaleFac)+scaleFac//2
yoffset=((10+interpad*5)*scaleFac)+scaleFac//2
res = cv.resize(cropClahe,None,fx=scaleFac, fy=scaleFac, interpolation = cv.INTER_NEAREST)
numPads=123

estimatedRectSide=625*scaleFac
sep=estimatedRectSide/numPads
for x in range(0,numPads):
 cv.circle(res,(xoffset+np.int32( np.floor(x*sep) ),yoffset),3,(0,0,65535),1)

cv.imshow('res',res)

461,466,471,476,481,486,






















import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def rowMult(Mat,theRow,xv,yv):
    return(Mat[theRow,0]*xv+Mat[theRow,1]*yv+Mat[theRow,2])

def gridBorders(theSums,perc):
  percen=np.percentile(theSums,perc)
  matchingX=np.arange(0,len(theSums))[theSums<percen]
  arr=np.array(matchingX[0])
  for i in np.arange(1,len(matchingX)):
    if matchingX[i]-matchingX[i-1]!=1:
      arr=np.append(arr,[matchingX[i-1],matchingX[i]])
  arr=np.append(arr,matchingX[i])
  return(arr)

scaleFac=4 # how much the subAreas are zoomed 
numPads=123 # got this from counting peaks in a subArea. image 488
interpad=5  # got this from measuring between peaks in a subArea. image 488


folderStub="procimage/"
fileStub="im488"

imageFile='C:/Users/david bramwell/Downloads/images/FC3344_LOBE_LANEA_0--Stage20--488.tif'

#fileStub="im647"
#imageFile='C:/Users/david bramwell/Downloads/images/FC3344_LOBE_LANEA_0--Stage20--647.tif'

# TL,TR,BR,BL
# manually selected from 488 image
patches={"Patch 1":np.array([[461,621],[1082,625],[1077,1246],[457,1241]],np.int32),
"Patch 2":np.array([[1150,626],[1771,630],[1767,1252],[1145,1246]],np.int32),
"Patch 3":np.array([[456,1310],[1077,1314],[1072,1935],[450,1932]],np.int32),
"Patch 4":np.array([[1145,1315],[1766,1319],[1763,1942],[1141,1936]],np.int32)
}

# should not need to change anything below here
e1 = cv.getTickCount()
origimg = cv.imread(imageFile,cv.IMREAD_ANYDEPTH )

# invert and contrast stretch an image for display
lower,upper=np.percentile(origimg,(0.1,99.9))
greyFac=255/(upper-lower)
img=255-np.uint8(np.clip(np.floor(greyFac*(origimg-lower)),0,255))

# create a version to draw on
colimg=cv.cvtColor(img,cv.COLOR_GRAY2RGB)

# take a guess where the inter subarray regions are based on grey level values
threshPerc=8
colSums= origimg.sum(axis=0)
rowSums= origimg.sum(axis=1)
percen=np.percentile(colSums,(9,10,20,30,40,50,60,70,80))
arrX=gridBorders(colSums,threshPerc)
arrY=gridBorders(rowSums,threshPerc)

if False:
  plt.ioff()
  plt.plot(np.arange(0,len(colSums)),colSums)
  plt.plot(np.arange(0,len(rowSums)),rowSums)
  plt.vlines(arrX,0,percen[8])
  plt.vlines(arrY,0,percen[8])
  plt.hlines(percen,0,len(colSums))
  plt.show()
  plt.close()


for i in np.arange(0,len(arrX),2):
  colimg=cv.rectangle(colimg,(arrX[i],0),(arrX[i+1],colimg.shape[1]),(65535,65535,0),1)
  
for i in np.arange(0,len(arrY),2):
  colimg=cv.rectangle(colimg,(0,arrY[i]),(colimg.shape[0],arrY[i+1]),(65535,65535,0),1)

#cv.imshow('colimg',colimg)

for patchName in patches:
    print(patchName)
    pts=patches[patchName]
    
    cropPad=interpad*3
    xcrop=min(pts[0:4,0])-cropPad
    xcropEnd=max(pts[0:4,0])+cropPad
    ycrop=min(pts[0:4,1])-cropPad*4 # leave space for the text
    ycropEnd=max(pts[0:4,1])+cropPad
    xoffset=pts[0,0]-xcrop
    yoffset=pts[0,1]-ycrop
    
    estimatedRectSide=(numPads-1)*interpad
    ptsRef=np.array([[0,0],[estimatedRectSide,0],[estimatedRectSide,estimatedRectSide],[0,estimatedRectSide]],np.int32)
    #ptsRef=np.array([[2*interpad,2*interpad],[estimatedRectSide,2*interpad],[estimatedRectSide,estimatedRectSide],[2*interpad,estimatedRectSide]],np.int32)
    
    M = cv.getAffineTransform(np.float32(pts[0:3]),np.float32(ptsRef[0:3]))
    Mback = cv.getAffineTransform(np.float32(ptsRef[0:3]),np.float32(pts[0:3]))
    
    MbackP = cv.getPerspectiveTransform(np.float32(ptsRef[0:4]),np.float32(pts[0:4]))
   
    # quick sense check
    for i in range(0,len(ptsRef)):
        xval,yval=ptsRef[i]
        xtran=rowMult(Mback,0,xval,yval)
        ytran=rowMult(Mback,1,xval,yval)
        print(pts[i],xtran,ytran)
    
    colimg=cv.polylines(colimg,[pts.reshape((-1,1,2))],True,(65535,0,0))
    colimg=cv.putText(colimg,patchName,(pts[0,0],pts[0,1]-2*interpad),cv.FONT_HERSHEY_SIMPLEX,1,(65535,0,0),2,cv.LINE_AA)
 
    
    cropOrig=origimg[ycrop:ycropEnd,xcrop:xcropEnd]
    ok=cv.imwrite(folderStub+fileStub+patchName+ " origCrop.tif", cropOrig)
    
    cropImg=colimg[ycrop:ycropEnd,xcrop:xcropEnd]
    
    resAffine = cv.resize(cropImg,None,fx=scaleFac, fy=scaleFac, interpolation = cv.INTER_NEAREST)
    ok=cv.imwrite(folderStub+fileStub+patchName+ " subAreaZoom.png", resAffine)
    resAffine=cv.putText(resAffine,"Affine transformed fixed grid. Manual grid region selection.",(resAffine.shape[0]//8,90),cv.FONT_HERSHEY_SIMPLEX,2,(65535,0,0),2,cv.LINE_AA)
     
    cropImg=colimg[ycrop:ycropEnd,xcrop:xcropEnd]
    resPersp = cv.resize(cropImg,None,fx=scaleFac, fy=scaleFac, interpolation = cv.INTER_NEAREST)
    resPersp=cv.putText(resPersp,"Perspective transformed fixed grid. Manual grid region selection.",(resPersp.shape[0]//8,90),cv.FONT_HERSHEY_SIMPLEX,2,(65535,0,0),2,cv.LINE_AA)
    
 
    sep=interpad*scaleFac
    rad=np.int32(sep/2)
    pixvals=np.empty([numPads,numPads])
    for y in range(0,numPads):
        for x in range(0,numPads):
            xval=np.floor(x*interpad)  
            yval=np.floor(y*interpad)
            
            xtran=rowMult(Mback,0,xval,yval)
            ytran=rowMult(Mback,1,xval,yval)
            resAffine=cv.circle(resAffine,(np.int32(scaleFac*(xtran-xcrop)),np.int32(scaleFac*(ytran-ycrop))),rad,(0,65535,0),1)
            
            perScale=rowMult(MbackP,2,xval,yval)
            xtran=rowMult(MbackP,0,xval,yval)/perScale
            ytran=rowMult(MbackP,1,xval,yval)/perScale
            resPersp=cv.circle(resPersp,(np.int32(scaleFac*(xtran-xcrop)),np.int32(scaleFac*(ytran-ycrop))),rad,(0,0,65535),1)
            #print(x,xval,yval,xtran,ytran)
            # doing the rows and columns this way to match what matshow expects to get things the right way up
            pixvals[y,x]=np.sum(origimg[np.int32(ytran-interpad):np.int32(ytran+interpad),np.int32(xtran-interpad):np.int32(xtran+interpad)])
    
    #cv.imshow('res',resPersp)
    
    ok=cv.imwrite(folderStub+fileStub+patchName+ " subAreaZoomAffineGrid.png", resAffine)
    ok=cv.imwrite(folderStub+fileStub+patchName+ " subAreaZoomPerspGrid.png", resPersp)

    plt.ioff()
    plt.
    plt.hist(pixvals.flatten(),bins=256, color = 'r')
    plt.title('Histogram of pad pixel sums for '+fileStub+' '+patchName)
    plt.grid(True)
    plt.savefig(folderStub+fileStub+patchName+ " subAreaZoomPerspGridHist.png")
    plt.close()
    
    plt.ioff()
    plt.matshow(pixvals,interpolation="none")
    plt.title('Map of pad pixel sums for '+fileStub+' '+patchName)
    plt.savefig(folderStub+fileStub+patchName+ " subAreaZoomPerspGridMatView.png")
    plt.close()

ok=cv.imwrite(folderStub+fileStub+".png", colimg)


# spatialGradient
e2 = cv.getTickCount()
time = (e2 - e1)/ cv.getTickFrequency()
print("All processing including loading and saving images complete in",time,"seconds")
print("Processor	Intel(R) Core(TM) i9-9900X CPU @ 3.50GHz, 3504 Mhz, 10 Core(s), 64 GB RAM")

