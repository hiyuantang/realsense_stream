import socket
import cv2
import pickle
import struct
import zlib

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.31.141.191'  
port = 9998

client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("L")

while True:
    # Retrieve message size for color data
    while len(data) < payload_size:
        data += client_socket.recv(4096)
    packed_color_size = data[:payload_size]
    data = data[payload_size:]
    color_size = struct.unpack("L", packed_color_size)[0]

    # Retrieve compressed color data
    while len(data) < color_size:
        data += client_socket.recv(4096)
    color_data_compressed = data[:color_size]
    data = data[color_size:]

    # Decompress color data
    color_data = zlib.decompress(color_data_compressed)

    # Retrieve message size for depth data
    while len(data) < payload_size:
        data += client_socket.recv(4096)
    packed_depth_size = data[:payload_size]
    data = data[payload_size:]
    depth_size = struct.unpack("L", packed_depth_size)[0]

    # Retrieve compressed depth data
    while len(data) < depth_size:
        data += client_socket.recv(4096)
    depth_data_compressed = data[:depth_size]
    data = data[depth_size:]

    # Decompress depth data
    depth_data = zlib.decompress(depth_data_compressed)

    # Extract frames
    color_frame = pickle.loads(color_data)
    depth_frame = pickle.loads(depth_data)

    # Display color and depth frames
    cv2.imshow("Received Color", color_frame)
    cv2.imshow("Received Depth", depth_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

