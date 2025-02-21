FROM runpod/base:0.4.0-cuda11.8.0

RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir 

RUN python3.11 /run.py

CMD python3.11 -u /run.py