import xml.etree.ElementTree as ET
import base64
import wget
import tarfile
from pyiotown import post
# sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val')]
sets=[]
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
num = 0

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

def convert_annotation(year, image_id, label):
    in_file = open('./upload_data/VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()
    classes = []
    for obj in root.iter('object'):
        classes.append(obj.find('name').text)
    if label not in classes:
        return None
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

def sendToIoTown(url, token, label):
    global num
    for year, image_set in sets:
        f = open('./upload_data/VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set))
        contents = f.read()
        image_ids = contents.strip().split()
        for image_id in image_ids:
            payload = convert_annotation(year, image_id, label)
            if (payload == None):
                continue
            r = post.uploadImage(url,token,payload)
            if r:
                num += 1
                print('Upload Success./upload_data/VOCdevkit/VOC%s/JPEGImages/%s.jpg' % (year, image_id))
            else:
                print("Upload Fail.")

            

def upload_dataset(url, token, label, year):
    global sets
    download_url = ""
    tar_url = ""
    if year == "voc2012":
        download_url = ["https://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar"]
        tar_url = ["./upload_data/VOCtrainval_11-May-2012.tar"]
        sets = [('2012', 'train'), ('2012', 'val')]
    elif year == "voc2007":
        download_url = ["https://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar", "http://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar"]
        tar_url = ["./upload_data/VOCtrainval_06-Nov-2007.tar","./upload_data/VOCtest_06-Nov-2007.tar"]
        sets = [('2007', 'train'), ('2007', 'val'), ('2007','test')]
    else: 
        print("Dataset", args.dataset ,"invalid dataset.")
        exit()
    print("Downloading Dataset....")
    for down_url in download_url:
        print(down_url)
        wget.download(down_url, out="./upload_data/") 
    print("\n Downloaded OK. Unzip Dataset....")
    for tarURL in tar_url:
        if tarURL[-3:] == "tar":
            tar = tarfile.open(tarURL)
            tar.extractall(path="./upload_data/")
            tar.close()
        else:
            print("unknown zip system check file.")
            exit()
    print("extract OK.")
    print("Send To IoT.own")
    sendToIoTown(url,token,label)
    print("total",num,"file upload ok")
    
