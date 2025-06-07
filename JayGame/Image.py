from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
import cv2
import numpy as np
import os

class Image:
    def __init__(self: 'Game'):
        self._frame = None

    def screenshot(self : "Game",name):
        if self._frame is not None:
            os.makedirs(os.path.dirname(name), exist_ok=True)
            cv2.imwrite(name + ".jpg", self._frame)
        else:
            raise ValueError("프레임이 없습니다.")

    def imageSearch(self: 'Game', img_path, image=None, confidence=0.75):
        # 1. 템플릿 이미지 로드 (한글 경로 지원)
        img_array = np.fromfile(img_path, np.uint8)
        template = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if template is None:
            raise ValueError("템플릿 이미지를 읽을 수 없습니다.")

        # 2. 대상 이미지 준비
        if image is not None:
            # image는 NumPy (BGR)로 받는다고 가정
            haystack = image
        else:
            haystack = self._frame  # self.screen은 NumPy (BGR)임

        if haystack is None:
            raise ValueError("대상 이미지가 비어 있습니다.")

        # 3. 템플릿 매칭
        result = cv2.matchTemplate(haystack, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            h, w = template.shape[:2]
            return max_loc[0], max_loc[1], w, h  # left, top, width, height
        else:
            return None