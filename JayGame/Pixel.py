from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
import math


class Pixel:
    def __init__(self: 'Game'):
        pass

    def getPixel(self: 'Game', position, image=None):
        if image is None:
            image = self._frame  # OpenCV 이미지 (NumPy 배열)

        x, y = position

        # 높이, 너비 가져오기
        height, width = image.shape[:2]

        if x < 0 or y < 0 or x >= width or y >= height:
            raise ValueError("좌표가 이미지 범위를 벗어났습니다.")

        # OpenCV는 BGR 순서
        b, g, r = image[y, x]
        return (r, g, b)  # (R, G, B)로 반환

    def pixelSearch(self: 'Game', target_rgb, pos,threshold = 0.85):
        image = self._frame
        height, width = image.shape[:2]

        x1, y1, x2, y2 = pos

        # 기본값 처리
        if x2 is None:
            x2 = width
        if y2 is None:
            y2 = height

        # 범위 보정
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(width, x2), min(height, y2)

        for y in range(y1, y2):
            for x in range(x1, x2):
                pixel = self.getPixel((x, y),image)
                if self.comparePixel(pixel,target_rgb,threshold) :
                    return x, y

        return None

    def comparePixel(self: 'Game',rgb1,rgb2,threshold=0.85):
        # 예: rgb1 = (255, 255, 255), rgb2 = (200, 200, 200)
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2

        distance = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
        max_distance = math.sqrt(255 ** 2 * 3)  # ≈ 441.67

        similarity = 1 - (distance / max_distance)
        return similarity >= threshold