import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.settimeout(10)
clientsocket.connect(('192.168.1.70',8089))

while True:
    try:
        ret,frame=cap.read()
        data = pickle.dumps(frame)
        clientsocket.sendall(struct.pack("L", len(data))+data)
        time.sleep(0.5)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            time.sleep(1)
            print("disconnecting...")
            clientsocket.close()
            break
    except KeyboardInterrupt:
            print('Interrupted')
            clientsocket.close()
            cap.release()
            sys.exit()

clientsocket.close()
cap.release()
print("done")