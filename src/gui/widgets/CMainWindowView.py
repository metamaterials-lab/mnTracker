from PyQt5 import QtWidgets, QtCore

from src.gui.widgets.CVideo import CVideo
from src.gui.widgets.CPanel import CPanel
from src.gui.widgets.CPlot  import CPlot

class CMainWindowView( object ):
    def setupUI(self, MainWindow : QtWidgets.QMainWindow ):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1450, 480)
        #MainWindow.resize(1000, 480)
        # Central Widget
        self.centralwidget  = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.setup()
        # MainWindow Build
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # Connect Widgets
        self._connections()

    def setup(self):
        self._setupCentralWidget( self.centralwidget )

    def _setupCentralWidget(self, widget : QtWidgets.QWidget ):
        aflag   = QtCore.Qt.AlignmentFlag
        mlayout = QtWidgets.QHBoxLayout()

        self.plot  = CPlot( widget )
        self.plot.setMinimumWidth( 500 )
        mlayout.addWidget( self.plot, alignment=aflag.AlignCenter, stretch=1 )

        self.video = CVideo( widget )
        mlayout.addWidget( self.video, alignment=aflag.AlignLeft | aflag.AlignTop )

        self.panel = CPanel( widget )
        self.panel.setMaximumWidth( 350 )
        mlayout.addWidget( self.panel, alignment=aflag.AlignLeft )

        widget.setLayout( mlayout )

    def _connections( self ):
        self.panel.structure = self.video.structure
        self.video._mousePressEventCallback = self.panel.updateNodes
        self.video.structure.txtmtr = self.plot.texturometer
        self.video.structure.initStateMachine()
        