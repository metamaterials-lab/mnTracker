from PyQt5 import QtWidgets

from src.gui.widgets.CPlotView import CPlotView

class CPlot( QtWidgets.QWidget, CPlotView ):
    def __init__(self, parent = None, *args ) -> None:
        super( QtWidgets.QWidget, self ).__init__(parent, *args)
        super( CPlotView, self ).__init__()

        self.setupUI( self )
        self.setCallbacks()

    def setCallbacks(self):
        self.file_button.clicked.connect( self._browseClickCallback )