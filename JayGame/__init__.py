import dxcam

from .Draw import Draw
from .Hwnd import Hwnd
from .Image import Image
from .Keyboard import Keyboard
from .Lib import Lib
from .Mouse import Mouse
from .Pixel import Pixel
from .Thread import Thread
from .Util import Util
from .Yolo import Yolo

import ctypes

class Game(Draw,Hwnd,Image,Keyboard,Lib,Mouse,Pixel,Thread,Util,Yolo):
    def __init__(self, title):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            raise RuntimeError("관리자 권한이 아닙니다.")

        self._yolo_resize = (640, 640)
        self.keyboard = "arduino"  # dd or arduino
        self.start_key = "f5"
        self.end_key = "f6"
        self.title = title

        self._camera = dxcam.create(output_color="BGR")
        Draw.__init__(self)
        Hwnd.__init__(self)
        Image.__init__(self)
        Keyboard.__init__(self)
        Lib.__init__(self)
        Mouse.__init__(self)
        Pixel.__init__(self)
        Thread.__init__(self)
        Util.__init__(self)
        Yolo.__init__(self)




