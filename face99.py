import cv2
import numpy as np
import serial
import timeit

# 가중치 파일 경로
cascade_filename = 'haarcascade_frontalface_alt.xml'
# 모델 불러오기
cascade = cv2.CascadeClassifier(cascade_filename)

sp = serial.Serial('COM3', 9600, timeout = 1)

webcam = cv2.VideoCapture(0)

pos_x = pos_y = 90
_pos_x = _pos_y = 90

margin_x = 20
margin_y = 20

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, img = webcam.read()
    img = cv2.resize(img,dsize=None,fx=1.0,fy=1.0)
    frame = cv2.flip(img, 1)
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    results = cascade.detectMultiScale(gray,            # 입력 이미지
                                        scaleFactor= 1.1,# 이미지 피라미드 스케일 factor
                                        minNeighbors=5,  # 인접 객체 최소 거리 픽셀
                                        minSize=(20,20)  # 탐지 객체 최소 크기
                                        )
      
    for box in results:
        x, y, w, h = box
        print("center = (%s, %s)" % (x - w//2, y + h//2))             
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,255,255), thickness=2)
                                               
        center_x = x + w//2
        center_y = y + h//2
        print("center: ( %s, %s )"%(center_x, center_y)) 
        
        if center_x < 320 - margin_x:
            print("pan left")
            if pos_x - 1 >= 0:
                pos_x = pos_x - 1
                _pos_x = pos_x
            else:
                pos_x = 0
                _pos_x = pos_x
                
        elif center_x > 320 + margin_x:
            print("pan right")
            if pos_x + 1 <= 180:
                pos_x = pos_x + 1
                _pos_x = pos_x
            else:
                pos_x = 180
                _pos_x = pos_x   
        else:
            print("pan stop")
            pos_x = _pos_x           
            
        tx_data = "pan" + str(pos_x) + '\n'
        sp.write(tx_data.encode())
        print(tx_data)        
        
        if center_y < 240 - margin_y:
            print("tilt up")
            if pos_y - 1 >= 0:
                pos_y = pos_y - 1
                _pos_y = pos_y
            else:
                pos_y = 0
                _pos_y = pos_y
                
        elif center_y > 240 + margin_y:
            print("tilt down")
            if pos_y + 1 <= 180:
                pos_y = pos_y + 1
                _pos_y = pos_y
            else:
                pos_y = 180
                _pos_y = pos_y
        else:
            print("tilt stop")
            pos_y = _pos_y
                 
        tilt_data = "tilt" + str(pos_y) + '\n'
        sp.write(tilt_data.encode())
        print(tilt_data)      
            
    cv2.imshow("VideoFrame",frame)       # show original frame
    
    k = cv2.waitKey(100) & 0xFF
        
    if k == 27:
        break        
cv2.destroyAllWindows()