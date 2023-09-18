import cv2
import typing

def metrics( cap : cv2.VideoCapture, fsize : typing.Tuple[int,int] ):
    count = int( cap.get( cv2.CAP_PROP_FRAME_COUNT ) )
    w     = int( cap.get( cv2.CAP_PROP_FRAME_WIDTH ) )
    h     = int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT ) )
    return count, ( w / fsize[0], h / fsize[1] ), ( w, h )

class CVideoCapture:
    def __init__( self, filename : str, fix_size : typing.Tuple[int, int] = ( 640, 480 ) ):
        self.fsize  = fix_size
        self.cap    = cv2.VideoCapture( filename )
        self.count, self.scale , self.ssize = metrics( self.cap, self.fsize )
        self.gen    = self.run()
        self.active = False

    def _draw( self, I ):
        return I

    def draw( self, frame ):
        image  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image  = self._draw( image )
        return cv2.resize( image, self.fsize )

    def run( self ):
        frame = None
        f = 0
        while f < self.count:
            if self.active:
                ret, frame = self.cap.read()
                f += 1
                if ret:
                    yield self.draw( frame )
                else:
                    frame = None
                    yield frame
            else:
                if isinstance( frame, type( None ) ):
                    yield frame
                else:
                    yield self.draw( frame )

    def next( self, active : bool = True ):
        self.active = active
        return next( self.gen )

    def __del__( self ):
        self.cap.release()
