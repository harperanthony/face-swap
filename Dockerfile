FROM runpod/base:0.4.0-cuda11.8.0

# Set the working directory
WORKDIR /app

# Copy requirements and source code to the image
COPY requirements.txt ./
COPY run.py ./

# Upgrade pip and install dependencies
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r requirements.txt --no-cache-dir 

# Set the command to run the script when the container starts
CMD ["python3.11", "-u", "run.py"]
