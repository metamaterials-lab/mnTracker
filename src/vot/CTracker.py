import numpy as np

from src.vot.CStructure import CStructure
from src.vot.CKCF import CKCF

class CTracker:
    def __init__(self, structure : CStructure) -> None:
        self.trackers  = None
        self.structure = structure
    def init(self, img : np.ndarray) -> None:
        self.trackers = [ CKCF( img, roi ) for roi in self.structure.dump() ]
    def update( self, img : np.ndarray ) -> None:
        if  isinstance( self.trackers, type( None ) ):
            self.init( img )
        else:
            rois = []
            for kcf in self.trackers:
                kcf.update( img )
                rois.append( kcf.roi.pos )
            self.structure.load( rois )
            self.structure.timestep()