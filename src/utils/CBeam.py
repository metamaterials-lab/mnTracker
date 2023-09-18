import cv2
import math
import typing
import numpy as np
import functools

from src import CONFIG_FILE
from src.utils.CTimer import CTimer
from src.vot.utils.CNode import CNode
from src.vot.utils.CNodeSub import CNodeSub
from src.utils.CDiff import CDiff

MAX_SUB_NODES  = CONFIG_FILE.get( "MAXIMUM_SUB_NODES", 2 )
CURVE_METHOD   = CONFIG_FILE.get( "CURVE_METHOD", "" ).lower()

class State:
    def __init__(self) -> None:
        self.buckling = False
        self.bending  = False
        self.stretch  = False
    def color( self ) -> typing.Tuple[int,int,int]:
        r = 0; g = 0; b = 0
        if self.buckling: r = 255; g = 255; b = 255
        if self.bending:  g = 255
        if self.stretch:  b = 255
        return (r,g,b)

class CBeam:
    def __init__( self, strut : typing.Tuple[ int, int ], nodes : typing.Dict[ int, CNode ] ) -> None:
        super().__init__()
        self.strut    = strut
        self.nodes    = nodes
        self.subnodes = [ CNodeSub() for _ in range( MAX_SUB_NODES ) ]
        self._length  = []
        self._angle   = []
        self.tangle   = 0.0
        self.diff_ang = CDiff()
        self.t        = CTimer()
        self.state    = State()

    def getStrut( self ):
        s = self.strut
        A = self.nodes.get( s[0], None )
        B = self.nodes.get( s[1], None )
        return A, B

    def norm( self, live : bool ):
        if bool( self ):
            A,B = self.getStrut()
            S = [A] + list( self ) + [B]
            length = []
            for i in range( 1, len( S ) ):
                length.append( sNorm( S[ i-1 ], S[ i ] ) )
            if not live: self._length = length
            else: return [ self._length[i] - length[i] for i in range( len( length ) ) ]

    def angle( self, live : bool ):
        if bool( self ):
            A,B = self.getStrut()
            S = [A] + list( self ) + [B] 
            angle = []
            for i in range( 1, len( S ) ):
                angle.append( sAngle( S[ i-1 ], S[ i ] ) )
            if not live: self._angle = angle
            else: return [ self._angle[i] - angle[i] for i in range( len( angle ) ) ]

    def total_angle( self, angle : typing.List[float] ):
        total = 0.0
        if not isinstance( angle, type( None ) ):
            if CURVE_METHOD == "abs":
                total = functools.reduce( lambda x, y : abs( x ) + abs( y ), angle )
            else:
                total = functools.reduce( lambda x, y : x + y, angle )
        return total

    def _draw( self, I, live : bool ):
        A,B = self.getStrut()
        if bool( self ):
            length = self.norm( live )
            angle  = self.angle( live )
            #r = 0; b = 0
            if live:
                self.tangle = self.total_angle( angle )
                self.diff_ang.diff( self.t.TIMEMS, self.tangle )
            connect_lines( I, A, B, self.subnodes, self.state, angle, length )
            #draw_deflection( I, A, B, self.subnodes, ( r, 255, b ), self._angle, angle )

    def __bool__( self ) -> bool:
        A,B = self.getStrut()
        return isinstance( A, CNode ) and isinstance( B, CNode )
    
    def __iter__( self ):
        for node in self.subnodes:
            if bool( node ): yield node


def sNorm( A : CNode, B : CNode ):
    c = ( A.x - B.x, A.y - B.y )
    return math.sqrt( c[0]**2 + c[1]**2 )

def sAngle( A : CNode, B : CNode ):
    c = ( A.x - B.x, A.y - B.y )
    return math.atan2( c[1], c[0] )
    
def connect_lines( I, A : CNode, B : CNode,
                   S : typing.List[ CNodeSub ],
                   state : State,
                   angle : typing.List[ float ] = [],
                   norm : typing.List[ float ] = [] ):
    C = [( A.x, A.y )]
    for s in S:
        if bool( s ): C.append( (s.x, s.y) )
    C.append( ( B.x, B.y ) )
    for i in range( 1, len(C) ):
        #r = 0; b = 0
        #if not isinstance( norm, type( None ) ):
        #    r = 255 if abs( norm [i-1] ) > 2 else 0
        #    b = 255 if abs( angle[i-1] ) > 0.1 else 0
        cv2.line( I, C[i-1], C[i], state.color(), 2, 4 )












def poly_lines( I, P : np.ndarray, color : typing.Tuple[int,int,int] = (0,255,0) ):
    C = P.tolist()
    for i in range( 1, len( C ) ):
        cv2.line( I, C[i-1], C[i], color, 2, 4 )

def rot_matrix( alpha : float ) -> np.ndarray:
    return np.array(
        [
            [  np.cos( alpha ), -np.sin( alpha ) ],
            [  np.sin( alpha ),  np.cos( alpha ) ]
        ]
    )

def fit_curve( P : np.ndarray, N : int = 10 ):
    P1 = P[ 1 ]; x1 = int( P1[0] )
    P2 = P[ 2 ]; x2 = int( P2[0] )
    P3 = P[ 3 ]; x3 = int( P3[0] )
    X = np.array(
        [
            [   x1**5,   x1**4,   x1**3,   x1**2 ],
            [   x2**5,   x2**4,   x2**3,   x2**2 ],
            [   x3**5,   x3**4,   x3**3,   x3**2 ],
            [ 5*x3**4, 4*x3**3, 3*x3**2, 2*x3    ]
        ],
        np.int64
    )
    Y = np.array(
        [ 
            [P1[1]],
            [P2[1]],
            [P3[1]],
            [0]
        ]
    )
    a = np.linalg.solve( X, Y )
    x = np.linspace( 0, x3, N )
    y = a[0]*x**5 + a[1]*x**4 + a[2]*x**3 + a[3]*x**2
    return np.array( [ x, y ] ).T.astype( np.int32 )

def draw_deflection( I, A : CNode, B : CNode, S : typing.List[ CNodeSub ], color : typing.Tuple[ int, int, int ] = (0,255,0), alpha : float = None, dalpha : float = None  ):
    P = get_points( A, B , S )
    if P.shape[0] > 2:
        if isinstance( alpha, type( None ) ):
            C = B - A
            alpha = np.arctan2( C.y, C.x )
        if isinstance( dalpha, float ):
            alpha = alpha +  0.5 * dalpha
        R = rot_matrix(alpha)
        O = np.array( list(A) )
        Q = ( R @ ( P - O ).T ).astype( np.int64 ).T
        R = rot_matrix(-alpha)
        Q = ( R @ fit_curve( Q ).T ).T + O
        #Q = fit_curve(Q) + O
        Q = Q.astype( np.int32 )
        poly_lines( I, Q, color )
    else:
        poly_lines( I, P, color )

def get_points( A : CNode, B : CNode, S : typing.List[ CNodeSub ] ):
    points = [ list( A ) ]
    for s in S:
        if bool(s):
            points.append( list( s ) )
    points.append( list( B ) )
    return np.array( points )