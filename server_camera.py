import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import base64

HOST='192.168.1.70'
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

### new
data = b''
payload_size = struct.calcsize("L")
while True:
    try:
        while len(data) < payload_size:
            data += conn.recv(4096*2)
            if not data:
                break
        if len(data) == 0 or len(data) < payload_size:
            cv2.destroyAllWindows()
            pass
        else:
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += conn.recv(4096*2)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            print(data)
            ###
            frame=pickle.loads(frame_data)
            # print(frame)
            cv2.imshow('frame',frame)
            cv2.waitKey(1)
    except socket.error:
        time.wait(1)
        cv2.destroyAllWindows()
