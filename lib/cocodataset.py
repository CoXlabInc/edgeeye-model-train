
# {"name":"%s","x":%f,"y":%f,"w":%f,"h":%f}
import json
import base64
import wget
import zipfile
from pyiotown import post
import os

num = 0
category = {}
annodict = {}
def make_label(file_name, label, bbox):
    img_file = open("./upload_data/coco2017/train2017/" + file_name , 'rb')
    message = '{"image":"'
    message += base64.b64encode(img_file.read()).decode('UTF-8')
    img_file.close()
    message += '","type":"jpg","labels":['
    first = True
    for box in bbox:
        if first:
            first = False
        else:
            message += ','
        message += '{"name":"%s","x":%f,"y":%f,"w":%f,"h":%f}' % (label,box[0],box[1],box[2],box[3])
    message += ']}'
    return message    

def sendToIoTown(json_data, url, token, label):
    global category, annodict, num
    #init category
    for cat in json_data['categories']:
        category[cat['name']] = cat['id']
    if label not in category:
        print("coco 2017 has no label [",label,"]") 
        exit()

    #Save Annotation Dictionary
    for anno in json_data['annotations']:
        if anno['iscrowd'] == 1:
            continue
        if category[label] == anno['category_id']:
            image_id = anno['image_id']
            if (image_id not in annodict):
                annodict[image_id] = []
                annodict[image_id].append(anno)
            else:
                annodict[image_id].append(anno)
    print(len(annodict.keys()), "images will be uploaded")
    for image in json_data['images']:
        file_name = image['file_name']
        width = image['width']
        height = image['height']
        image_id = image['id']
        if (image_id not in annodict):
            continue
        annolist = annodict[image_id]
        bbox = []
        for anno in annolist:
            x = ( float(anno['bbox'][0]) + ( float(anno['bbox'][2]) / 2) ) / width
            y = ( float(anno['bbox'][1]) + ( float(anno['bbox'][3]) / 2) ) / height
            w = float(anno['bbox'][2]) / width
            h = float(anno['bbox'][3]) / height
            bbox.append([x,y,w,h])
        payload = make_label(file_name, label, bbox)
        r = post.uploadImage(url, token, payload)
        if r:
            num += 1
            print("Upload Success ./upload_data/coco2017/train2017/%s" % file_name)
        else:
            print("Upload Fail.")



def upload_dataset(url, token, label):
    print("Coco Dataset 2017 Image Download")
    download_url = ["http://images.cocodataset.org/zips/train2017.zip"]
    tar_url = ["./upload_data/train2017.zip"]
    for down_url in download_url:
        if not os.path.isfile("./upload_data/train2017.zip"):
            wget.download(down_url, out="./upload_data/") 
        else:
            print(down_url,"is already exist!")
    print("\n Downloaded OK. Unzip Dataset....")
    for tarURL in tar_url:
        zip_ref = zipfile.ZipFile(tarURL, 'r')
        zip_ref.extractall("./upload_data/coco2017/")
        zip_ref.close()
    print("extract OK.")
    print("Coco Dataset 2017 Annotation Download")
    if not os.path.isfile("./upload_data/annotations_trainval2017.zip"):
        wget.download("http://images.cocodataset.org/annotations/annotations_trainval2017.zip", out="./upload_data/")
    else:
        print("annotation already exist!")
    print("\n download OK. Unzip Annotation...")
    zip_ref = zipfile.ZipFile("./upload_data/annotations_trainval2017.zip", 'r')
    zip_ref.extractall("./upload_data/coco2017/")
    zip_ref.close()
    with open("./upload_data/coco2017/annotations/instances_train2017.json", 'r') as f:
        json_data = json.load(f)
        sendToIoTown(json_data, url, token, label)
    print("total",num,"file upload ok")