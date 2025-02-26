import socket  
import cv2  
import numpy as np  
import struct  
import threading  
import random  
import string  
import os  

import cv2
from cv2_enumerate_cameras import enumerate_cameras  # Add this import
import time
from modules.face_swapper import process_frame

from modules.face_analyser import (
    get_one_face,
)

# Server configuration  
HOST = '213.173.108.139'  # Replace with your server's IP address  
PORT = 11058  

def handle_client(conn, addr):  
    print(f"Connection from: {addr}")  
    data = b""  
    payload_size = struct.calcsize("Q")  

    frames = []  # List to hold captured frames

    # Step 1: Receive the reference image  
    # Receive the size of the reference image  
    while len(data) < payload_size:  
        packet = conn.recv(4 * 1024)  
        if not packet:  
            print(f"Connection lost with {addr} while receiving reference image size.")  
            conn.close()  
            return  
        data += packet  

    packed_msg_size = data[:payload_size]  
    data = data[payload_size:]  
    ref_image_size = struct.unpack("Q", packed_msg_size)[0]  

    # Receive the reference image data  
    while len(data) < ref_image_size:  
        data += conn.recv(4 * 1024)  

    ref_image_data = data[:ref_image_size]  
    data = data[ref_image_size:]  

    # Decode and save the reference image  
    ref_image = np.frombuffer(ref_image_data, dtype=np.uint8)  
    ref_image = cv2.imdecode(ref_image, cv2.IMREAD_COLOR)  

    # Generate a random filename for the reference image  
    source_image = None
    # Step 2: Process video frames  
    while True:  
        # Receive frame size  
        while len(data) < payload_size:  
            packet = conn.recv(4 * 1024)  
            if not packet:  
                break  
            data += packet  

        if len(data) < payload_size:  
            print(f"Connection lost with {addr}")  
            break  

        packed_msg_size = data[:payload_size]  
        data = data[payload_size:]  
        msg_size = struct.unpack("Q", packed_msg_size)[0]  

        # Receive the actual frame  
        while len(data) < msg_size:  
            data += conn.recv(4 * 1024)  

        frame_data = data[:msg_size]  
        data = data[msg_size:]  

        # Decode the frame  
        frame = np.frombuffer(frame_data, dtype=np.uint8)  
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)  

        if source_image is None:
            source_image = get_one_face(ref_image)
        processed_frame = process_frame(source_image, frame)

        frames.append(processed_frame)  

        # Resize processed frame to approximate original sent size if necessary  
        # processed_frame = cv2.resize(processed_frame, (320, 240))  # Resize as per client   

        # Encode the processed frame  
        _, buffer = cv2.imencode('.jpg', processed_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  
        processed_data = buffer.tobytes()  

        # Send the processed frame back to the client  
        processed_msg_size = struct.pack("Q", len(processed_data))  
        conn.sendall(processed_msg_size + processed_data)  

    conn.close()  

def start():  
    # Create a socket  
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.connect(("8.8.8.8", 80))
    # HOST = server_socket.getsockname()[0]
    # server_socket.close()
    server_socket.bind((HOST, PORT))  
    server_socket.listen(5)  # Allow up to 5 unaccepted connections before refusing new connections  
    print("Server listening on", HOST, PORT)  

    while True:  
        conn, addr = server_socket.accept()  
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))  
        client_thread.start()
