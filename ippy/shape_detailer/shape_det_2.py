import cv2
import imutils
import numpy as np
from shape_detailer import shape_detailer as sd
import threading

cam = cv2.VideoCapture(0)
kernel = np.ones((5,5),dtype = np.uint8)
kernel2 = np.ones((3,3),dtype = np.float32)/25

black = np.zeros((480,640,3), dtype=np.uint8)

def apply_contrast(img, contrast=0):

    if contrast != 0:
        f = 131*(contrast+127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        img = cv2.addWeighted(img, alpha_c, img, 0, gamma_c)
    return img

while(True):

    ret, frame = cam.read()
    frame = apply_contrast(frame, 20)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray  = cv2.filter2D(gray, -1, kernel2)
    v = np.median(gray)
    sigma = 0.33
    low = int(max(0, (1-sigma)*v))
    high = int(max(200, (1+sigma)*v))
    edge = cv2.Canny(gray, low, high)
    #edge = cv2.dilate(edge, kernel, iterations = 2)

    #thresh_ = cv2.bitwise_or(thresh, edge)

    ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh,kernel,iterations = 2)
    #thresh = cv2.Canny(gray, 100, 180)

    final_frame = cv2.bitwise_or(thresh, edge)

    contours = cv2.findContours(final_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = imutils.grab_contours(contours)

    for c in centers:
        M=cv2.moments(c)

        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
            cv2.drawContours(frame, [c], -1, (0,255,0), 2)
            peri = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c, 0.04*peri, True)

            contour_frame = frame[y-10:y+10,x-10:x+10]

            detector = sd(approx,x,y,frame,contour_frame)
            frame = detector.computeShape()
            frame = detector.colorDetect()

    cv2.imshow('frame', frame)
    #cv2.imshow('thresh', thresh)
    #cv2.imshow('gray',gray)
    #cv2.imshow('LAB_colour', lab_frame)
    #cv2.imshow('gray_LAB_colour', gray_lab_frame)
    #cv2.imshow('thresh_lab', thresh_lab_frame)
    cv2.imshow('edge', edge)
    k = cv2.waitKey(1) & 0xFF
    if k==27:
        break

cam.release()
cv2.destroyAllWindows()