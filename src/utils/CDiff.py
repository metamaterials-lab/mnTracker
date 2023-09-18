import numpy as np
import functools
from src import CONFIG_FILE

NDIFF = CONFIG_FILE.get( "N_DIFF", 50 )
NPEAK = CONFIG_FILE.get( "N_PEAK", 5 )
#PTOL  = CONFIG_FILE.get( "PEAK_TOL", 5e-5 )

class CDiff:
    def __init__(self) -> None:
        self.x = []
        self.y = []
        self._dy   = [ 0.0 ]
        self._peak = [False]

    @property
    def peak( self ) -> bool:
        return functools.reduce( lambda x, y : x and y, self._peak )
    @peak.setter
    def peak( self, peak : bool ):
        if len( self._peak ) > NPEAK: self._peak.pop( 0 )
        self._peak.append( peak )

    @property
    def dy( self ) -> float:
        return self._dy[-1]
    @dy.setter
    def dy( self, dy : float ):
        if len( self._dy ) > NPEAK: self._dy.pop( 0 )
        self._dy.append( dy )
        if abs( max( self._dy, key=abs ) ) > abs( self.dy ): self.peak = True
        else: self.peak = False

    def diff( self, x : float, y : float ) -> None:
        self.slice( x, y )
        X = np.c_[ self.x ]
        Y = np.c_[ self.y ]
        A = np.column_stack( ( np.ones_like( X ), X ) )
        Q,R = np.linalg.qr( A, mode="reduced" )
        if np.count_nonzero( np.diag( R ) ) == A.shape[ 1 ]:
            a = np.linalg.solve( R, Q.T @ Y )
            self.dy = a[1,0]
        
        
    def slice( self, x : float, y : float ) -> None:
        if len( self.x ) > NDIFF: self.x.pop( 0 ); self.y.pop( 0 )
        self.x.append( x )
        self.y.append( y )
