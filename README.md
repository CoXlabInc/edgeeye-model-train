<img src="logo/edgeeye.jpg" title="EdgeEye" alt="EdgeEye"></img><br/>
# Edgeeye Model Train 

Edgeeye Custom Model Training based on - [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB]=)

---
## Environment
- Linux ( currently only support )
## Install
1. Dockerfile Build & Run
2. Upload Custom Dataset
3. Show Datasets
4. Train Start
---
## Dockerfile Build & Run
- Dockerfile Build
```
docker build --tag {tagname} ./
```
- Run Docker
```
docker run --rm -it --runtime nvidia --network host -v $PWD:/app {tagname}
```
## Upload Custom Dataset

```
python3 upload_data_iotown.py --dataset {dataset name} --token {IoT.own Api token} --url {IoT.own Server URL}
```
- voc2007 or voc2012
```
python3 upload_data_iotown.py --dataset voc2007 --token aboi123jflkmb --url https://town.coxlab.kr
or
python3 upload_data_iotown.py --dataset voc2012 --token aboi123jflkmb --url https://town.coxlab.kr
```
- coco
```
python3 upload_data_iotown.py --dataset coco2014 --token aboi123jflkmb --url https://town.coxlab.kr

```
## Show Datasets
show Datasets in IoT.own
```
python3 upload_data_iotown.py --list --token aboi123jflkmb
```
Result
```
----------------------------
# Dataset From IoT.own #
----------------------------
voc2007
voc2012
coco2014
----------------------------
```
## Train Start
Essential Parameter : -c : class, -f : confirmed, -d : dataset, -t : token
- ex) using coco2014 dataset, confirmed dataset, person class
```
sh run.sh -d coco2014 -t aboi123jflkmb -f 1 -c person
```
- ex) using coco2014 + voc2007 dataset, unconfirmed dataset, car class
```
sh run.sh -d coco2014 voc2007 -t aboi123jflkmb -f 0 -c car
```

## Reference
- [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB)
- [nncase](https://github.com/kendryte/nncase)
