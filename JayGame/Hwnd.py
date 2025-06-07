from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
import ctypes
import win32con
import win32gui


class Hwnd :
    def __init__(self : 'Game'):
        self._hwnd = self.setHwnd()
        if not self._hwnd:
            raise RuntimeError(f"❌ '{self.title}' 창을 찾을 수 없습니다.")

        self.ActiveHwnd()
        self._region = self.getClientRegion()
        self._hwnd_size = self.getClientSize()

    def setHwnd(self : 'Game'):
        def callback(hwnd, result):
            if win32gui.IsWindowVisible(hwnd) and self.title.lower() in win32gui.GetWindowText(hwnd).lower():
                result.append(hwnd)

        result = []
        win32gui.EnumWindows(callback, result)
        return result[0] if result else None

    def ActiveHwnd(self : 'Game'):
        # 최소화 상태면 복원
        win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)

        # 포그라운드로 올림
        win32gui.SetForegroundWindow(self._hwnd)

        # 항상 위로 설정 (SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)
        ctypes.windll.user32.SetWindowPos(
            self._hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
            0x0001 | 0x0002  # SWP_NOSIZE | SWP_NOMOVE
        )

        # 항상 위 해제 (원상복구)
        ctypes.windll.user32.SetWindowPos(
            self._hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
            0x0001 | 0x0002
        )

    def getClientRegion(self: 'Game'):
        cx, cy, cw, ch = win32gui.GetClientRect(self._hwnd)
        abs_cx, abs_cy = win32gui.ClientToScreen(self._hwnd, (cx, cy))
        abs_cx1, abs_cy1 = win32gui.ClientToScreen(self._hwnd, (cw, ch))

        return abs_cx, abs_cy, abs_cx1, abs_cy1

    def getClientSize(self : 'Game'):
        rect = win32gui.GetClientRect(self._hwnd)  # (left, top, right, bottom)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return width, height