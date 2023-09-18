import os
import numpy as np

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget

from src.utils.CZoom import CZoom
from src.utils.CVideoCapture import CVideoCapture
from src.vot.CStructure import CStructure
from src.vot.CTracker import CTracker
from src.gui.widgets.CScaleDialog import Dialog

def gen_cover( size : tuple[ int, int ] = ( 640, 480 ) ) -> QtGui.QImage:
    frame = np.zeros( [ size[1], size[0], 3 ] )
    return QtGui.QImage( frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format.Format_RGB888 )

class CVideoView( object ):
    def __init__( self ):
        # Parameters
        self.fix_size  = ( 640, 480 )
        self.file_name = ""
        self.active    = False
        # Objects
        self.cframe    = None
        self.parent    = None
        self.cap       = None
        self.zoom      = None
        self.structure = CStructure()
        self.tracker   = CTracker( self.structure )

    def setupUI( self, parent : QWidget ):
        # Layout
        aflag  = QtCore.Qt.AlignmentFlag
        layout = QtWidgets.QVBoxLayout()
        # Widget: Frame
        self.cover = gen_cover( parent.fix_size )
        self.frame = QtWidgets.QLabel()
        self._setFrame()
        layout.addWidget( self.frame, alignment=aflag.AlignTop | aflag.AlignCenter )
        # Widget: File browser
        self.file_label  = QtWidgets.QLabel()
        self.file_label.setMinimumSize( 60, 8 )
        self.file_button = QtWidgets.QPushButton()
        self.file_button.setText( "Browse" )
        self.play_button = QtWidgets.QPushButton()
        self.play_button.setText( "Start" )
        self.scale_button = QtWidgets.QPushButton()
        self.scale_button.setText( "Scale" )
        _layout = QtWidgets.QHBoxLayout()
        _layout.addWidget( QtWidgets.QLabel( "File:" ), alignment=aflag.AlignCenter )
        _layout.addWidget( self.file_label, alignment=aflag.AlignCenter )
        _layout.addWidget( self.file_button, alignment=aflag.AlignCenter, stretch=1 )
        _layout.addWidget( self.play_button, alignment=aflag.AlignCenter )
        _layout.addWidget( self.scale_button, alignment=aflag.AlignCenter )
        layout.addLayout( _layout, 0 )
        # Layout assembly
        parent.setLayout( layout )

    def _setVideoCapture( self ):
        if self.file_name:
            self.cap = CVideoCapture( self.file_name, self.fix_size )
            self.zoom = CZoom( self.cap )
            self.cap._draw = self._draw
            self._setFrame( self.cap.next() )
        else:
            self.cap  = None
            self.zoom = None
            self._setFrame()

    def _setFrame( self, frame : np.ndarray = None ):
        if isinstance( frame, type( None ) ):
            self.frame.setPixmap( QtGui.QPixmap.fromImage( self.cover ) )
        else:
            img = QtGui.QImage( frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format.Format_RGB888 )
            self.frame.setPixmap( QtGui.QPixmap.fromImage( img ) )

    def _draw( self, I : np.ndarray ):
        if self.active:
            self.tracker.update( I )
        else:
            self.cframe = np.copy( I )
        self.structure.draw( I, self.active )
        I = self.zoom.crop( I )
        return I

    def _playClickCallback( self ):
        if self.active: self.active = False; self.play_button.setText( "Start" )
        else:           self.active = True ; self.play_button.setText( "Stop"  ); self.parent.unsetMouseEvents()

    def _browseClickCallback( self ):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Video",
            ".",
            "Video Files (*.mp4 *.mov *.wmv *.avi *.flv)"
        )
        self.file_label.setText( os.path.basename( filename ) )
        self.file_name = filename
        self._setVideoCapture()

    def _scaleClickCallback( self ):
        if isinstance( self.cap, CVideoCapture ):
            scale, origin = Dialog( self.parent, self.cframe )
            if isinstance( scale, float ):
                self.structure.scale    = scale
                self.structure.origin   = origin