from src import CONFIG_FILE

FPS = CONFIG_FILE.get( "FRAMES_PER_SECOND", 30 )

class CTimer:
    TIMEMS = 0
    def __init__(self) -> None:
        self.T        = int( 1000/FPS )
    def timeStep(self) -> int:
        CTimer.TIMEMS += self.T
        return CTimer.TIMEMS