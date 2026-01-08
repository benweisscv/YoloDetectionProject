import numpy as np
import cv2

def postprocess(outputs, scale, pad_x, pad_y, conf_thres=0.80, iou_thres=0.45):
            # output0: (1, 12, 8400)
    preds = outputs[0][0].T  # (num_proposals, 4 + num_classes) = (12, 8400) -> (8400, 12)
    boxes_xywh = preds[:, :4]
    class_scores = preds[:, 4:]
    
    cls_ids = np.argmax(class_scores, axis=1)
    confs = class_scores[np.arange(len(class_scores)), cls_ids]
    
    # Filter by confidence
    mask = confs >= conf_thres
    boxes_xywh = boxes_xywh[mask]
    confs = confs[mask]
    cls_ids = cls_ids[mask]
    
    # Convert xywh → xyxy
    boxes_xyxy = np.zeros_like(boxes_xywh)
    boxes_xyxy[:, 0] = boxes_xywh[:, 0] - boxes_xywh[:, 2] / 2  # x1
    boxes_xyxy[:, 1] = boxes_xywh[:, 1] - boxes_xywh[:, 3] / 2  # y1
    boxes_xyxy[:, 2] = boxes_xywh[:, 0] + boxes_xywh[:, 2] / 2  # x2
    boxes_xyxy[:, 3] = boxes_xywh[:, 1] + boxes_xywh[:, 3] / 2  # y2

    # Undo letterbox
    boxes_xyxy[:, [0, 2]] = (boxes_xyxy[:, [0, 2]] - pad_x) / scale
    boxes_xyxy[:, [1, 3]] = (boxes_xyxy[:, [1, 3]] - pad_y) / scale

    # Optional NMS
    if len(boxes_xyxy) > 0:
        indices = cv2.dnn.NMSBoxes(
            boxes_xyxy.tolist(), confs.tolist(), conf_thres, iou_thres
        )
        boxes_xyxy = boxes_xyxy[indices.flatten()]
        confs = confs[indices.flatten()]
        cls_ids = cls_ids[indices.flatten()]

    results = [
        {"bbox": boxes_xyxy[i].tolist(), "score": float(confs[i]), "class": int(cls_ids[i])}
        for i in range(len(boxes_xyxy))
    ]
    return results
