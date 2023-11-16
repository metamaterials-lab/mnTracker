from PyQt5 import QtWidgets, QtCore, QtGui

from src import CONFIG_FILE
from src.gui.widgets.CVideoView import CVideoView
from src.utils.CZoom import CZoom
from src.utils.CVideoCapture import CVideoCapture

FPS = CONFIG_FILE.get( "FRAMES_PER_SECOND", 30 )

class CVideo( QtWidgets.QWidget, CVideoView ):
    def __init__(self, parent = None,  *args ) -> None:
        super( QtWidgets.QWidget, self ).__init__(parent)
        super( CVideoView, self ).__init__()
        # Variables
        self.parent = self
        
        # Setup User Interface
        self.setupUI( self )
        self.setCallbacks()
        self.setTimers()
        self.setMouseEvents()

    def run( self ):
        #if self.active:
        if isinstance( self.cap, CVideoCapture ):
            # TODO: CATCH ERROR StopIteration
            try:
                frame = self.cap.next( self.active )
                self._setFrame( frame )
            except StopIteration:
                if self.active: self._playClickCallback()
        else:
            self._setFrame()

    def setTimers( self ):
        self.cap_timer = QtCore.QTimer()
        self.cap_timer.setInterval( int( 1000 / FPS ) )
        self.cap_timer.timeout.connect( self.run )
        self.cap_timer.start()

    def setCallbacks( self ):
        self.file_button.clicked.connect( self._browseClickCallback )
        self.play_button.clicked.connect( self._playClickCallback )
        self.scale_button.clicked.connect( self._scaleClickCallback )

    def setMouseEvents( self ):
        self.frame.wheelEvent = self._wheelEvent
        self.frame.mousePressEvent = self._mousePressEvent

    def unsetMouseEvents( self ):
        #self.frame.wheelEvent = lambda _ : None
        self.frame.mousePressEvent = lambda _ : None

    def _wheelEvent( self, e: QtGui.QWheelEvent ):
        if isinstance( self.zoom, CZoom ):
            x, y = self.zoom.getPos( e.pos().x(), e.pos().y() )
            p    = e.angleDelta().y()
            self.zoom.mouse_callback( x, y, p )

    def _mousePressEvent( self, e: QtGui.QMouseEvent ):
        if isinstance( self.zoom, CZoom ):
            x, y = self.zoom.getPos( e.pos().x(), e.pos().y() )
            if e.buttons() & QtCore.Qt.MouseButton.LeftButton:
                self.structure.get().set( x, y )
            elif e.buttons() & QtCore.Qt.MouseButton.MidButton:
                self.structure.next()
            self._mousePressEventCallback( e )

    def _mousePressEventCallback( self, *_ ):
        pass


