import os
import json
import typing

from src.vot.utils.CStruts import CStruts
from src.utils.CStateMachine import CStateMachine

class CStrutManager:
    def __init__(self) -> None:
        self.state   = None
        self.struts  = None
        self.nodes   = {}
    
    def initStateMachine( self ):
        self.state   = CStateMachine( self.struts, self.txtmtr )
    def readLinkerFile( self, file : str ):
        if os.path.isfile( file ):
            with open( file, "r" ) as pfile :
                links = self.parseLinks( json.load( pfile )[ "Links" ] ) 
                self.struts = CStruts( links, self.nodes )
                self.initStateMachine()
    def parseLinks( self, links : typing.List[ typing.List ] ):
        _links = []
        for link in links:
            link.sort(); link = tuple( link )
            if link not in _links:
                _links.append( link )
        return _links