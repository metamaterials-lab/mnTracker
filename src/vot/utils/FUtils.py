import numpy as np
from typing import Tuple

#import matplotlib.pyplot as plt
#def image_show( I : np.ndarray ) -> None:
#    h, w = I.shape
#    Y, X = np.mgrid[ 0:h, 0:w ]
#    _, ax = plt.subplots()
#    ax.pcolormesh( X, Y, I, cmap=plt.colormaps["jet"])
#    plt.show()

def crop_frame( img : np.ndarray, roi : Tuple[int,int,int,int] ) -> np.ndarray:
    return img[ 
        roi[0]-roi[2] : roi[0]+roi[2],
        roi[1]-roi[3] : roi[1]+roi[3] ]