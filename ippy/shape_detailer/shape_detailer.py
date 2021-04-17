import cv2
import math

class shape_detailer():

    def __init__(self):

        self.color = ('b', 'g', 'r')

        self.shape_detected = 0 #( 1 for triangle, 2 for square, 3 for circle, 4 for polygon, 5 for quad)


    def computeShape(self, main_image, approx, center_x, center_y):

        if len(approx) == 3:
            
            self.shape_detected = 1
            cv2.putText(main_image, 'Triangle', (center_x,center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)

        elif len(approx) == 4:
            dst1 = int(math.sqrt(math.pow(approx[0][0][0]-approx[1][0][0],2) + math.pow(approx[0][0][1]-approx[1][0][1],2)))
            dst2 = int(math.sqrt(math.pow(approx[0][0][0]-approx[3][0][0],2) + math.pow(approx[0][0][1]-approx[3][0][1],2)))

            if int(math.sqrt(math.pow(dst2 - dst1,2))) <=15:
                cv2.putText(main_image, 'Square', (center_x,center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                self.shape_detected = 2
            else:
                cv2.putText(main_image, 'Quad', (center_x,center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                self.shape_detected = 5
                
        elif len(approx) > 4:
            radius = []
            for i in range(0, len(approx)):
                radius.append(int(math.sqrt(math.pow(center_x-approx[i][0][0],2)+math.pow(center_y-approx[i][0][1],2))))

            min_rad = radius[0]
            for i in radius:
                if i<min_rad:
                    min_rad=i

            flag2 = 0
            for i in radius:
                if i-min_rad>=50:
                    flag2=1
                    break

            if flag2 == 0:
                cv2.putText(main_image, 'Circle', (center_x,center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                self.shape_detected = 3           
            else:
                cv2.putText(main_image, 'Polygon', (center_x,center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                self.shape_detected = 4

        return main_image


    def colorDetect(self, main_image, contour_img, center_x, center_y):

        for i,col in enumerate(self.color):
            hist = cv2.calcHist([contour_img],[i],None,[3],[0,256])

        if hist[0]>hist[1] and hist[0]>hist[2]:
            cv2.putText(main_image, 'Blue', (center_x, center_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0,0,0), 1, cv2.LINE_AA)

        elif hist[1]>hist[0] and hist[1]>hist[2]:
            cv2.putText(main_image, 'Green', (center_x, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 0), 1, cv2.LINE_AA)

        elif hist[2]>hist[0] and hist[2]>hist[1]:
            cv2.putText(main_image, 'Red', (center_x, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 0), 1, cv2.LINE_AA)

        return main_image

        
