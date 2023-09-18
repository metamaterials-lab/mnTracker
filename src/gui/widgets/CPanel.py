import typing

from PyQt5 import QtWidgets, QtGui, QtCore

from src.vot.CStructure import CStructure
from src.gui.widgets.CPanelView import CPanelView

class CPanel( QtWidgets.QWidget, CPanelView ):
    def __init__(self, parent = None, *args ) -> None:
        super( QtWidgets.QWidget, self ).__init__(parent, *args)
        super( CPanelView, self ).__init__()
        
        # Setup User Interface
        self.setupUI( self )
        self.setCallbacks()

    def setCallbacks( self ):
        self.load_button.clicked.connect( self._loadClickedCallback )
        self.nodes_list.currentRowChanged.connect( self._nodesChangedCallback )
        self.lines_list.itemSelectionChanged.connect( self._linesChangedCallback )

    def updateNodes( self, e : QtGui.QMouseEvent ):
        if isinstance( self.structure, CStructure ):
            if not isinstance( self.structure.struts, type( None ) ):
                if isinstance( self.structure.struts.idx, int ):
                    return
            if e.buttons() & QtCore.Qt.MouseButton.LeftButton:
                self._updateNodesList( self.structure.idx_max )
                self._updateNodesIdx()
            elif e.buttons() & QtCore.Qt.MouseButton.MidButton:
                if self.idx < self.structure.idx_max:
                    self._updateNodesIdx()
                    self.idx += 1
    