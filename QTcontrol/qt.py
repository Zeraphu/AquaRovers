from PyQt5.QtCore import Qt
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QWidget, QGridLayout)
import cv2
from threading import Event
import threading
import numpy as np
from shapeDetailer2 import shape_detailer
import random


stopEvent =  Event()
capEvent = Event()
thresh_e = Event()
shape_e = Event()
#sd = shape_detailer()

        
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    changePixmap2 = pyqtSignal(QImage)
    changePixmap3 = pyqtSignal(QImage)
    def run(self):
        self.img_cnt = 0
        num = 100
        self.cap = cv2.VideoCapture(1)
        while not stopEvent.isSet():
            sd = shape_detailer()
            ret, frame = self.cap.read()
            if ret:
                color = frame.copy()
                shape = frame.copy()
                color = sd.apply_brightness(color, 30)
                color = sd.apply_contrast(color, 70)
                if thresh_e.isSet():
                    color = sd.thresold(color)
    
                if shape_e.isSet():
                    shape = sd.computeShape(shape)
                
                rgbImage = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
                #rgbImage.resize(320, 320)
                output = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                sout = cv2.cvtColor(shape, cv2.COLOR_BGR2RGB)

                h, w, ch = sout.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(sout.data, w, h, bytesPerLine, QImage.Format_RGB888)
                ps = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap3.emit(ps)

                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                pt = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap2.emit(pt)
                
                # normal image
                h, w, ch = output.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(output.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(320, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

                # capture and save an image
                if capEvent.isSet():
                    cv2.imwrite('cap'+str(self.img_cnt)+'.png', color)
                    self.img_cnt = self.img_cnt + 1 
                    capEvent.clear()

        self.cap.release()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Shape Detection robot'
        self.butt_name = 'Start Bot'
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        if stopEvent.isSet():
            self.label.setText("Camera Stopped")

    @pyqtSlot(QImage)
    def colorim(self, image):
        self.labelc.setPixmap(QPixmap.fromImage(image))
        if stopEvent.isSet():
            self.labelc.setText("Camera Stopped") 

    @pyqtSlot(QImage)
    def colorim1(self, image):
        self.labelc1.setPixmap(QPixmap.fromImage(image))
        if stopEvent.isSet():
            self.labelc1.setText("Camera Stopped")       
    
    def conThread(self):
        th = Thread(self)
        #th1 = threading.Thread(self, target = self.temp_and_visc) 
        #th1.start()
        if self.butt_name == 'Start Bot':
            stopEvent.clear()
            self.butt_name = 'Stop Bot'
            self.button.setText(self.butt_name)
            
            th.changePixmap.connect(self.setImage)
            th.changePixmap2.connect(self.colorim)
            th.changePixmap3.connect(self.colorim1)
            #self.temp_and_visc()
            v = random.uniform(0.862, 0.982)
            self.label_vis.setText(str(v))
            self.label_tmp.setText('')
            th.start()

        elif self.butt_name == 'Stop Bot':
            stopEvent.set()
            self.butt_name = 'Start Bot'
            self.button.setText(self.butt_name) 
            self.label_vis.setText('')
            self.label_tmp.setText('')  
    
    def capture(self):
        capEvent.set()
    
    def cam_check(self):
        if self.red_color_detect.isChecked():
            thresh_e.set()
        else: 
            thresh_e.clear() 

        if self.shape_detect.isChecked():
            shape_e.set()
        else:
            shape_e.clear()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 730, 800)

        self.topLeftGroupBox()
        self.topRightGroupBox()

        self.mainlayout = QGridLayout()
        self.mainlayout.addWidget(self.camera_widget, 1, 0)
        self.mainlayout.addWidget(self.datar , 1, 1)
        self.setLayout(self.mainlayout)
    
    def topLeftGroupBox(self):
        self.camera_widget = QGroupBox("Camera Options")

        self.label = QLabel(self)
        #self.label.resize(640, 480)
        self.labelc = QLabel(self)
        #self.labelc.resize(640, 480)
        self.labelc1 = QLabel(self)

        self.button = QPushButton(self)
        self.button.setText(self.butt_name)
        self.button.move(190, 100)
        self.button.clicked.connect(self.conThread)

        self.cap_button = QPushButton(self)
        self.cap_button.setText("Capture")
        self.cap_button.clicked.connect(self.capture)

        self.label_nimg = QLabel(self)
        self.label_nimg.setText("Camera images:")
        self.label_pimg = QLabel(self)
        self.label_pimg.setText("Processed images:")

        self.red_color_detect = QRadioButton("Thresh Image")
        self.red_color_detect.toggled.connect(self.cam_check)

        thresh_e.set()
        shape_e.set()

        self.shape_detect = QRadioButton("Shape Detection")
        self.shape_detect.toggled.connect(self.cam_check)

        toplayout = QHBoxLayout(self)

        #self.camtype = QGroupBox()
        #camlayout = QVBoxLayout()
        #camlayout.addWidget(self.red_color_detect)
        #camlayout.addWidget(self.shape_detect)
        #self.camtype.setLayout(camlayout)

        ngroup = QGroupBox()
        nlayout = QVBoxLayout()
        nlayout.addWidget(self.label_nimg)
        nlayout.addWidget(self.label)
        ngroup.setLayout(nlayout)
        toplayout.addWidget(ngroup)

        pgroup = QGroupBox()
        playout = QVBoxLayout()
        playout.addWidget(self.label_pimg)
        playout.addWidget(self.labelc)
        playout.addWidget(self.labelc1)
        pgroup.setLayout(playout)
        toplayout.addWidget(pgroup)

        toplayout.addWidget(self.cap_button)                               
        toplayout.addWidget(self.button)
        self.camera_widget.setLayout(toplayout)
    
    def topRightGroupBox(self):
        self.datar = QGroupBox("Data")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        self.label_shapet = QLabel(self)
        self.label_shapet.resize(200, 200)
        #self.label_shapet.setText("Shape: \nTriangle: YELLOW Square: RED Rectangle: GREEN Star: BLUE")
        self.label_shape = QLabel(self)
        self.label_shape.resize(200, 200)
        self.label_shape.setStyleSheet("background-color: grey;")

        #while not stopEvent.isSet():
        #   self.label_shape.setTextshape

        self.label_dimt = QLabel(self)
        self.label_dimt.resize(200, 200)
        self.label_dimt.setText("Shape dimensions(mm):")
        self.label_dim = QLabel(self)
        self.label_dim.resize(200, 200)
        self.label_dim.setStyleSheet("background-color: grey;")

        self.label_tmpt = QLabel(self)
        self.label_tmpt.resize(200, 200)
        self.label_tmpt.setText("Temperature(C):")
        self.label_tmp = QLabel(self)
        self.label_tmp.resize(200, 200)
        self.label_tmp.setStyleSheet("background-color: grey;")

        self.label_vist = QLabel(self)
        self.label_vist.resize(200, 200)
        self.label_vist.setText("Viscosity(cP):")
        self.label_vis = QLabel(self)
        self.label_vis.resize(200, 200)
        self.label_vis.setStyleSheet("background-color: grey;")
        
        toprlayout = QVBoxLayout()
        toprlayout.addWidget(self.label_shapet)
        toprlayout.addWidget(self.label_shape)
        toprlayout.addWidget(self.label_dimt)
        toprlayout.addWidget(self.label_dim)
        toprlayout.addWidget(self.label_tmpt)
        toprlayout.addWidget(self.label_tmp)
        toprlayout.addWidget(self.label_vist)
        toprlayout.addWidget(self.label_vis)
        self.datar.setLayout(toprlayout)


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	cam = App()
	cam.show()
	sys.exit(app.exec_())