import socket
import cv2
import pyrealsense2 as rs
import numpy as np
import pickle
import struct
import zlib

# Configure depth and color streams from RealSense camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

# Start streaming
pipeline.start(config)

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = 'YOUR_UBUNTU_IP_ADDRESS'  # Replace with your Ubuntu system's IP address
port = 9999
socket_address = (host_ip, port)

# Bind and listen
server_socket.bind(socket_address)
server_socket.listen(5)
print("Listening at:", socket_address)

# Accept a client connection
client_socket, addr = server_socket.accept()
print('Connection from:', addr)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())


        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_RAINBOW)

        # Compress color frame
        color_data = zlib.compress(pickle.dumps(color_image))
        # Compress depth frame
        depth_data = zlib.compress(pickle.dumps(depth_colormap))

        # Send message length first, then color data, then depth data
        color_size = struct.pack("L", len(color_data))
        depth_size = struct.pack("L", len(depth_data))
        client_socket.sendall(color_size + color_data + depth_size + depth_data)

finally:
    # Stop streaming
    pipeline.stop()
    client_socket.close()
