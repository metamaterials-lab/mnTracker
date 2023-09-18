import typing

from src.vot.utils.CNode import CNode
from src.vot.utils.CStrut import CStrut

class CStruts:
    def __init__( self, struts : typing.List[ typing.Tuple[ int, int ] ], nodes : typing.Dict[ int, CNode ] ) -> None:
        self.struts       = [ CStrut( strut, nodes ) for strut in struts ]
        self.struts_list  = struts
        self.idx          = None
    def draw( self, I, live : bool ):
        for strut in self.struts:
            strut.draw( I, live )
    def setIdx( self, i : int = None ):
        self.idx = i
    def get( self ):
        if isinstance( self.idx, int ):
            return self.struts[ self.idx ]
    def __iter__(self):
        for strut in self.struts_list:
            yield strut
    def dump( self ):
        struts = []
        for strut in self.struts:
            flag = False
            if bool( strut ):
                for n in strut.subnodes:
                    if bool(n): flag = True; break
                if flag: struts.append( strut )
        return struts
