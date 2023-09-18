
from PyQt5 import QtWidgets, QtCore, QtGui

from src.vot.CStructure import CStructure

class CListWidget( QtWidgets.QListWidget ):
    def __init__(self,parent = None):
        super().__init__(parent)
    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(e)
        if not self.indexAt(e.pos()).isValid():
            self.clearSelection()

class CPanelView( object ):
    def __init__( self ) -> None:
        # Parameters
        
        # Objects
        self.idx        = 0
        self.structure  = None

    def setupUI( self, parent : QtWidgets.QWidget ):
        aflag = QtCore.Qt.AlignmentFlag
        # Layout Declaration
        layout = QtWidgets.QVBoxLayout()

        # Load / Dump
        self.load_button = QtWidgets.QPushButton()
        self.load_button.setText( "Load" )
        _layout = QtWidgets.QHBoxLayout()
        _layout.addWidget( self.load_button, alignment=aflag.AlignBottom | aflag.AlignRight )
        layout.addLayout( _layout )

        # List Box
        self.nodes_list = QtWidgets.QListWidget()
        self.lines_list = CListWidget()
        _layout = QtWidgets.QGridLayout()
        _layout.addWidget( QtWidgets.QLabel( "Nodes List" ), 0, 0, alignment=aflag.AlignBottom | aflag.AlignLeft )
        _layout.addWidget( QtWidgets.QLabel( "Lines List" ), 0, 2, alignment=aflag.AlignBottom | aflag.AlignLeft )
        _layout.addWidget( self.nodes_list, 1,0,1,2 )
        _layout.addWidget( self.lines_list, 1,2,1,2 )
        layout.addLayout( _layout )

        # Build Layout
        parent.setLayout( layout )

    def _updateNodesList( self, N : int ):
        self.nodes_list.blockSignals( True )
        self.nodes_list.clear()
        for n in range( N + 1 ):
            self.nodes_list.addItem( str( n ) )
        self.nodes_list.blockSignals( False )

    def _updateLinksList( self ):
        if isinstance( self.structure, CStructure ):
            for A, B in self.structure.struts:
                self.lines_list.addItem( f"( {A}, {B} )" )

    def _updateNodesIdx( self ):
        self.nodes_list.blockSignals( True )
        self.nodes_list.setCurrentRow( self.idx )
        self.nodes_list.blockSignals( False )

    def _nodesChangedCallback(self, idx : int ):
        self.idx = idx
        if isinstance( self.structure, CStructure ):
            self.structure.setIdx( idx )
    
    def _linesChangedCallback(self ):
        idx = [ i.row() for i in self.lines_list.selectedIndexes() ]
        if isinstance( self.structure, CStructure ):
            i = idx[0] if len( idx ) else None
            self.structure.setSubIdx( i )
    
    def _loadClickedCallback( self ):
        if isinstance( self.structure, CStructure ):
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Select Config File",
                ".",
                "JSON (*.json)"
            )
            self.structure.readLinkerFile( filename )
            self._updateLinksList()