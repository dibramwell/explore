import os, sys
import cv2
import numpy as np
from matplotlib import pyplot as plt



def ecc_alignment(img1_path, img2_path, warp_mode = cv2.MOTION_TRANSLATION):

    # Read the images to be aligned
    im1 = cv2.imread(img1_path,cv2.IMREAD_ANYDEPTH )
    lower,upper=np.percentile(im1,(0.1,99.9))
    greyFac=255/(upper-lower)
    im1_gray=np.float32(im1)

    im2 = cv2.imread(img2_path,cv2.IMREAD_ANYDEPTH )
    lower,upper=np.percentile(im2,(0.1,99.9))
    greyFac=255/(upper-lower)
    im2_gray=np.float32(im2)
  

    # Find size of image1
    sz = im1_gray.shape

    # Define the motion model
    warp_mode = cv2.MOTION_TRANSLATION

    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else :
        warp_matrix = np.eye(2, 3, dtype=np.float32)
        
    # Specify the number of iterations.
    number_of_iterations = 50;

    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-2 # 1e-10;

    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)

    # Run the ECC algorithm. The results are stored in warp_matrix.
    inputMask = None
    gaussFiltSize = 1
    (cc, warp_matrix) = cv2.findTransformECC(im1_gray, im2_gray, warp_matrix, warp_mode, criteria, inputMask, gaussFiltSize)


    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        # Use warpPerspective for Homography 
        im2_aligned = cv2.warpPerspective (im2_gray, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_CONSTANT, 
                          borderValue=np.min(im2_gray))
    else :
        # Use warpAffine for Translation, Euclidean and Affine
        im2_aligned = cv2.warpAffine(im2_gray, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_CONSTANT, 
                          borderValue=0);

    cv2.imwrite("im1.tif", im1 )
    cv2.imwrite("im2.tif", im2 )
    cv2.imwrite("im2warp.tif", np.uint16(im2_aligned) )

    lower,upper=np.percentile(im1,(0.1,99.9))
    greyFac=255/(upper-lower)
    img=255-np.uint8(np.clip(np.floor(greyFac*(im1-lower)),0,255))

    lower,upper=np.percentile(im2,(0.1,99.9))
    greyFac=255/(upper-lower)
    img2=255-np.uint8(np.clip(np.floor(greyFac*(im2-lower)),0,255))

    img2a=255-np.uint8(np.clip(np.floor(greyFac*(im2_aligned-lower)),0,255))
   
    overColour = cv2.merge((img2,img,img2))
    cv2.imwrite("img_over.png", overColour )
    overColour = cv2.merge((img2a,img,img2a))
    cv2.imwrite("img_aligned.png", overColour )

    return im2_aligned
    #cv2.imwrite("img_aligned.png", im2_aligned )

img1_path = "_images/FC4575_LOBE01_LANEB_0--Stage17--488.tif"
img2_path = "_images/FC4575_LOBE02_LANEB_0--Stage17--488.tif"

result = ecc_alignment(img1_path, img2_path,warp_mode=cv2.MOTION_HOMOGRAPHY)

plt.imshow(result), plt.show()
