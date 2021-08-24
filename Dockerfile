#for Edgeeye-Model-Train
FROM pytorch/pytorch:latest

WORKDIR /app
ENV LANG C.UTF-8
RUN apt-get update
RUN apt-get install -y libhdf5-serial-dev hdf5-tools libgl-dev libgeos-dev libglib2.0-0 vim 
RUN apt-get update
RUN apt-get install -y libgomp1 software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt update
RUN apt install -y gcc-10 libstdc++6
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install opencv-python
RUN python3 -m pip install typing
RUN python3 -m pip install ptflops
RUN python3 -m pip install onnx==1.8.1 onnxruntime onnx-simplifier
RUN python3 -m pip install matplotlib
RUN python3 -m pip install flask
RUN python3 -m pip install future
RUN python3 -m pip install aiohttp
RUN python3 -m pip install aiofiles
RUN python3 -m pip install wget
