import cv2
import typing

from src import CONFIG_FILE
from src.utils.CBeam import CBeam
from src.vot.utils.CNode import CNode
from src.vot.utils.CNodeSub import CNodeSub, gen_iter

RADIUS         = CONFIG_FILE.get( "MARKER_RADIUS", 10 )
IDX_ITER       = gen_iter()

class CStrut( CBeam ):
    def __init__( self, strut : typing.Tuple[ int, int ], nodes : typing.Dict[ int, CNode ] ) -> None:
        super().__init__( strut, nodes )
        self.idx      = 0
        self.r        = RADIUS
        next( IDX_ITER )
    def next( self ):
        self.idx    = next( IDX_ITER )
    def get( self ) -> CNodeSub:
        if bool(self):
            return self.subnodes[ self.idx ]
        else:
            return CNodeSub()
    def draw( self, I, live : bool ):
        self.norm ( live )
        self.angle( live )
        self._draw( I, live )
        for subnode in self.subnodes:
            subnode.draw( I, live=live )
    
def connect_lines( I, A : CNode, B : CNode, S : typing.List[ CNodeSub ], color : typing.Tuple[int,int,int] = (0,255,0) ):
    C = [( A.x, A.y )]
    for s in S:
        if bool( s ): C.append( (s.x, s.y) )
    C.append( ( B.x, B.y ) )
    for i in range( 1, len(C) ):
        cv2.line( I, C[i-1], C[i], color, 2, 4 )