import os
import re
import json
import sys

sys.path.append( os.path.abspath( "." ) )
from src import CONFIG_FILE

results_path = CONFIG_FILE.get( "RESULTS_PATH", "." )

class Creator:
    def __init__( self, results_file : str, config_file : str ):
        with open( results_file, "r" ) as pfile:
            self.headers = pfile.readline()[0:-1]
        with open( config_file, "r" ) as pfile:
            self.config = json.load( pfile ).get( "Links", [] )
        self.nodes = self.genNodeMap()
        self.subnodes = self.genSubNodeMap()
        self.struts = self.index_struts()
        self.superIndex = self.index_nodes()

    def genNodeMap( self ) -> dict:
        nodes = {}
        for i, h in enumerate( self.headers.split( "," ) ):
            if len( re.findall( "M[^a-zA-Z]X", h ) ):
                n = int(h[1:-1])
                nodes[ n ] = ( i, i + 1 )
        return nodes

    def genSubNodeMap( self ) -> dict:
        subnodes = {}
        for i, h in enumerate( self.headers.split( "," ) ):
            if len( re.findall( "S[^a-zA-Z]*X", h ) ):
                n, A, B = tuple( re.findall( "(\d+)", h ) )
                subnodes[ f"{A},{B},{n}" ] = ( i, i + 1 )
        return subnodes
    
    def index_struts( self ):
        struts = []
        strut  = []
        for A, B in self.config:
            if len( strut ):
                if not strut[ -1 ] == A: struts.append( strut ); strut = []; strut.append( A )
            else: strut.append( A )
            strut.append( B )
        return struts

    def index_nodes( self ):
        super_index = []
        for strut in self.struts:
            B = None
            index = []
            for i in range( len( strut ) - 1 ):
                A = self.nodes.get( strut[i], None )
                B = self.nodes.get( strut[i+1], None )
                if isinstance( A, tuple ) and isinstance( B, tuple ):
                    index.append( A )
                    name = f"{strut[i]},{strut[i + 1]}"
                    for sname in list( self.subnodes.keys() ):
                        if len( re.findall( f"^{name}", sname ) ):
                            index.append( self.subnodes.get( sname ) )
                    index.append( B )
            if len(index):
                nindex = [ index[0] ]
                for i in range( 1, len( index ) ):
                    if not index[ i - 1 ] == index[ i ]: nindex.append( index[i] )
                super_index.append( nindex )
        return super_index

if __name__ == "__main__":
    table_path = r".\results\Results_2023-09-18_2.csv"
    links_path = r".\config\example.json"
    
    creator = Creator(
        table_path,
        links_path
    )
    TABLE_NAME = "TABLE"
    PROGRAM = f"{TABLE_NAME} = readmatrix( \"{os.path.abspath(table_path)}\" );\nfigure;\nhold on;\naxis equal;\n\n"
    for i, line in enumerate( creator.superIndex ):
        xline = ""
        yline = ""
        for x, y in line:
            xline = xline + f"{x+1},"
            yline = yline + f"{y+1},"
        txt_x = f"line{i}_x = {TABLE_NAME}( :, [{xline[0:-1]}] );\n"
        txt_y = f"line{i}_y = {TABLE_NAME}( :, [{yline[0:-1]}] );\n"
        plt   = f"h{i} = plot( line{i}_x(1,:), line{i}_y(1,:), \"b\" );\n"
        plt   = plt + f"h{i}.XDataSource = \"line{i}_x(t,:)\";\n"
        plt   = plt + f"h{i}.YDataSource = \"line{i}_y(t,:)\";\n\n"
        PROGRAM = PROGRAM + txt_x + txt_y + plt
    PROGRAM = PROGRAM + f"for t = 1 : size( {TABLE_NAME}, 1 )\n"
    for i, _ in enumerate( creator.superIndex ):
        PROGRAM = PROGRAM + f"\trefreshdata(h{i},\"caller\");\n"
    PROGRAM = PROGRAM + "end\n"
    with open( os.path.join( results_path, "matlab_plotter.m" ), "w" ) as pFile:
        pFile.write( PROGRAM )