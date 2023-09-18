from src import CONFIG_FILE

CALC_DIRECTION = CONFIG_FILE.get( "CALC_DIRECTION_EACH", 10 )
FPS            = CONFIG_FILE.get( "FRAMES_PER_SECOND", 30 )

class CNodeBase:
    def __init__( self, x : int = None, y : int = None ) -> None:
        self.x = x; self.y = y
        self.dx = None; self.dy = None
        self._x = None; self._y = None
        self.gen = self.setGen( CALC_DIRECTION )
    def set( self, x : int = None, y : int = None ) -> None:
        self.x = x
        self.y = y
        next( self.gen )
    def setGen( self, n : int ) -> None:
        while True:
            for _ in range( n ): yield None
            if isinstance( self._x, int ) and isinstance( self._y, int ):
                if self.x - self._x:
                    self.dx = ( self.x - self._x ) * FPS / CALC_DIRECTION
                if self.y - self._y:
                    self.dy = ( self.y - self._y ) * FPS / CALC_DIRECTION
            self._x = self.x; self._y = self.y 
    def draw( self, img, *args ):
        pass
    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    def __bool__(self) -> bool:
        return isinstance( self.x, int ) and isinstance( self.y, int )
    def __iter__(self):
        yield self.x
        yield self.y
    def __add__(self, A):
        return CNodeBase( self.x + A.x, self.y + A.y )
    def __sub__(self, A):
        return CNodeBase( self.x - A.x, self.y - A.y )