"""
This code is used to convert the pytorch model into an onnx format model.
"""
import sys
import argparse
import torch.onnx
import os
from onnxsim import simplify
import onnx

from vision.ssd.config.fd_config import define_img_size
from vision.ssd.mb_tiny_RFB_fd import create_Mb_Tiny_RFB_fd
from vision.ssd.mb_tiny_fd import create_mb_tiny_fd


input_img_size = 320  # define input size ,default optional(128/160/320/480/640/1280)
define_img_size(input_img_size)

def pth_to_onnx(modelid):
    label_path = "models/train-version-RFB/" + modelid + "/voc-model-labels.txt"
    class_names = [name.strip() for name in open(label_path).readlines()]
    num_classes = len(class_names)

    model_list = os.listdir("models/train-version-RFB/" + modelid)
    lossdict = {}
    for model in model_list:
        if(model[-3:] != "pth"):
            continue
        loss = model.split('-')[4][:-4]
        lossdict[loss] = model
    print()
    model_path = "models/train-version-RFB/" + modelid + "/" + lossdict[min(lossdict.keys())]

    net = create_Mb_Tiny_RFB_fd(len(class_names), is_test=True)
    net.load(model_path)
    net.eval()
    net.to("cuda")

    model_path = f"models/onnx/{modelid}.onnx"

    dummy_input = torch.randn(1, 3, 240, 320).to("cuda")

# dummy_input = torch.randn(1, 3, 480, 640).to("cuda") #if input size is 640*480

    torch.onnx.export(net, dummy_input, model_path, verbose=False, input_names=['input'], output_names=['scores', 'boxes'])
    model = onnx.load(model_path)
    # convert model
    model_simp, check = simplify(model)
    simple_path=  f"models/onnx/{modelid}_simple.onnx"
    onnx.save(model_simp, simple_path)
    return check
