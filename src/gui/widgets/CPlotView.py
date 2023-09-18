import os
import typing
import matplotlib
matplotlib.use( "Qt5Agg" )

from PyQt5 import QtWidgets, QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from src.utils.CTexturometer import CTexturometer

class Canvas( FigureCanvasQTAgg ):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        fig = Figure( figsize=(width, height), dpi=dpi )
        fig.tight_layout()
        self.axes = fig.add_subplot(111)
        super(Canvas, self).__init__(fig)
    def plot(self, x : typing.List[ float ], y : typing.List[ float ], xlim : typing.Tuple[ float, float ], ylim : typing.Tuple[ float, float ] ):
        self.axes.cla()
        self.axes.set_xlim( xlim )
        self.axes.set_ylim( ylim )
        self.axes.plot( x, y )
        self.axes.grid(True)
        
        self.draw()

class CPlotView(object):
    def __init__( self ) -> None:
        self.texturometer = CTexturometer()
    def setupUI( self, parent : QtWidgets.QWidget ):
        aflag = QtCore.Qt.AlignmentFlag

        layout = QtWidgets.QVBoxLayout()
        
        self.canvas = Canvas( parent )
        layout.addWidget( self.canvas, stretch=1, alignment=aflag.AlignTop | aflag.AlignLeft )

        # Widget: File browser
        self.file_label  = QtWidgets.QLabel()
        self.file_label.setMinimumSize( 60, 8 )
        self.file_button = QtWidgets.QPushButton()
        self.file_button.setText( "Browse" )
        _layout = QtWidgets.QHBoxLayout()
        _layout.addWidget( QtWidgets.QLabel( "File:" ), alignment=aflag.AlignCenter )
        _layout.addWidget( self.file_label, alignment=aflag.AlignCenter )
        _layout.addWidget( self.file_button, alignment=aflag.AlignCenter, stretch=1 )
        layout.addLayout( _layout, 0 )

        parent.setLayout( layout )

    def _browseClickCallback( self ):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Video",
            ".",
            "Tabular data (*.csv)"
        )
        self.file_label.setText( os.path.basename( filename ) )
        self.texturometer.init( filename )
        self.texturometer._plot = self.canvas.plot