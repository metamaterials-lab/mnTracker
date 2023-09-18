from src.utils.CVideoCapture import CVideoCapture

class CZoom:
    def __init__(self, cap : CVideoCapture) -> None:
        self.fsize = cap.fsize
        self.ssize = cap.ssize
        self.scale = cap.scale
        self.zfact = 1.0
        # Initialize Box
        self.zoom()

    def zoom( self, x : int = 0, y : int = 0, scale : float = 1.0 ):
        w, h = self.ssize
        xmin = int( x - scale * w / 2 )
        xmax = int( x + scale * w / 2 )
        ymin = int( y - scale * h / 2 )
        ymax = int( y + scale * h / 2 )
        if xmin < 0: xmax = int( xmax - xmin ); xmin = 0
        if ymin < 0: ymax = int( ymax - ymin ); ymin = 0
        if xmax > w: xmin = xmin - ( xmax - w ); xmax = w
        if ymax > h: ymin = ymin - ( ymax - h ); ymax = h
        
        self.box = ( xmin, ymin, xmax, ymax )

    def crop( self, img ):
        xmin, ymin, xmax, ymax = self.box
        return img[ ymin:ymax, xmin:xmax ]

    def getPos( self, x : int, y : int ):
        xmin, ymin, _, _ = self.box
        return xmin + int( x * self.scale[0] * self.zfact ), ymin + int( y * self.scale[1] * self.zfact )

    def mouse_callback( self, x : int, y : int, p : int ):
        if p > 0:
            self.zfact = scale( self.zfact, False )
            self.zoom( x, y, self.zfact )
        else:
            self.zfact = scale( self.zfact, True )
            self.zoom( x, y, self.zfact )

def scale( scale, dir = True ) -> float:
    if dir: return min( scale + 0.05, 1.0 )
    else:   return max( scale - 0.05, 0.2 )