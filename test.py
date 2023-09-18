import cv2
import numpy as np


def rotPoints( pts : np.ndarray ):
    A = pts[ 0 ]; C = pts[ -1 ] - A
    alpha = np.arctan2( C[1], C[0] )
    R = np.array(
        [
            [  np.cos( alpha ),  np.sin( alpha ) ],
            [ -np.sin( alpha ),  np.cos( alpha ) ]
        ]
    )
    npts = R @ ( pts - A ).T 
    npts = npts.astype( np.int32 )
    return npts.T

def fitTheoreticalCurve( pts : np.ndarray, N : int = 10 ):
    D = pts[ 1 ]; B = pts[ -1 ]
    xd = int( D[0] ); xb = int( B[0] )
    X = np.array(
        [
            [   xb**4,   xb**3,   xb**2 ],
            [ 4*xb**3, 3*xb**2, 2*xb    ],
            [   xd**4,   xd**3,   xd**2 ]
        ]
    ).astype( np.int64 )
    Y = np.array(
        [ 
            [0],
            [0],
            [D[1]]
        ]
    )
    a = np.linalg.solve( X, Y )
    x = np.linspace( 0, xb, N )
    y = a[0]*x**4 + a[1]*x**3 + a[2]*x**2
    return np.array( [ x, y ] ).T.astype( np.int32 )

capture = cv2.VideoCapture( "./media/HexBlue_1.MP4" )
ret, frame = capture.read()

pts = np.array([[200,200],[300,350],[400,400]], np.int32)
pts = rotPoints( pts )
pts = fitTheoreticalCurve( pts )

if ret:
    Img = cv2.polylines( frame, [pts], False, (255,0,0), 3 )
    cv2.imshow( "Image", frame )
    cv2.waitKey()