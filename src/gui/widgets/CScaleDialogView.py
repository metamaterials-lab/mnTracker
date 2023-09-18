import cv2
import numpy as np

from PyQt5 import QtCore, QtWidgets, QtGui

from src.utils.CZoom import CZoom

class CScaleDialogView:
    def __init__(self) -> None:
        self.length = None
        self.origin = None
        self.parent = None
        self.zoom   = None
        self.line   = None
    def setupUI(self, parent : QtWidgets.QWidget ) -> None:
        parent.setWindowTitle( "Scale Selector" )
        # Layout
        aflag  = QtCore.Qt.AlignmentFlag
        layout = QtWidgets.QVBoxLayout()

        self.frame = QtWidgets.QLabel()
        layout.addWidget( self.frame, alignment=aflag.AlignCenter )
        
        _layout = QtWidgets.QHBoxLayout()
        self.scale = QtWidgets.QLineEdit()
        self.scale.setValidator( QtGui.QDoubleValidator( 0.0, 300.00, 2 ) )
        OK           = QtWidgets.QDialogButtonBox.StandardButton.Ok
        CANCEL       = QtWidgets.QDialogButtonBox.StandardButton.Cancel
        self.buttons = QtWidgets.QDialogButtonBox( OK | CANCEL )
        _layout.addWidget( QtWidgets.QLabel( "Line length [mm]" ), alignment=aflag.AlignCenter )
        _layout.addWidget( self.scale, alignment=aflag.AlignCenter )
        _layout.addWidget( self.buttons, stretch=1, alignment=aflag.AlignCenter )
        layout.addLayout( _layout )

        parent.setLayout( layout )
        QtCore.QMetaObject.connectSlotsByName( parent )
    def _setZoom( self ):
        self.zoom = CZoom( self.parent.cap )
    def _setFrame( self, I : np.ndarray = None ): 
        frame = self.zoom.crop( I )
        frame = cv2.resize( frame, self.parent.fix_size )
        img = QtGui.QImage( frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format.Format_RGB888 )
        self.frame.setPixmap( QtGui.QPixmap.fromImage( img ) )
    def _acceptedCallback(self):
        num = self.scale.text()
        if num:
            num = float( num )
            length = self.line.length()
            if num > 0 and isinstance( length, float ):
                self.length = num / length
            self.origin = self.line.origin()
    def _rejectedCallback(self):
        pass