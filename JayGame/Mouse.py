from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
import win32api
import win32gui



class Mouse:
    def __init__(self: 'Game'):
        pass

    def getMousePosition(self: 'Game'):
        # 현재 마우스 절대 좌표
        x, y = win32api.GetCursorPos()

        # hwnd 기준 상대 좌표로 변환
        client_x, client_y = win32gui.ScreenToClient(self._hwnd, (x, y))

        return client_x, client_y