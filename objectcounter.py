import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

def createmodel(weights="yolov7.pt", device='cpu'):
    # Initialize
    device = select_device(device)

    # Load model
    return attempt_load(weights, map_location=device)  # load FP32 model


def objcounter(model, source, device='cpu', view_img=True, save_txt=True, imgsz=640, trace=False):
    # Initialize
    device = select_device(device)
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    dataset = LoadImages(source, img_size=imgsz, stride=stride)

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=True)[0]
        t2 = time_synchronized()

        # Apply NMS
        pred = non_max_suppression(pred, 0.375, 0.45, agnostic=True)
        t3 = time_synchronized()

        return len(pred[0])


if __name__=="__main__":
    mdl = createmodel()
    print(objcounter(mdl, '0.jpg', view_img=True, save_txt=True, imgsz=640, trace=False))
    print(objcounter(mdl, '1.jpg', view_img=True, save_txt=True, imgsz=640, trace=False))
    print(objcounter(mdl, '2.jpg', view_img=True, save_txt=True, imgsz=640, trace=False))