import numpy as np

from PyQt5 import QtCore, QtWidgets, QtGui

from src.utils.CZoom import CZoom
from src.utils.CLine import CLine
from src.gui.widgets.CScaleDialogView import CScaleDialogView

class CScaleDialog( QtWidgets.QDialog, CScaleDialogView ):
    def __init__(self, parent=None, frame : np.ndarray = None):
        super( QtWidgets.QDialog, self ).__init__()
        self.line = CLine( ( 0, parent.cap.ssize[1] ) )
        self.parent = parent
        self.cframe = frame
        self.setupUI( self )
        self._setZoom()
        self._setFrame( frame )
        
        self.setCallbacks()
        self.setTimers()
        self.setMouseEvents()
    def setCallbacks(self):
        self.buttons.accepted.connect( self.acceptedCallback )
        self.buttons.rejected.connect( self.rejectedCallback )
    def acceptedCallback(self):
        self._acceptedCallback()
        self.close()
    def rejectedCallback(self):
        self._rejectedCallback()
        self.close()

    def run( self ):
        frame = self.line.draw( self.cframe )
        self._setFrame( frame )

    def setTimers( self ):
        self.cap_timer = QtCore.QTimer()
        self.cap_timer.setInterval( int( 1000 / 30 ) )
        self.cap_timer.timeout.connect( self.run )
        self.cap_timer.start()

    def setMouseEvents( self ):
        self.frame.wheelEvent = self._wheelEvent
        self.frame.mousePressEvent = self._mousePressEvent

    def _wheelEvent( self, e: QtGui.QWheelEvent ):
        if isinstance( self.zoom, CZoom ):
            x, y = self.zoom.getPos( e.pos().x(), e.pos().y() )
            p    = e.angleDelta().y()
            self.zoom.mouse_callback( x, y, p )

    def _mousePressEvent( self, e: QtGui.QMouseEvent ):
        if isinstance( self.zoom, CZoom ):
            x, y = self.zoom.getPos( e.pos().x(), e.pos().y() )
            if e.buttons() & QtCore.Qt.MouseButton.LeftButton:
                self.line.set( x, y )
            elif e.buttons() & QtCore.Qt.MouseButton.MidButton:
                self.line.next()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.cap_timer.stop()
        return super().closeEvent(a0)
        
def Dialog( parent:QtWidgets.QWidget=None, frame:np.ndarray=None ):
    dialog = CScaleDialog( parent=parent, frame=frame )
    dialog.exec()
    return dialog.length, dialog.origin
    