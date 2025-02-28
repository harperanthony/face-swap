#!/bin/bash  

echo "Starting setup..."  

python -m pip install --upgrade pip
pip install -r requirements.txt

apt update
apt install ffmpeg

echo "Setup completed!"