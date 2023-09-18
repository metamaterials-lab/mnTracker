import cv2
from src.vot.CStructure import CStructure
from src.vot.utils.CNode import CNode
from src.utils.CStateMachine import CStateMachine
from src.vot.CTracker import CTracker
from src.utils.CTexturometer import CTexturometer

def setStructure( points, subpoints, links_path, txtmtr_path ):
    structure = CStructure()
    for i, p in enumerate( points ):
        structure.nodes[ i ] = CNode( *p )
    structure.readLinkerFile( links_path )
    for j, p in enumerate( subpoints ):
        for i, c in enumerate( p ):
            structure.struts.struts[j].subnodes[i].set( *c )
    structure.txtmtr = CTexturometer()
    structure.txtmtr.init( txtmtr_path )
    return structure


def mouse_callaback( e, x, y, *args ):
    if e == cv2.EVENT_LBUTTONDOWN:
        print( x, y )

if __name__ == "__main__":
    points = [
        ( 879, 346 ),
        ( 876, 444 ),
        ( 874, 536 ),
        ( 872, 629 ),
        ( 869, 724 )
    ]
    subpoints = [
        [ ( 877, 374 ), ( 877, 410 ) ],
        [ ( 874, 475 ), ( 874, 509 ) ],
        [ ( 873, 565 ), ( 873, 602 ) ],
        [ ( 871, 657 ), ( 871, 695 ) ]
    ]
    
    structure = setStructure( points, subpoints, r".\config\Links_squarehc.json", r".\media\SquareRed\SquareRed_FORMATED.csv" )
    tracker = CTracker( structure )
    state = CStateMachine( structure.struts, structure.txtmtr )

    cv2.namedWindow( "Image" )
    cv2.setMouseCallback( "Image", mouse_callaback )
    capture = cv2.VideoCapture( "./media/MAH02123 - Trim.MP4" )
    
    ret, frame = capture.read()
    if ret:
        tracker.init( frame )
        structure.draw( frame, False )
        cv2.imshow( "Image", frame )
        cv2.waitKey()

    for c in range( 5000 ):
        if cv2.getWindowProperty( "Image", cv2.WND_PROP_VISIBLE ) < 1: structure.__del__(); exit()
        ret, frame = capture.read()
        if ret:
            #print( f"Num {c}: " )
            state.next()
            tracker.update( frame )
            structure.draw( frame, True )
            cv2.imshow( "Image", frame )
            cv2.waitKey( 16 )
    structure.__del__()