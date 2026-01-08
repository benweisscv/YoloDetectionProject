import cv2
import numpy as np


def letterbox(img, new_size=640, color=(114, 114, 114)):
    h, w = img.shape[:2]
    scale = min(new_size / h, new_size / w)

    nh, nw = int(h * scale), int(w * scale)
    resized = cv2.resize(img, (nw, nh))

    canvas = np.full((new_size, new_size, 3), color, dtype=np.uint8)
    top = (new_size - nh) // 2
    left = (new_size - nw) // 2
    canvas[top:top + nh, left:left + nw] = resized

    return canvas, scale, left, top


def preprocess(image_bgr):
    img, scale, pad_x, pad_y = letterbox(image_bgr)

    img = img[:, :, ::-1]  # BGR → RGB
    img = img.astype(np.float16) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)

    return img, scale, pad_x, pad_y
