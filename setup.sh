#!/bin/bash  

echo "Starting setup..."  

python -m pip install --upgrade pip
pip install tensorflow
pip install onnxruntime
pip install onnxruntime-gpu
pip install opencv-python
pip install cv2-enumerate-cameras
pip install insightface

apt update
apt install ffmpeg

echo "Setup completed!"