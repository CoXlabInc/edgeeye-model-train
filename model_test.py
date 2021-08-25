import cv2
import argparse
import copy
import onnx
import subprocess
import numpy as np
import onnxruntime
import struct

binpath = "./inference/bin/binforinf.bin"
threshold = 0.3

def area_of(left_top, right_bottom):
    """Compute the areas of rectangles given two corners.

    Args:
        left_top (N, 2): left top corner.
        right_bottom (N, 2): right bottom corner.

    Returns:
        area (N): return the area.
    """
    hw = np.clip(right_bottom - left_top, 0.0, None)
    return hw[..., 0] * hw[..., 1]


def iou_of(boxes0, boxes1, eps=1e-5):
    """Return intersection-over-union (Jaccard index) of boxes.

    Args:
        boxes0 (N, 4): ground truth boxes.
        boxes1 (N or 1, 4): predicted boxes.
        eps: a small number to avoid 0 as denominator.
    Returns:
        iou (N): IoU values.
    """
    overlap_left_top = np.maximum(boxes0[..., :2], boxes1[..., :2])
    overlap_right_bottom = np.minimum(boxes0[..., 2:], boxes1[..., 2:])

    overlap_area = area_of(overlap_left_top, overlap_right_bottom)
    area0 = area_of(boxes0[..., :2], boxes0[..., 2:])
    area1 = area_of(boxes1[..., :2], boxes1[..., 2:])
    return overlap_area / (area0 + area1 - overlap_area + eps)

def hard_nms(box_scores, iou_threshold, top_k=-1, candidate_size=200):
    """

    Args:
        box_scores (N, 5): boxes in corner-form and probabilities.
        iou_threshold: intersection over union threshold.
        top_k: keep top_k results. If k <= 0, keep all the results.
        candidate_size: only consider the candidates with the highest scores.
    Returns:
         picked: a list of indexes of the kept boxes
    """
    scores = box_scores[:, -1]
    boxes = box_scores[:, :-1]
    picked = []
    # _, indexes = scores.sort(descending=True)
    indexes = np.argsort(scores)
    # indexes = indexes[:candidate_size]
    indexes = indexes[-candidate_size:]
    while len(indexes) > 0:
        # current = indexes[0]
        current = indexes[-1]
        picked.append(current)
        if 0 < top_k == len(picked) or len(indexes) == 1:
            break
        current_box = boxes[current, :]
        # indexes = indexes[1:]
        indexes = indexes[:-1]
        rest_boxes = boxes[indexes, :]
        iou = iou_of(
            rest_boxes,
            np.expand_dims(current_box, axis=0),
        )
        indexes = indexes[iou <= iou_threshold]

    return box_scores[picked, :]

def predict(width, height, confidences, boxes, prob_threshold, iou_threshold=0.3, top_k=-1):
    boxes = boxes[0]
    confidences = confidences[0]
    picked_box_probs = []
    picked_labels = []
    for class_index in range(1, confidences.shape[1]):
        probs = confidences[:, class_index]
        mask = probs > prob_threshold
        probs = probs[mask]
        if probs.shape[0] == 0:
            continue
        subset_boxes = boxes[mask, :]
        box_probs = np.concatenate([subset_boxes, probs.reshape(-1, 1)], axis=1)
        box_probs = hard_nms(box_probs,
                            iou_threshold=iou_threshold,
                            top_k=top_k,
                            )
        picked_box_probs.append(box_probs)
        picked_labels.extend([class_index] * box_probs.shape[0])
    if not picked_box_probs:
        return np.array([]), np.array([]), np.array([])

    picked_box_probs = np.concatenate(picked_box_probs)
    picked_box_probs[:, 0] *= width
    picked_box_probs[:, 1] *= height
    picked_box_probs[:, 2] *= width
    picked_box_probs[:, 3] *= height
    return picked_box_probs[:, :4].astype(np.int32), np.array(picked_labels), picked_box_probs[:, 4]

