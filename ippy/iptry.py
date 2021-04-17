import numpy as np
import cv2
 
cap = cv2.VideoCapture(0)
_, frame = cap.read()

frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert to hsv colorspace

	#lowermask
lower_red = np.arrar[(0,50,50)]
upper_red = np_array[(10,255,255)]
mask1= cv2.inRange(frame_hsv,lower_red,upper_red)
#uppermask
lower_redu = np.array[(170,50,50)]
upper_redu = np.array[(180,255,255)]
mask2= cv2.inRange(frame_hsv,lower_redu,upper_redu)

mask = mask1+mask2;#combining both masks
output_frame = frame_hsv.copy()
output_frame[np.where(mask==0)]=0 #setting hsv values to zero wherever mask doesnt apply

cv2.imshow('frame',output_frame) #output image

#if(cv2.waitKey(1)&0xFF == ord(q)) #if q is pressed, exit loop
#break;

cv2.release()
cv2.destroyAllWindows()

