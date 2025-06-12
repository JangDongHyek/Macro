from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .__init__ import Game
import cv2
import numpy as np

class Yolo:
    def __init__(self: 'Game'):
        self._onnx = {}
        self._onnx_session = {}

    def preprocess(self: 'Game'):
        img = cv2.resize(self._frame, self._yolo_resize)  # 이미 ndarray
        img = img.transpose(2, 0, 1)  # HWC -> CHW
        img = img.astype(np.float32) / 255.0
        return img[np.newaxis, :]

    def postprocess(self: 'Game',output, conf_thres=0.25, allowed_classes=None):
        preds = output[0]
        if len(preds.shape) == 3:
            preds = preds[0]

        xy_list = []

        SCALE_X = self._hwnd_size[0] / self._yolo_resize[0]
        SCALE_Y = self._hwnd_size[1] / self._yolo_resize[1]

        for det in preds:
            conf = float(det[4])
            cls = int(det[5])
            if conf < conf_thres:
                continue
            if allowed_classes and cls not in allowed_classes:
                continue

            x1, y1, x2, y2 = det[:4]
            cx = (x1 + x2) / 2 * SCALE_X
            cy = (y1 + y2) / 2 * SCALE_Y

            xy_list.append({
                "x": int(cx),
                "y": int(cy),
                "pt" : (int(cx),int(cy)),
                "conf": round(conf, 2),
                "class": cls
            })

        return xy_list