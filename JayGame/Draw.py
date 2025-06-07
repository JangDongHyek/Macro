from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
import time
import cv2

class Draw:
    def __init__(self: 'Game'):
        self._draw_dynamic = {}

        self._draw_color_cache = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
            'yellow': (0, 255, 255),
            'magenta': (255, 0, 255),
            'cyan': (255, 255, 0),
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'orange': (0, 165, 255),
        }

    def drawFrame(self: 'Game',frame):
        now = time.time()
        to_delete = []

        for draw_id, item in self._draw_dynamic.items():
            draw_type, expire_time, *args = item
            if expire_time is not None and expire_time < now:
                to_delete.append(draw_id)
                continue
            if draw_type == 'rect':
                pt1, pt2, color, thickness = args
                cv2.rectangle(frame, pt1, pt2, color, thickness)
            elif draw_type == 'circle':
                center, radius, color, thickness = args
                cv2.circle(frame, center, radius, color, thickness)
            elif draw_type == 'text':
                text, org, color, scale_text, thickness = args
                cv2.putText(frame, text, org, cv2.FONT_HERSHEY_SIMPLEX, scale_text, color, thickness)
            elif draw_type == 'line':
                pt1, pt2, color, thickness = args
                cv2.line(frame, pt1, pt2, color, thickness)

        for draw_id in to_delete:
            del self._draw_dynamic[draw_id]


    def drawRect(self: 'Game', draw_id, pt1, pt2, color="green", thickness=2, duration=None):
        color = self._draw_color_cache[color]
        expire_time = None if duration is None else time.time() + duration
        self._draw_dynamic[draw_id] = ('rect', expire_time, pt1, pt2, color, thickness)

    def drawCircle(self: 'Game', draw_id, center, radius=20, color="green", thickness=2, duration=None):
        color = self._draw_color_cache[color]
        expire_time = None if duration is None else time.time() + duration
        self._draw_dynamic[draw_id] = ('circle', expire_time, center, radius, color, thickness)

    def drawText(self: 'Game', draw_id, text, org, color="green", scale=0.6, thickness=1, duration=None):
        color = self._draw_color_cache[color]
        expire_time = None if duration is None else time.time() + duration
        self._draw_dynamic[draw_id] = ('text', expire_time, text, org, color, scale, thickness)

    def drawLine(self: 'Game',draw_id, pt1, pt2, color="green", thickness=1,duration=None):
        color = self._draw_color_cache[color]
        expire_time = None if duration is None else time.time() + duration
        self._draw_dynamic[draw_id] = ('line',expire_time, pt1, pt2, color, thickness)

    def deleteDraw(self: 'Game', draw_id):
        if draw_id in self._draw_dynamic:
            del self._draw_dynamic[draw_id]


