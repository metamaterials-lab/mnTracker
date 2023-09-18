import csv
import typing

from src import CONFIG_FILE
from src.utils.CDiff import CDiff

TCOL = CONFIG_FILE.get( "TIME_COL_NAME", "TIME" )
XCOL = CONFIG_FILE.get( "X_COL_NAME", "STRAIN" )
YCOL = CONFIG_FILE.get( "Y_COL_NAME", "STRESS" )

class CTexturometer:
    def __init__(self) -> None:
        self.file   = None
        self.reader = None
        self.x      = []
        self.y      = []
        self.diff   = CDiff()
    def init(self, file : str) -> None:
        self.xlim, self.ylim = self.stats( file )
        self.file   = open( file )
        self.reader = csv.DictReader( self.file )
        self.data   = next( self.reader )
        self.next()
    def stats(self, file : str):
        with open(file, "r") as csvfile:
            data = csv.DictReader(csvfile, delimiter=',')
            #next( data )
            x, y = [], []
            for i in data:
                x.append(float( i[XCOL] ))
                y.append(float( i[YCOL] ))
        xlim = [ 0, max(x) ]
        ylim = [ 0, max(y) ]
        return xlim, ylim
    def next(self):
        try:
            data =  next( self.reader )
        except StopIteration:
            return False
        self.pdata = self.data
        self.data  = data
        return True
    def get( self, time : float, flag : bool = True ):
        if isinstance( self.reader, csv.DictReader ):
            while True:
                if self._flag(time): break
                if not self.next(): break
            x = self._interpol( time, XCOL )
            y = self._interpol( time, YCOL )
            if not flag:
                self.diff.diff( x, y )
            else:
                self.x.append( x )
                self.y.append( y )
                self._plot( self.x, self.y, self.xlim, self.ylim )
            return x, y
        else:
            return "", ""
    def _plot( self,
              x : typing.List[float],
              y : typing.List[float],
              xlim : typing.Tuple[ float, float ],
              ylim : typing.Tuple[ float, float ]  ) -> None:
        pass
    def _interpol(self, time:float, key:str):
        return ( float(self.data[key]) - float(self.pdata[key]) ) / ( int(self.data[TCOL]) - int(self.pdata[TCOL]) ) * ( time - int(self.pdata[TCOL]) ) + float(self.pdata[key])
    def _flag(self, time:float):
        return ( int( self.data[TCOL] ) >= time ) and ( int( self.pdata[TCOL] ) <= time )
    def __del__( self ):
        if not isinstance( self.file, type( None ) ):
            self.file.close()