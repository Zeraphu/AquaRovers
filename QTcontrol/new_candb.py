import cv2
from shapeDetailer2 import shape_detailer
import numpy as np


def detect(c):
	shape = 'unknown'
    # calculate perimeter using
	peri = cv2.arcLength(c, True)
    # apply contour approximation and store the result in vertices
	vertices = cv2.approxPolyDP(c, 0.04 * peri, True)

    # If the shape it triangle, it will have 3 vertices
	if len(vertices) == 3:
		shape = 'triangle'

    # if the shape has 4 vertices, it is either a square or
    # a rectangle
	elif len(vertices) == 4:
        # using the boundingRect method calculate the width and height
        # of enclosing rectange and then calculte aspect ratio

		x, y, width, height = cv2.boundingRect(vertices)
		aspectRatio = float(width) / height
        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
		if aspectRatio >= 0.95 and aspectRatio <= 1.05:
			shape = "square"
		else:
			shape = "rectangle"
    # if the shape is a pentagon, it will have 5 vertices
	elif len(vertices) == 5:
		shape = "pentagon"

    # otherwise, we assume the shape is a circle
	elif len(vertices) == 10:
		shape = "star"
	else:
		shape = "circle"

    # return the name of the shape
	return shape

def c_and_b(image, clip_hist_percent = 10):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calc grayscale hist
    ghist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    ghist_size = len(ghist)

    # Calcs cumulative dist
    acc = []
    acc.append(float(ghist[0]))
    for i in range(1, ghist_size):
        acc.append(acc[i-1] + float(ghist[i]))

    max = acc[-1]
    clip_hist_percent *= (max/100.0)
    clip_hist_percent /= 2.0
    try:
    # Locate left cut
        min_gray = 0
        while acc[min_gray] < clip_hist_percent:
            min_gray += 1

    # Locate right cut
        max_gray = ghist_size-1
        while acc[max_gray] >= (max-clip_hist_percent):
            max_gray -= 1
    except IndexError:
        acc[0] = (max-clip_hist_percent)

    alpha = 255/(max_gray-min_gray)
    beta = -min_gray*alpha

    output = cv2.convertScaleAbs(image, alpha = alpha, beta = beta)
    return (output, alpha, beta)

cam = cv2.VideoCapture(0)
#sd = shape_detailer()

while(True):

    ret, frame = cam.read()
    frame2, alpha, beta = c_and_b(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    v = np.median(gray)
    high = int(max(255, (1+0.33)*v))
    low = int(max(0, 1-0.33)*v)

    canny = cv2.Canny(gray, low, high)
    
    contours, img = cv2.findContours(canny, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        shape = 'unknown'
        if cv2.contourArea(c)<300:
            continue
      #  M = cv2.moments(c)
     #   x = int(M['m10']/M['m00'])
    #    y = int(M['m01']/M['m00'])
 #       shape = detect(c)
        if shape == 'unknown':
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
  #          cv2.putText(frame, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow('frame2', frame2)
    cv2.imshow('frame', frame)
    cv2.imshow('contrast', canny)
    k = cv2.waitKey(25) & 0xFF

    if k == 27:  
        break

cam.release()
cv2.destroyAllWindows()
