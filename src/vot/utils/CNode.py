import cv2

from random import randint

from src import CONFIG_FILE
from src.vot.utils.CNodeBase import CNodeBase


MAX_NODES      = CONFIG_FILE.get( "MAXIMUM_NODES", 20 )
PLOT_ARROWS    = CONFIG_FILE.get( "PLOT_ARROWS", False )
SCALE_ARROWS   = CONFIG_FILE.get( "SCALE_ARROWS", 1 )

class CNode( CNodeBase ):
    __ITER__   = ( i for i in range( MAX_NODES ) )
    def __init__( self, x : int = None, y : int = None ) -> None:
        super().__init__( x, y )
        self.n     = self.enum()
        self.color = hsl2rgb( randint( 0,360 ), 0.8, 0.8 )
    def enum( self ):
        try:
            return next( self.__ITER__ )
        except StopIteration:
            raise Exception( "Max number of nodes reached!" )
    def draw( self, img, r : int = 10, live : bool = False ):
        if bool(self):
            center = ( self.x, self.y )
            cv2.circle( img, center, r, self.color, 2 if live else -1 )
            if not live:
                ctext  = ( self.x - 4 if self.n < 10 else self.x - 8, self.y + 4 )
                cv2.putText( img, str( self.n ), ctext, cv2.FONT_HERSHEY_SIMPLEX, 0.04 * r, (0,0,0), 1, cv2.LINE_AA )
            else:
                if isinstance( self.dx, float ) and isinstance( self.dy, float ) and PLOT_ARROWS:
                    p1 = ( self.x, self.y )
                    p2 = ( int( self.x + SCALE_ARROWS * self.dx ), int( self.y + SCALE_ARROWS * self.dy ) )
                    cv2.arrowedLine( img, p1, p2, self.color, 2 )

def hsl2rgb( h : int, s : int = 0.8, l : int = 0.8 ):
    d = s * ( 1 - abs(2 * l - 1) )
    m = 255 * ( l - 0.5 * d )
    x = d * ( 1 - abs( (h/60)%2 - 1 ) )
    if h >= 0 and h < 60:
        r = 255*d + m; g = 255*x + m; b = m
    elif h >= 60 and h < 120:
        r = 255*x + m; g = 255*d + m; b = m
    elif h >= 120 and h < 180:
        r = m; g = 255*d + m; b = 255*x + m
    elif h >= 180 and h < 240:
        r = m; g = 255*x + m; b = 255*d + m
    elif h >= 240 and h < 300:
        r = 255*x + m; g = m; b = 255*d + m
    else:
        r = 255*d + m; g = m; b = 255*x + m
    return ( int(r), int(g), int(b) )