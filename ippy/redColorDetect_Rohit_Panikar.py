import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask1= cv2.inRange(hsv,lower_red,upper_red)

    lower_redu = np.array([170,50,50])
    upper_redu = np.array([180,255,255])
    mask2= cv2.inRange(hsv,lower_redu,upper_redu)

    mask = mask1+mask2; # combining both masks

    (img, contours, heirarchy) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>3000):		
            x,y,w,h = cv2.boundingRect(contour)	
            frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),2) # displaying rectangle wherever red is detected
            cv2.putText(frame, "RED", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))

    cv2.imshow('mask',mask)
    cv2.imshow('frame',frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
