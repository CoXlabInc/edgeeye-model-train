<img src="logo/edgeeye.jpg" title="EdgeEye" alt="EdgeEye"></img><br/>
# Edgeeye Model Train 

Edgeeye Custom Model Training based on - [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB]=)

---
## Environment
- Linux ( currently only support )
## Install
1. Dockerfile Build & Run
2. Start Script
3. Select Model & Datasets
4. Train Start
---
## Dockerfile Build & Run
- Dockerfile Build
```
docker build --tag {tagname} ./
```
## Start Script
- Run Docker
```
docker run --rm -it --runtime nvidia --network host -v $PWD:/app {tagname}
```
- Run Script
```
sh run.sh
```
## Select Model & Datasets

## Train Start

## Reference
- [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB]=)
- [nncase](https://github.com/kendryte/nncase)