import cv2
import math
import numpy as np
import typing

class CCross:
    def __init__( self, x : int = None, y : int = None ) -> None:
        self.x = x
        self.y = y
        self.color = (0,255,0)
    def set( self, x : int = None, y : int = None ) -> None:
        self.x = x
        self.y = y
    def draw( self, img, r : int = 10 ):
        if bool(self):
            p1 = ( self.x, self.y + r ); p2 = ( self.x, self.y - r ) 
            cv2.line( img, p1, p2, self.color, 2 )
            p1 = ( self.x + r, self.y ); p2 = ( self.x - r, self.y ) 
            cv2.line( img, p1, p2, self.color, 2 )
    def pos(self):
        return self.x, self.y
    def __bool__(self):
        if isinstance( self.x, int ) and isinstance( self.y, int ):
            return True
        return False
    def __sub__(self, A):
        if bool(self) and bool(A):
            return CCross( self.x - A.x, self.y - A.y )
        return CCross()
    def norm( self ):
        if bool(self):
            return math.sqrt( self.x**2 + self.y**2 )
        
class CCoord( CCross ):
    def __init__(self, x: int = None, y: int = None) -> None:
        super().__init__(x, y)
        self.color = (255,0,0)
    def draw(self, img, r: int = 50):
        if bool(self):
            p = ( self.x, self.y )
            p2 = ( self.x, self.y - r ) 
            cv2.line( img, p, p2, self.color, 2 )
            cv2.putText( img, "Y", p2, cv2.FONT_HERSHEY_SIMPLEX, 0.02*r, (0,0,0), 2, cv2.LINE_AA )
            p2 = ( self.x + r, self.y ) 
            cv2.line( img, p, p2, self.color, 2 )
            cv2.putText( img, "X", p2, cv2.FONT_HERSHEY_SIMPLEX, 0.02*r, (0,0,0), 2, cv2.LINE_AA )

class CLine:
    def __init__(self, co : typing.Tuple[int,int] = (0,0)) -> None:
        self.color = (0,0,255)
        self.p1 = CCross()
        self.p2 = CCross()
        self.co = CCoord( *co )
        self.cp = None
        self.gen = self.getGen()
        self.next()
    def length(self):
        if bool(self.p1) and bool(self.p2):
            return (self.p1 - self.p2).norm()
    def origin(self):
        if bool( self.co ):
            return ( self.co.x, self.co.y )
    def getGen(self):
        while True:
            yield self.p1
            yield self.p2
            yield self.co
    def next(self):
        self.cp = next( self.gen )
    def set(self, x:int, y:int):
        self.cp.set( x, y )
    def draw(self, img):
        I = np.copy( img )
        if bool( self.p1 ) and bool( self.p2 ):
            cv2.line( I, self.p1.pos(), self.p2.pos(), self.color, 2 )
        self.p1.draw( I )
        self.p2.draw( I )
        self.co.draw( I )
        return I