import cv2
import imutils
import numpy as np
from shape_detailer import shape_detailer as sd
import serial


cam = cv2.VideoCapture(1)

kernel = np.ones((5,5),dtype = np.uint8)
kernel2 = np.ones((5,5),dtype = np.float32)/25

while(True):

    ret, frame = cam.read()

    filtered_img = cv2.filter2D(frame,-1,kernel2)

    gray = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh,kernel,iterations = 2)
    # thresh = cv2.Canny(gray, 100, 180)

    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = imutils.grab_contours(contours)
    detector = sd()
    for c in centers:
        M=cv2.moments(c)

        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
            cv2.drawContours(frame, [c], -1, (0,255,0), 2)
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05*peri, True)

            min_x = c[0][0][0]
            min_y = c[0][0][1]

            for i in range(0,len(c)):
                if c[i][0][0]<min_x:
                    min_x = c[i][0][0]

                if c[i][0][1]<min_y:
                    min_y = c[i][0][1]

            max_x = c[0][0][0]
            max_y = c[0][0][1]

            for i in range(0,len(c)):
                if c[i][0][0]>max_x:
                    max_x = c[i][0][0]

                if c[i][0][1]>max_y:
                    max_y = c[i][0][1]

            contour_frame = frame[min_y:max_y,min_x:max_x]

            frame = detector.computeShape(frame, approx, x, y)











































            
            frame = detector.colorDetect(frame, contour_frame, x, y)

    if cv2.waitKey(1)&0xFF == ord('c'):
        b = 0
        g = 0
        r = 0
        t = 0
        frame = cv2.resize(frame, (340,480))
        for x in range(0,340,1):
            for y in range(0,480,1):
                color = frame[y,x]
                b = b + color[0]
                g = g + color[1]
                r = r + color[2]
        t = b+g+r
        if t != 0:
            b = (b/t)*100
            g = (g/t)*100
            r = (r/t)*100
            print("b = ", b)
            print("g = ", g)
            print("r = ", r)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF
    if k==27:
        break

cam.release()
cv2.destroyAllWindows()
