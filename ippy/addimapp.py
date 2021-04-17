import cv2
import numpy as np


cap = cv2.VideoCapture(0)

_, frame = cap.read()
w, h, d = frame.shape
print(w, h, d)
copy = frame.copy()
#output.resize(w, 2*h, 3)
output = np.concatenate((copy, frame), axis = 1)
while True:
    cv2.imshow('output', output)
    if cv2.waitKey(1)&0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()