def onnx_inference(img, path):
    copy_img = copy.deepcopy(img)
    class_names = ["BACKGROUND", "person"]
    image = cv2.cvtColor(copy_img, cv2.COLOR_BGR2RGB)
    image_mean = np.array([127, 127, 127])
    image = (image - image_mean) / 128
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)

    ort_session = onnxruntime.InferenceSession(path)
    input_name = ort_session.get_inputs()[0].name
    confidences, boxes = ort_session.run(None, {input_name: image})

    boxes, labels, probs = predict(copy_img.shape[1], copy_img.shape[0], confidences, boxes, threshold)
    for i in range(boxes.shape[0]):
        box = boxes[i, :]
        cv2.putText(copy_img, str(round(probs[i],2)), (box[0], box[1]-10),cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0),2)
        cv2.rectangle(copy_img, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 2)
    return copy_img
def kmodel_inference(img, path):
    kmodel_image = copy.deepcopy(img)
    proc = subprocess.Popen(['./install/bin/ncc', 'infer',path,'./inference/binout','--dataset','./inference/bin','--dataset-format','raw','--input-std','0.5','--input-mean','0.5' ],stdout=subprocess.PIPE)
    out,err = proc.communicate() # wait nncase result
    nncasetime = out.decode().split('\n')

    bin_path = "./inference/binout/binforinf.bin"
    binfile = open(bin_path,"rb")
    output = []
    output.append(binfile.read(35360))# Read confidence( 1 * 4420 * 2 ) output[0]
    output.append(binfile.read()) #Read Last ( 1 * 4420 * 4 ) output[1]
    
    #post process kmodel
    data0 = bytearray(output[0])
    bytetuple1 = struct.unpack('<8840f',data0)
    outbrace1 = []
    outbrace2 = []
    for i in range(4420):
        outbrace3 = []
        for j in range(2):
            outbrace3.append(bytetuple1[j + i*2])
        outbrace2.append(outbrace3)
    outbrace1.append(outbrace2)
    numpydata1 = np.array(outbrace1)
    data1 = bytearray(output[1])
    bytetuple2 = struct.unpack('<17680f',data1)
    outbrace1 = []
    outbrace2 = []
    for i in range(4420):
        outbrace3 = []
        for j in range(4):
            outbrace3.append(bytetuple2[j + i*4])
        outbrace2.append(outbrace3)
    outbrace1.append(outbrace2)
    numpydata2 = np.array(outbrace1)
    confidences = numpydata1
    boxes = numpydata2
    boxes, labels, probs = predict(kmodel_image.shape[1], kmodel_image.shape[0], confidences, boxes, threshold)
    for i in range(boxes.shape[0]):
        box = boxes[i, :]
        cv2.putText(kmodel_image, str(round(probs[i],2)), (box[0], box[1]-10),cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0),2)
        cv2.rectangle(kmodel_image, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 2)
    return kmodel_image
if __name__ == "__main__":
    #parsing args
    parser = argparse.ArgumentParser(description="EdgeEye Model Test")
    parser.add_argument("--image", help="input image path",required=True)
    parser.add_argument("--onnx", help="onnx file path",required=True)
    parser.add_argument("--kmodel", help="kmodel file path",required=True)
    args = parser.parse_args()
    # load image
    img = cv2.imread(args.image)
    original_image = cv2.resize(img, dsize=(320,240))

    # save binary to inference kmodel
    transposed = np.transpose(original_image, [2,0,1])
    res = transposed.flatten()
    res.tofile(binpath)
    #onnx inference
    onnxIMG = onnx_inference(original_image, args.onnx)
    #kmodel inference
    kmodelIMG = kmodel_inference(original_image,args.kmodel)
    #save result image
    img_merge = np.hstack([original_image, onnxIMG, kmodelIMG])
    cv2.imwrite("./inference/" + args.image.split("/")[-1],img_merge)