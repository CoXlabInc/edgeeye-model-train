# Annotations/  : xml files
# ImageSets/Main/ : test.txt trainval.txt
# JPEGImages/ : .jpg files

# 이것들을 저장하지말고 그냥 바로 가져오는걸 train.py에서 하면 어떨까?
# 근데 JPEGIMAGES는 어디다 저장해? HMM....
# 램에다 때려박는건, 램사용을 너무 많이해서 별로라고 생각되는데 또 GPU생각하면 그렇진 않은것 같긴 함.
# 일단 램 사용하는건 보류하고 ( 아직 확실한 요구사항이 없음 )


#iotown에서 Annotation 을 가져옴



# 1. Annotation 제작

# 2. ImageSets/Main test.txt trainval.txt 2:8비율로 생성

# 3. JPEGImages JPEG이미지 다운로드

import argparse
import requests
from PIL import Image
from io import BytesIO
import os
from xml.etree.ElementTree import Element, SubElement, ElementTree
from tqdm import tqdm #progress bar

folderRoot = ""
folderAnnotation = ""
folderImageSets = ""
folderJPEG = ""

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
def make_xml(trainClass, folder,filename,width,height,bbox):
    fname = filename
    root = Element('annotation')
    SubElement(root, 'folder').text = folder
    SubElement(root, 'filename').text = fname + ".jpg" #Change
    source = SubElement(root,'source')
    SubElement(source,'database').text = "IoT.own"
    SubElement(source,'annotation').text = folder 
    SubElement(source,'image').text = "flickr"
    SubElement(source,'flickrid').text = '-1' 
    owner = SubElement(root,'owner')
    SubElement(owner,'flickrid').text = "coxlab"
    SubElement(owner,'name').text = "coxlab"
    size = SubElement(root,'size')
    SubElement(size,'width').text = str(width) #change
    SubElement(size,'height').text = str(height) #change
    SubElement(size,'depth').text = '3' 

    SubElement(root, 'segmented').text = '0'
    for box in bbox:
        obj = SubElement(root,'object')
        SubElement(obj,'name').text = trainClass #change
        SubElement(obj,'pose').text = "Unspecified"
        SubElement(obj,'truncated').text = '1'
        SubElement(obj,'difficult').text = '0'

        bndbox = SubElement(obj,'bndbox')
        SubElement(bndbox,'xmin').text = str(box[0]) #change
        SubElement(bndbox,'ymin').text = str(box[1]) #change
        SubElement(bndbox,'xmax').text = str(box[2]) #change
        SubElement(bndbox,'ymax').text = str(box[3]) #change

    indent(root)
    tree = ElementTree(root)
    tree.write(folderAnnotation + "/" + fname + '.xml',encoding='utf-8',xml_declaration=True)

def MakeDirectory(modelid):
    # iotown_data_$modlid mkdir
    # under root Annotations, ImageSets/Main/, JPEGImages folder
    global folderRoot, folderAnnotation, folderImageSets, folderJPEG
    folderRoot = "./data/iotown_data_" + modelid
    folderAnnotation = folderRoot + "/Annotations"
    folderImageSets = folderRoot + "/ImageSets/Main"
    folderJPEG = folderRoot + "/JPEGImages"
    try:
        if not(os.path.isdir(folderRoot)):
            os.makedirs(os.path.join(folderRoot))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create Root directory!!!!!")
            raise

    try:
        if not(os.path.isdir(folderAnnotation)):
            os.makedirs(os.path.join(folderAnnotation))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create Annotation directory!!!!!")
            raise
    try:
        if not(os.path.isdir(folderImageSets)):
            os.makedirs(os.path.join(folderImageSets))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create ImageSets directory!!!!!")
            raise
    try:
        if not(os.path.isdir(folderJPEG)):
            os.makedirs(os.path.join(folderJPEG))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create JPEG directory!!!!!")
            raise
def MakeAnnoAndImage(addr, token, trainClass, dataset):
    labelAddr = addr + "/api/v1.0/nn/images?labels=" + trainClass
    header = {'Accept':'application/json', 'token':token}
    r = requests.get(labelAddr, headers=header).json()
    trainLength = int(len(r['result']) * 0.8)
    count = 0
    f_test  = open( folderImageSets + "/test.txt","w")
    f_train = open( folderImageSets + "/trainval.txt","w")
    f_label = open( folderRoot + "/labels.txt","w")
    f_label.write(trainClass)
    f_label.close()
    for item in tqdm(r['result']):
        imageID = item['id']
        imageAddr = addr + "/nn/dataset/img/" + imageID
        byteimage = requests.get(imageAddr, headers=header).content
        image = Image.open(BytesIO(byteimage))
        image.save(folderJPEG + "/" + imageID + ".jpg") # image save
        minmaxlist = []
        for label in item['labels']:
            imageClass = label['name']
            xmin = (float(label['x']) - float(label['w'])/2) * image.width
            ymin = (float(label['y']) - float(label['h'])/2) * image.height
            xmax = (float(label['x']) + float(label['w'])/2) * image.width
            ymax = (float(label['y']) + float(label['h'])/2) * image.height
            minmaxlist.append([int(xmin), int(ymin), int(xmax), int(ymax)])
            # print (imageID, imageClass, xmin, ymin, xmax, ymax)
        make_xml(trainClass, dataset, imageID, image.width, image.height, minmaxlist) # make xml file
        count += 1
        if count > trainLength:
            f_test.write(imageID + "\n")
        else:
            f_train.write(imageID + "\n")
            # if save file number exceed train ratio (0.8), then save to test.txt
    f_test.close()
    f_train.close()
    print("success")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dataset uploader for IoT.own")
    parser.add_argument("-d", "--dataset", help="Train Dataset in IoT.own")
    parser.add_argument("-f", "--confirmed", help="Dataset config confirmed or not confirmed")
    parser.add_argument("-t", "--token", help="token for using IOTOWN API")
    parser.add_argument("-c", "--trainclass", help="Train Class Label")
    parser.add_argument("-a", "--address", help="IoT.own Server Address")
    parser.add_argument("-i", "--modelid", help="Model ID")
    args = parser.parse_args()

    MakeDirectory(args.modelid)
    MakeAnnoAndImage(args.address, args.token, args.trainclass, args.dataset)

    