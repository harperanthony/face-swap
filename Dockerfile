FROM runpod/base:0.4.0-cuda11.8.0

# Set the working directory
WORKDIR /app

# Copy requirements and source code to the image
COPY requirements.txt ./
COPY run.py ./
COPY modules/ ./modules/

# Upgrade pip and install dependencies with logging
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r requirements.txt --no-cache-dir > install.log 2>&1

# Run the script (if needed for setup)
# RUN python3.11 ./run.py

# Set the command to run the script when the container starts
CMD ["python3.11", "-u", "run.py"]
