import os
import datetime

from src import CONFIG_FILE
from src.utils.CTimer import CTimer
from src.vot.utils.CNode import CNode
from src.vot.utils.CStruts import CStruts
from src.utils.CTexturometer import CTexturometer

RADIUS         = CONFIG_FILE.get( "MARKER_RADIUS", 10 )
SAVE_EACH      = CONFIG_FILE.get( "SAVE_DATA_EACH", 10 )
RESULTS_PATH   = CONFIG_FILE.get( "RESULTS_PATH", "." )
SAVE_RESULTS   = CONFIG_FILE.get( "SAVE_RESULTS", False )
#FPS            = CONFIG_FILE.get( "FRAMES_PER_SECOND", 30 )
TCOL           = CONFIG_FILE.get( "TIME_COL_NAME", "TIME" )
XCOL           = CONFIG_FILE.get( "X_COL_NAME", "STRAIN" )
YCOL           = CONFIG_FILE.get( "Y_COL_NAME", "STRESS" )

class CFileWriter:
    def __init__(self) -> None:
        self.origin   = None
        self.scale    = 1.0
        self.txtmtr   = None
        self.time     = 0
        #self.T        = int( 1000/FPS )
        self.T        = CTimer()
        self.setResultsFile()
    def setResultsFile( self ):
        file = os.path.abspath( RESULTS_PATH )
        if not os.path.isdir( file ): os.makedirs( file )
        name = f"Results_{datetime.datetime.now():%Y-%m-%d}"
        c = 0
        while True:
            filename = os.path.join( file,  f"{name}_{c}.csv" )
            c += 1
            if not os.path.isfile( filename ): break
        if SAVE_RESULTS: self.file = open( filename, "w" ); self.gen  = self.writeGen( SAVE_EACH )
    def writeGen( self, n : int ):
        line = f"{TCOL},"
        for i, _ in enumerate( self.nodes.items() ):
            line = line + f"M{i}X,M{i}Y,"
        line = line + self.getStrutsHeaders()
        line = f"{line}{XCOL},{YCOL}\n"
        self.file.write( line )
        while True:
            for _ in range( n ):
                if isinstance( self.txtmtr, CTexturometer ): self.txtmtr.get( self.time, False )
                yield None
            self.write()
    def write( self ):
        line = f"{self.time},"
        for _, marker in self.nodes.items():
            x, y = self.scaleCoord( marker )
            line = line + "{:.3f},{:.3f},".format( x, y )
        line = line + self.getStruts()
        if isinstance( self.txtmtr, CTexturometer ):
            x, y = self.txtmtr.get( self.time, True )
            if isinstance( x, str ):
                line = "{},\n".format( line )
            else:
                line = "{}{:.3f},{:.3f}\n".format( line,x,y )
        else:
            line = f"{line},\n"
        self.file.write( line )
    def timestep( self ):
        #self.time = self.time + self.T
        self.time = self.T.timeStep()
    def scaleCoord(self, node:CNode):
        if isinstance( self.origin, tuple ):
            x = ( node.x - self.origin[0] ) * self.scale
            y = ( self.origin[1] - node.y ) * self.scale
        else:
            x, y = node.x, node.y
        return x, y
    
    def getStrutsHeaders( self ) -> str:
        line = ""
        if isinstance( self.struts, CStruts ):
            for strut in self.struts.dump():
                for node in strut:
                    prefix = f"S{node.n}({strut.strut[0]}&{strut.strut[1]})"
                    line = line + f"{prefix}X,{prefix}Y,"
                line = line + f"A({strut.strut[0]}&{strut.strut[1]})," + f"D({strut.strut[0]}&{strut.strut[1]}),"
        return line
    
    def getStruts( self ) -> str:
        line = ""
        if isinstance( self.struts, CStruts ):
            for strut in self.struts.dump():
                for node in strut:
                    line = line + f"{node.x},{node.y},"
                line = line + f"{strut.tangle}," + f"{strut.diff_ang.dy},"
        return line

    def __del__( self ):
        if SAVE_RESULTS: self.file.close()
        