import urllib.request
import cv2
import numpy as np
while True:
    url="http://192.168.43.21:8080/shot.jpg"
    img=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img.read()),dtype=np.uint8)
    imgreal=cv2.imdecode(imgnp,-1)
    cv2.imshow("test",imgreal)
    #print("gjg")
    if(ord('q')==cv2.waitKey(10)):
        exit(0)