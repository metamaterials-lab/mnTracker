from src.utils.CTexturometer import CTexturometer
from src.vot.utils.CStruts import CStruts

class CStateMachine:
    def __init__( self, struts : CStruts, txtmtr : CTexturometer ) -> None:
        self.struts = struts
        self.txtmtr = txtmtr
        self._gen   = self.gen()

    def next(self):
        next( self._gen )

    def gen(self):
        while True:
            if self.txtmtr.diff.peak: break
            yield None
        while True:
            for strut in self.struts.struts:
                if bool( strut ):
                    if strut.diff_ang.peak: strut.state.buckling = True
                        #print( f"Strut {i}: Buckled" )
            yield None
                    