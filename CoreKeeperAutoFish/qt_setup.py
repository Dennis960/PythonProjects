import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight, QtCore.Qt.AlignTop,
                QtCore.QSize(2560, 1440),
                QtWidgets.qApp.desktop().availableGeometry()
        ))
        # red box in the top right corner
        box = QtWidgets.QWidget(self)
        box.setStyleSheet("background-color: red;")
        box.setGeometry(2510, 0, 50, 50)

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()
