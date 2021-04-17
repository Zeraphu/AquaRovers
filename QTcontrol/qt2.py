
from PyQt5.QtCore import Qt
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QWidget, QGridLayout)
import cv2
#from threading import Thread
import numpy as np
from shapeDetailer2 import shape_detailer
import sys


sd = shape_detailer()

class App(QWidget):

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Video Receiver')
        self.setGeometry(100, 100, 1800, 900)

        self.label1 = QLabel(self)
        self.label1.resize(640,480)

        #self.label2 = QLabel(self)
        #self.label2.move(660, 0)
        #self.label2.resize(640,480)

        self.th1 = Thread(self)
        self.th1.changePixmap.connect(self.label1.setPixmap)
        self.th1.start()
        #self.th1.join()

        #self.th2 = Thread(self)
        #self.th2.port = 8001
        #self.th2.changePixmap.connect(self.label2.setPixmap)
        #self.th2.start()

       # self.threads = [self.th1]

        #for t in self.threads:
         #   t.join()

class Thread(QThread):

    changePixmap = pyqtSignal(QPixmap)

    def __init__(self, parent=None):

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        QThread.__init__(self, parent = parent)
        self.isRunning = True

    def run(self):

        cap = cv2.VideoCapture(0)

        while(True):

            ret, frame = cap.read()

            frame = sd.computeShape(frame)

            result, rgbImage = cv2.imencode('.jpg', frame, encode_param)
            rgbImage = cv2.cvtColor(frame, cv2.BGR2RGB)

            h, w, ch = rgbImage.shape
            bytesPerLine = ch*w

            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage[0], bytesPerLine, QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

            k = cv2.waitKey(2) & 0xFF

            changePixmap.emit(p)

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())