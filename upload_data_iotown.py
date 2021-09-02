import argparse
import xml.etree.ElementTree as ET
import base64
import wget
import tarfile
from pyiotown import model
# sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val')]
sets=[]
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    in_file = open('./upload_data/VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    img_file = open('./upload_data/VOCdevkit/VOC%s/JPEGImages/%s.jpg' % (year, image_id), 'rb')

    message = '{"image":"'
    message += base64.b64encode(img_file.read()).decode('UTF-8')
    img_file.close()
    message += '","type":"jpg","labels":['
    first = True

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        if first:
            first = False
        else:
            message += ','
        message += '{"name":"%s","x":%f,"y":%f,"w":%f,"h":%f}' % (cls, bb[0], bb[1], bb[2], bb[3])
    message += ']}'
    return message

def sendToIoTown():
    for year, image_set in sets:
        f = open('./upload_data/VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set))
        contents = f.read()
        image_ids = contents.strip().split()
        for image_id in image_ids:
            payload = convert_annotation(year, image_id)
            r = model.uploadImage(args.url,args.token,payload)
            if r:
                print('Upload Success./upload_data/VOCdevkit/VOC%s/JPEGImages/%s.jpg' % (year, image_id))
            else:
                print("Upload Fail.")

            

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Dataset uploader for IoT.own')
    parser.add_argument("-l", "--list", help="get list of dataset in IoT.own",action="store_true")
    parser.add_argument("-d", "--dataset", help="dataset names ex) coco2014, voc2012, voc2007")
    parser.add_argument("-t", "--token", help="you must input api token for using IoT.own API")
    parser.add_argument("-u", "--url", help="IoT.own Server URL ex) http://192.168.0.224")
    args = parser.parse_args()


    if args.list:
        print("----------------------------")
        print("# Dataset From IoT.own #")
        print("----------------------------")
        print("voc2007")
        print("voc2012")
        print("coco2014")
        print("----------------------------")
        exit()
    else:
        if args.dataset == None or args.token == None or args.url == None:
            print("You must input Dataset & Token & server url. check -h")
            exit()
    download_url = ""
    tar_url = ""
    if args.dataset == "voc2012":
        download_url = "https://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar"
        tar_url = "./upload_data/VOCtrainval_11-May-2012.tar"
        sets = [('2012', 'train'), ('2012', 'val')]
    elif args.dataset == "voc2007":
        download_url = "https://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar"
        tar_url = "./upload_data/VOCtrainval_06-Nov-2007.tar"
        sets = [('2007', 'train'), ('2007', 'val')]
    elif args.dataset == "coco2014":
        download_url = "fuck"
        tar_url = "fuck2"
    else: 
        print("Dataset", args.dataset ,"is Not Exist in IoT.own")
        exit()
    print("Downloading Dataset....")
    wget.download(download_url, out="./upload_data/") 
    print("\n Downloaded OK. Unzip Dataset....")
    tar = tarfile.open(tar_url)
    tar.extractall(path="./upload_data/")
    tar.close()
    print("extract OK.")
    print("Send To IoT.own")
    sendToIoTown()
    
