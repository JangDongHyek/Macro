from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
from pathlib import Path
import ctypes
import time

class Keyboard:
    def __init__(self: 'Game'):
        self._status = False
        self.hold_keys = set()
        self.KEY_MAP = {
            # F키
            'esc': 100, 'f1': 101, 'f2': 102, 'f3': 103, 'f4': 104, 'f5': 105,
            'f6': 106, 'f7': 107, 'f8': 108, 'f9': 109, 'f10': 110, 'f11': 111, 'f12': 112,
            # 숫자키
            '1': 201, '2': 202, '3': 203, '4': 204, '5': 205,
            '6': 206, '7': 207, '8': 208, '9': 209, '0': 210,
            # 문자키
            'q': 301, 'w': 302, 'e': 303, 'r': 304, 't': 305,
            'y': 306, 'u': 307, 'i': 308, 'o': 309, 'p': 310,
            'a': 401, 's': 402, 'd': 403, 'f': 404, 'g': 405,
            'h': 406, 'j': 407, 'k': 408, 'l': 409,
            'z': 501, 'x': 502, 'c': 503, 'v': 504, 'b': 505,
            'n': 506, 'm': 507,
            # 방향키
            'up': 709, 'left': 710, 'down': 711, 'right': 712,
            # 기타 조작키
            'shift': 500, 'ctrl': 600, 'alt': 602, 'space': 603, 'enter': 313,
            'insert': 703, 'home': 704, 'pageup': 705,
            'delete': 706, 'end': 707, 'pagedown': 708,
        }

        if self.keyboard == 'dd':
            CURRENT_DIR = Path(__file__).parent
            dll_path = CURRENT_DIR / "dll/keyboard.dll"
            if not dll_path.exists():
                raise RuntimeError("keyboard.dll 이 없습니다.")

            self.ddl = ctypes.windll.LoadLibrary("./keyboard.dll")
            st = self.ddl.DD_btn(0)  # classdd 초기설정
            if st != 1:
                raise RuntimeError("ClassDD에 문제가 생겼습니다.")

    def press(self: 'Game',key, push=0.1):
        key_name = key.lower()
        if key_name not in self.KEY_MAP:
            raise ValueError(f"키 '{key_name}'는 정의되어 있지 않습니다.")

        keycode = self.KEY_MAP[key_name]

        self.ddl.DD_key(keycode, 1)
        time.sleep(push)
        self.ddl.DD_key(keycode, 2)

    def hold(self: 'Game',key):
        key_name = key.lower()
        if key_name not in self.KEY_MAP:
            raise ValueError(f"키 '{key_name}'는 정의되어 있지 않습니다.")

        if key_name in self.hold_keys:
            return  # 이미 눌려 있으면 무시

        keycode = self.KEY_MAP[key_name]
        self.ddl.DD_key(keycode, 1)
        self.hold_keys.add(key_name)

    def release(self: 'Game',key):
        key_name = key.lower()
        if key_name not in self.KEY_MAP:
            raise ValueError(f"키 '{key_name}'는 정의되어 있지 않습니다.")

        keycode = self.KEY_MAP[key_name]
        self.ddl.DD_key(keycode, 2)
        self.hold_keys.discard(key_name)

    def releaseAll(self: 'Game'):
        for key in ['left','up','right','down'] :
            keycode = self.KEY_MAP[key]
            self.ddl.DD_key(keycode, 2)
            time.sleep(0.01)

        self.hold_keys.clear()