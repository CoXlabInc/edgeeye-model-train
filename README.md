<img src="logo/edgeeye.jpg" title="EdgeEye" alt="EdgeEye"></img><br/>
# **Edgeeye Model Train**

Edgeeye Custom Model Training based on - [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB]=)

---
## **1. Environment**
- Linux ( currently only support )
## **2. Install**
1. Dockerfile Build & Run
2. Upload Custom Dataset
3. Show Datasets
4. Train Start
5. Test Model
---
## **3. Dockerfile Build & Run**
- Dockerfile Build
```
docker build --tag {tagname} ./
```
- Run Docker
```
docker run --rm -it --runtime nvidia --network host -v $PWD:/app {tagname}
```
---
## **4. Upload Dataset**
### *parameters*
| name | desc | example |
|:---:|:---:|:---:|
|--dataset, -d| dataset name| coco2017 |
|--token, -t| IoT.own API token| aboi123jflkmb |
|--url, -u| IoT.own Server URL | https://town.coxlab.kr |
|--label, -l| Object Class| cat |
```
python3 upload.py --dataset {dataset name} --token {IoT.own Api token} --url {IoT.own Server URL} --label {object class}
```
- voc2007 or voc2012 + person
```
python3 upload.py --dataset voc2007 --token aboi123jflkmb --url https://town.coxlab.kr --label person
or
python3 upload.py --dataset voc2012 --token aboi123jflkmb --url https://town.coxlab.kr --label person
```
- coco + car
```
python3 upload.py --dataset coco2014 --token aboi123jflkmb --url https://town.coxlab.kr --label car

```
- ## *Custom dataset*
If you want upload your custom dataset, you should keep data format<br> **(reference example/customdata)**
### 1. folder structure
```
upload_data
    \customdata
        \imgs
            \0000001.jpg
            \0000002.jpg
            ...
            \0001000.jpg
        annotations.csv

```
### 2. annotations.csv


### *format*
|name|desc|example|
|:---:|:---:|:---:|
| filename | image file name| 0000001.jpg |
| class | object class | cat |
| x | box center X ratio ( center X coordinate / image width )| 0.36 |
| y | box center Y ratio ( center Y coordinate / image height )| 0.69 |
| w | box width ratio ( box width / image width ) | 0.16 |
| h | box height ratio ( box height / image height) | 0.42 | 
### *csv example*
| filename | class | x | y | w | h |
|:---:|:---:|:---:|:---:|:---:|:---:|
|0000001.jpg|cat|0.36|0.69|0.16|0.42|
|0000001.jpg|car|0.16|0.57|0.32|0.32|
|0000002.jpg|person|0.50|0.63|0.14|0.52|
|0000003.jpg|person|0.60|0.49|0.47|0.69|

```
python3 upload.py --dataset custom --token aboi123jflkmb --url https://town.coxlab.kr --label cat
```
---
## **5. Train Start**
Essential Parameter : -c : class, -f : confirmed, -d : dataset, -t : token, -a: address -i:modelid
- ex) using coco2014 dataset, confirmed dataset, person class
```
sh run.sh -d coco2014 -t aboi123jflkmb -f 1 -c person -a https://town.coxlab.kr -i abcd1234
```
- ex) using coco2014 + voc2007 dataset, unconfirmed dataset, car class
```
sh run.sh -d coco2014 voc2007 -t aboi123jflkmb -f 0 -c car -a https://town.coxlab.kr -i abcd1234
```
---
## **6. Test Model**
input imageroot, onnxroot, kmodelroot then draw box to original image
```
python3 model_test.py --image ./image/1.jpg --onnx ./models/onnx/abcd1234_simple.onnx --kmodel abcd1234.kmodel
```
check /inference folder save with name 1.jpg (original image name)


---
## **7. Reference**
- [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB)
- [nncase](https://github.com/kendryte/nncase)
