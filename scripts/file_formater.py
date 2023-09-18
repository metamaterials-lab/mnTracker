import os
import csv
import typing

WINDOW_SIZE  = 20
WINDOW_STEPS = 3


class FileFormater:
    SKIP_LINES   = 4
    TIME_HEADER  = "TIME"
    DIST_HEADER  = "DISTANCE"
    FORC_HEADER  = "FORCE"

    STRN_HEADER  = "STRAIN"
    STRS_HEADER  = "STRESS"

    TIME_POS = 1
    DIST_POS = 3
    FORC_POS = 4
    def __init__( self, filename : str, L : float = None, A : float = None ):
        self.file = os.path.basename( filename )
        self.base = os.path.abspath( os.path.dirname( filename ) )
        self.L = L
        self.A = A

        filep = self.gen_name( self.file, "PARSED", self.base )
        filef = self.gen_name( self.file, "FORMATED", self.base )
        
        if not os.path.isfile( filep ):
            self.parse_results_file( filename, filep )
        if not os.path.isfile( filef ):
            self.detect_collision( filep, filef )

    def gen_name( self, file : str, subfix : str, base : str ):
        S = file.split( "." )
        S.insert( 1, f"_{subfix}." )
        w = ""
        for s in S: w = w + s
        return os.path.join( base, w )

    def parse_results_file( self, file_in : str, file_out : str ):
        with open( file_out, "w" ) as ofile:
            with open( file_in, "r" ) as pfile:
                for _ in range( self.SKIP_LINES ): pfile.readline()
                while True:
                    line = pfile.readline()
                    if line:
                        line = line.replace( ",", "." )
                        line = line.replace( ";", "," )
                        ofile.write( line )
                    else: break

    def detect_collision( self, file_in : str, file_out : str ):
        r = self.collision_iterator( file_in )
        self.collision_writer( file_in, file_out, r )

    def collision_iterator( self, file_in : str ):
        w = []
        with open( file_in, "r" ) as pfile:
            pfile.readline()
            reader = csv.reader( pfile )
            c = 0
            for line in reader:
                force = line[self.FORC_POS]
                w.append( float(force) )
                if len( w ) > WINDOW_SIZE: w.pop( 0 )
                if self.detector( w ): break
                c = c + 1
            r = c - list( reversed( w ) ).index( 0 )
        return r
    
    def collision_writer( self, file_in : str, file_out : str, r : int ):
        with open( file_out, "w" ) as ofile:
            with open( file_in, "r" ) as pfile:
                for _ in range( r ): pfile.readline()
                reader = csv.reader( pfile )
                if bool( self ): ofile.write( f"{self.TIME_HEADER},{self.STRN_HEADER},{self.STRS_HEADER}\n" )
                else: ofile.write( f"{self.TIME_HEADER},{self.DIST_HEADER},{self.FORC_HEADER}\n" )
                line = next( reader )
                t = int( line[ self.TIME_POS ] )
                d = float( line[ self.DIST_POS ] )
                ofile.write( f"0,0.0,0\n" )
                for line in reader:
                    ofile.write( self.gen_line( line, t, d ) )

    def gen_line( self, line : typing.List[str] , t : int , d : float ):
        T = int(line[self.TIME_POS]) - t
        E = float(line[self.DIST_POS]) - d
        S = int(line[self.FORC_POS])
        if bool(self):
            E = E / self.L; S = S / self.A
            return "{},{:.3f},{:.3f}\n".format( T, E, S )
        else:
            return "{},{:.3f},{}\n".format( T, E, S )

    def detector( self, l : typing.List[ int ] ):
        c = 0
        for i in range( 1, len( l ) ):
            if   l[ i - 1 ] < l[ i ]: c = c + 1
            elif l[ i - 1 ] > l[ i ]: c = c - 1
        return c > WINDOW_STEPS
    
    def __bool__( self ):
        return isinstance( self.L, float ) and isinstance( self.A, float )


# File formater function
# Parameters:
#   input_file  : string
#   length      : float | None
#   area        : float | None
#
# If length and/or area are omitted
# force and distance will be reported
# otherwise stress and stress will
# be computed.

FileFormater( "./media/hex_blue/HexBlue.csv", 62.0, 960.0 )

# FileFormater( "./media/HexRed/HexRed.csv" )