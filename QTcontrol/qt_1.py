from PyQt5.QtCore import Qt
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QWidget, QGridLayout)
import cv2
from threading import Event
import numpy as np
from shapeDetailer2 import shape_detailer


stopEvent =  Event()
capEvent = Event()
red_e = Event()
shape_e = Event()


class camalt():
    def shape_detect(self, c):
        shape = 'unknown'
        peri = cv2.arcLength(c, True)
        vertices = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(vertices) == 3:
            shape = 'triangle'
        elif len(vertices) == 4:
            x, y, width, height = cv2.boundingRect(vertices)
            aspectRatio = float(width) / height
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                shape = "square"
            else:
                shape = "rectangle"
        elif len(vertices) == 5:
            shape = "pentagon"
        elif len(vertices) == 10:
            shape = "star"
        else:
            shape = "circle"
        return shape
        
     
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    changePixmap2 = pyqtSignal(QImage)
    camalt = camalt()
    def run(self):
        self.img_cnt = 0
        num = 100
        sd = shape_detailer()
        self.cap = cv2.VideoCapture(1)
        while not stopEvent.isSet():
            ret, frame = self.cap.read()

            if ret:
                color = frame.copy()
                #color = sd.apply_brightness(color, 30)
                #color = sd.apply_contrast(color, 70)
                if red_e.isSet():
                # color image
                    color = sd.thresold(color)
                
                if shape_e.isSet():
                    color = sd.computeShape(color)
                
                rgbImage = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
                rgbImagef = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                h, w, ch = color.shape
                bytesPerLine = ch*w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap2.emit(p)

                # normal image
                convertToQtFormat = QImage(rgbImagef.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

                if capEvent.isSet():
                    cv2.imwrite('cap'+str(self.img_cnt)+'.png', color)
                    self.img_cnt = self.img_cnt + 1 
                    capEvent.clear()
        self.cap.release()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Camera'
        self.butt_name = 'Start Camera'
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
    
    def conThread(self):
        th = Thread(self) 
        if self.butt_name == 'Start Camera':
            stopEvent.clear()
            self.butt_name = 'Stop Camera'
            self.button.setText(self.butt_name)

            th.changePixmap.connect(self.setImage)
            th.changePixmap2.connect(self.colorim)
            th.start()

        elif self.butt_name == 'Stop Camera':
            stopEvent.set()
            self.butt_name = 'Start Camera'
            self.button.setText(self.butt_name)
    
    def capture(self):
        capEvent.set()
    
    def cam_check(self):
        if self.red_color_detect.isChecked():
            red_e.set()
        else: 
            red_e.clear() 

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
        self.label.resize(640, 480)
        self.labelc = QLabel(self)
        self.labelc.resize(640, 480)

        self.button = QPushButton(self)
        self.button.setText(self.butt_name)
        self.button.move(190, 100)
        self.button.clicked.connect(self.conThread)

        self.cap_button = QPushButton(self)
        self.cap_button.setText('Capture')
        self.cap_button.clicked.connect(self.capture)

        self.red_color_detect = QRadioButton("Thresh Image")
        self.red_color_detect.toggled.connect(self.cam_check)

        self.shape_detect = QRadioButton("Shape Detection")
        self.shape_detect.toggled.connect(self.cam_check)

        toplayout = QVBoxLayout()

        self.camtype = QGroupBox()
        camlayout = QVBoxLayout()
        camlayout.addWidget(self.red_color_detect)
        camlayout.addWidget(self.shape_detect)
        self.camtype.setLayout(camlayout)

        toplayout.addWidget(self.label)
        toplayout.addWidget(self.camtype)
        toplayout.addWidget(self.labelc)
        toplayout.addWidget(self.cap_button)                               
        toplayout.addWidget(self.button)
        self.camera_widget.setLayout(toplayout)
    
    def topRightGroupBox(self):
        self.datar = QGroupBox("Data")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        self.labeld = QLabel(self)
        self.labeld.resize(700,700)

        toprlayout = QVBoxLayout()
        toprlayout.addWidget(self.labeld)
        self.datar.setLayout(toprlayout)


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	cam = App()
	cam.show()
	sys.exit(app.exec_())