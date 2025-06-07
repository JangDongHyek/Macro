from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
import time
import dxcam


class Util:
    def __init__(self: 'Game'):
        self._fps = 60
        self._delay = 1
        self._last_loop = 0
        self._camera_state = False
        pass

    def getTime(self: 'Game',bool=False):
        if (bool):
            return time.strftime('%Y%m%d %H%M%S')
        else:
            return time.strftime('%Y-%m-%d_%H:%M:%S')

    def compareTime(self: 'Game',value, elapse):
        if not value:
            return False

        if time.time() - value >= elapse:
            return True
        return False

    def timeDelay(self : 'Game'):
        now = time.perf_counter()
        delay = max(0, (1 / self._fps) - (now - getattr(self, "_last_loop", 0)))
        self._delay = delay
        time.sleep(delay)

        self._last_loop = time.perf_counter()



    def cameraStart(self : 'Game'):
        self._camera.start(self._region)
        self._camera_state = True

    def cameraStop(self : 'Game'):
        self._camera.stop()
        self._camera_state = False
