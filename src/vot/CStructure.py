import typing

from src import CONFIG_FILE
from src.vot.utils.CStruts import CStruts
from src.vot.utils.CNode import CNode
from src.vot.utils.CFileWriter import CFileWriter
from src.vot.utils.CStrutManager import CStrutManager
from src.utils.CStateMachine import CStateMachine

RADIUS         = CONFIG_FILE.get( "MARKER_RADIUS", 10 )
SAVE_RESULTS   = CONFIG_FILE.get( "SAVE_RESULTS", False )

class CStructure( CFileWriter, CStrutManager ):
    def __init__(self) -> None:
        super().__init__()
        super(CFileWriter, self).__init__()
        self.idx     = 0
        self.idx_max = 0
        self.r       = RADIUS
    def next( self ):
        if isinstance( self.struts, CStruts ):
            if isinstance( self.struts.idx, int ):
                self.struts.get().next(); return
        self._next()
    def _next( self ):
        if self.idx in list( self.nodes.keys() ):
            self.idx += 1
            if self.idx > self.idx_max:
                self.idx_max += 1 
    def setIdx( self, idx : int ):
        if idx <= self.idx_max:
            self.idx = idx
    def setSubIdx( self, idx : int = None ):
        self.struts.setIdx( idx )
    def get( self ) -> CNode:
        if isinstance( self.struts, CStruts ):
            if isinstance( self.struts.idx, int ):
                return self.struts.get().get()
        return self._get()
    def _get( self ) -> CNode:
        if self.idx in list( self.nodes.keys() ):
            return self.nodes.get( self.idx )
        else:
            self.nodes[ self.idx ] = CNode()
            return self.get()
    def draw( self, I, live : bool = False ):
        if isinstance( self.state, CStateMachine ): self.state.next()
        if live and SAVE_RESULTS: next( self.gen )
        if isinstance( self.struts, CStruts ): self.struts.draw( I, live )
        for _, node in self.nodes.items():
            node.draw( I, self.r, live )
    def dump( self ) -> typing.List[ typing.Tuple[ int, int, int, int ] ]:
        rois = []
        for _, node in self.nodes.items():
            roi = ( node.y, node.x, self.r, self.r )
            rois.append( roi )
        if isinstance( self.struts, CStruts ):
            for strut in self.struts.dump():
                for node in strut:
                    roi = ( node.y, node.x, self.r, self.r )
                    rois.append( roi )
        return rois
    def load( self, rois: typing.List[ typing.Tuple[ int, int ] ] ):
        irois = iter( rois )
        for _, node in self.nodes.items():
            x, y = next( irois )
            node.set( y, x )
        if isinstance( self.struts, CStruts ):
            for strut in self.struts.dump():
                for node in strut:
                    x, y = next( irois )
                    node.set( y, x )