import subprocess
import os
def onnx_to_kmodel(data_path, modelid):
    simple_path = f"models/onnx/{modelid}_simple.onnx"
    kmodel_path = f"models/kmodel/{modelid}.kmodel"
    proc = subprocess.Popen(['./install/bin/ncc', 'compile',simple_path,kmodel_path,'-i','onnx','-t','k210','--input-std','0.5','--input-mean','0.5','--dataset',data_path,'--calibrate-method','l2' ])
    out,err = proc.communicate() # wait nncase result