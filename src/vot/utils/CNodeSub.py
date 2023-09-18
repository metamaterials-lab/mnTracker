import cv2

from src import CONFIG_FILE
from src.vot.utils.CNodeBase import CNodeBase


MAX_SUB_NODES  = CONFIG_FILE.get( "MAXIMUM_SUB_NODES", 2 )
PLOT_ARROWS    = CONFIG_FILE.get( "PLOT_ARROWS", False )
SCALE_ARROWS   = CONFIG_FILE.get( "SCALE_ARROWS", 1 )

def gen_iter():
    while True:
        for i in range( MAX_SUB_NODES ):
            yield i

class CNodeSub( CNodeBase ):
    __ITER__ = gen_iter()
    def __init__( self, x : int = None, y : int = None ) -> None:
        super().__init__( x, y )
        self.n     = self.enum()
        self.color = ( 0, 200, 200 )
    def enum( self ):
        try:
            return next( self.__ITER__ )
        except StopIteration:
            raise Exception( "Error Enumarating Sub Nodes" )
    def draw( self, img, r : int = 10, live : bool = False ):
        if isinstance( self.x, int ) and isinstance( self.y, int ):
            center = ( self.x, self.y )
            cv2.circle( img, center, r if not live else int(r * 0.4), self.color, 2 if live else -1 )
            if not live:
                ctext  = ( self.x - 4 if self.n < 10 else self.x - 8, self.y + 4 )
                cv2.putText( img, str( self.n ), ctext, cv2.FONT_HERSHEY_SIMPLEX, 0.04 * r, (0,0,0), 1, cv2.LINE_AA )
            #else:
            #    if isinstance( self.dx, float ) and isinstance( self.dy, float ) and PLOT_ARROWS:
            #        p1 = ( self.x, self.y )
            #        p2 = ( int( self.x + SCALE_ARROWS * self.dx ), int( self.y + SCALE_ARROWS * self.dy ) )
            #        cv2.arrowedLine( img, p1, p2, self.color, 2 )