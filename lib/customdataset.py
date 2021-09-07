#custom dataset upload
'''
    Custom dataset 
    Format (CSV,JPEG)
    folder:
        1. /imgs
        2. /annotations


    | filename | class | x | y | w | h |
    # filename : img file name ex) 000001.jpg
    # class : object class ex) person, car, boat
    # x : box center x ratio ex) 0.12
    # y : box center y ratio ex) 0.34
    # w : box width ratio ex) 0.1
    # h : box width ratio ex) 0.1

'''
from pyiotown import post
import csv
import base64
num = 0
annodict = {}
def make_label(file_name, label, bbox):
    img_file = open("./upload_data/customdata/imgs/" + file_name, 'rb')
    message = '{"image":"'
    message += base64.b64encode(img_file.read()).decode('UTF-8')
    img_file.close()
    message += '","type":"jpg","labels":['
    first = True
    for box in bbox:
        if (box[0] != label):
            continue
        if first:
            first = False
        else:
            message += ','
        message += '{"name":"%s","x":%f,"y":%f,"w":%f,"h":%f}' % (box[0],float(box[1]),float(box[2]),float(box[3]),float(box[4]))
    message += ']}'
    return message
def sendToIoTown(url,token,label):
    global num
    print("read annotations")
    f = open('./upload_data/customdata/annotations.csv')
    rdr = csv.reader(f)
    for line in rdr:
        if line[1] != label:
            continue
        if line[0] not in annodict:
            annodict[line[0]] = []
            annodict[line[0]].append(line[1:])
        else:
            annodict[line[0]].append(line[1:])
    f.close()
    print("upload to iotown")
    for image in annodict:
        payload = make_label(image, label, annodict[image])
        r = post.uploadImage(url, token, payload)
        if r:
            num += 1
            print("Upload Success ./upload_data/customdata/imgs/%s" % image)
        else:
            print("Upload Fail.")
def upload_dataset(url,token,label):
    global sets
    sendToIoTown(url,token,label)
    print("total",num,"file upload ok")