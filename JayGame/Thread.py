from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
import threading
import keyboard
import time
from collections.abc import Callable
import onnxruntime


class Thread:
    def __init__(self: 'Game'):
        self._threads = {}         # ID → Thread 객체
        self._flags = {}           # ID → 실행 플래그

    def onnxSearch(self: 'Game',id):
        if id not in self._onnx_session:
            session = onnxruntime.InferenceSession(
                f"JayGame/yolo/{id}.onnx",  # ← id 기반 경로
                providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
            )
            input_name = session.get_inputs()[0].name
            self._onnx_session[id] = {
                "session": session,
                "input_name": input_name
            }

        if self._frame is not None:
            img = self.preprocess()
            output = self._onnx_session[id]["session"].run(
                None,
                {self._onnx_session[id]["input_name"]: img}
            )
            xy = self.postprocess(output)
            self._onnx[id] = xy

    def mainKey(self:'Game'):
        while True :
            if keyboard.is_pressed(self.start_key):
                if not self._status:
                    print("🟢 매크로 시작 (F5)")
                    self._status = True
                    time.sleep(0.3)  # 중복 방지

            if keyboard.is_pressed(self.end_key):
                if self._status:
                    print("🔴 매크로 중지 (F6)")
                    self._status = False
                    time.sleep(0.3)

            if keyboard.is_pressed('print screen'):
                print("📸 스크린샷 촬영")
                self.screenshot("./res/screenshot/" + self.getTime(True))
                time.sleep(0.3)  # 중복 방지
            time.sleep(self._delay)


    def threadStart(self: 'Game', id: str, target: Callable, args: tuple = (), kwargs: dict = {}):
        # 이미 실행 중이면 무시
        if id in self._threads and self._threads[id].is_alive():
            print(f"🟡 Thread '{id}' 이미 실행 중")
            return

        # 실행 플래그 ON
        self._flags[id] = True

        def wrapper(*args, **kwargs):
            print(f"🟢 Thread '{id}' 시작")
            while self._flags.get(id, False):
                target(*args, **kwargs)
                time.sleep(self._delay)
            print(f"🛑 Thread '{id}' 종료")

        thread = threading.Thread(target=wrapper, args=args, kwargs=kwargs, daemon=True)
        self._threads[id] = thread
        thread.start()

    def threadStop(self: 'Game', id: str):
        if id in self._flags:
            self._flags[id] = False

    def threadAllStop(self: 'Game'):
        for id in list(self._flags.keys()):
            if id == "mainKey":
                continue
            self._flags[id] = False