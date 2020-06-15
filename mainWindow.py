# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time
import requests
from configparser import ConfigParser
from win32clipboard import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui.dialog import Ui_Dialog
from ui.mainwindow import Ui_MainWindow
from ui.dialog import Ui_Dialog
#from ui.text_UI import text_UI
import baidu

class Ui_MainWindow(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(141, 321)
        self.pushButton_2 = QtWidgets.QPushButton(widget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 200, 75, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(widget)
        #self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(40, 90, 75, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "图文识别"))
        self.pushButton_2.setText(_translate("widget", "关闭"))
        self.pushButton.setText(_translate("widget", "截图"))



class Bbox(object):
    def __init__(self):
        self._x1, self._y1 = 0, 0
        self._x2, self._y2 = 0, 0

    @property
    def point1(self):
        return self._x1, self._y1

    @point1.setter
    def point1(self, position: tuple):
        self._x1 = position[0]
        self._y1 = position[1]

    @property
    def point2(self):
        return self._x2, self._y2

    @point2.setter
    def point2(self, position: tuple):
        self._empty = False
        self._x2 = position[0]
        self._y2 = position[1]

    @property
    def bbox(self):
        if self._x1 < self._x2:
            x_min, x_max = self._x1, self._x2
        else:
            x_min, x_max = self._x2, self._x1

        if self._y1 < self._y2:
            y_min, y_max = self._y1, self._y2
        else:
            y_min, y_max = self._y2, self._y1
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def __str__(self):
        return str(self.bbox)
class ScreenLabel(QLabel):
    signal = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self._press_flag = False
        self._bbox = Bbox()
        self._pen = QPen(Qt.white, 2, Qt.DashLine)
        self._painter = QPainter()
        self._bbox = Bbox()
        height = QApplication.desktop().screenGeometry().height()
        width = QApplication.desktop().screenGeometry().width()
        self._pixmap = QPixmap(width, height)
        self._pixmap.fill(QColor(255, 255, 255))
        self.setPixmap(self._pixmap)
        self.setWindowOpacity(0.4)

        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置背景颜色为透明

        QShortcut(QKeySequence("esc"), self, self.close)

        self.setWindowFlag(Qt.Tool)  # 不然exec_执行退出后整个程序退出

        # palette = QPalette()
        # palette.
        # self.setPalette()

    def _draw_bbox(self):
        pixmap = self._pixmap.copy()
        self._painter.begin(pixmap)
        self._painter.setPen(self._pen)  # 设置pen必须在begin后
        rect = QRect(*self._bbox.bbox)
        self._painter.fillRect(rect, Qt.SolidPattern)  # 区域不透明
        self._painter.drawRect(rect)  # 绘制虚线框
        self._painter.end()
        self.setPixmap(pixmap)
        self.update()
        self.showFullScreen()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("鼠标左键：", [QMouseEvent.x(), QMouseEvent.y()])
            self._press_flag = True
            self._bbox.point1 = [QMouseEvent.x(), QMouseEvent.y()]

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton and self._press_flag:
            print("鼠标释放：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._press_flag = False
            self.signal.emit(QRect(*self._bbox.bbox))

    def mouseMoveEvent(self, QMouseEvent):
        if self._press_flag:
            print("鼠标移动：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._draw_bbox()

class ShotDialog(QDialog, Ui_Dialog):
    def __init__(self, rect):
        super().__init__()
        self.setupUi(self)
        self.adjustSize()
        self.setWindowFlag(Qt.FramelessWindowHint)  # 没有窗口栏
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
        print(11)
        #self.pushButton_clipboard.clicked.connect(self.save_to_clipboard)
        print(12)
        #self.pushButton_markdown.clicked.connect(self.upload_to_picbed)
        print(13)
        self.pushButton_save.clicked.connect(self.save_local)
        print(14)
        self.pushButton_cancel.clicked.connect(self.close)

        self.label_shot.setPixmap(QApplication.primaryScreen().grabWindow(0).copy(rect))
        self.setWindowFlag(Qt.Tool)  # 不然exec_执行退出后整个程序退出

    def get_shot_img(self):
        return self.label_shot.pixmap().toImage()

    def get_shot_bytes(self):
        shot_bytes = QByteArray()
        buffer = QBuffer(shot_bytes)
        buffer.open(QIODevice.WriteOnly)
        shot_img = self.get_shot_img()
        shot_img.save(buffer, 'png')
        return shot_bytes.data()

    # def save_local(self):
    #     file, _ = QFileDialog.getSaveFileName(self, '保存到' './', 'screenshot.jpg',
    #                                           'Image files(*.jpg *.gif *.png)')
    #     if file:
    #         shot_img = self.get_shot_img()
    #         shot_img.save(file)
    #     self.close()
    def save_local(self):
        shot_img= self.get_shot_img()
        shot_img.save('upload.png')
        #resultText=baidu.get_text('./upload.png')
        dialogText = text_UI('123')
        try:
            dialogText.exec_()
        except (NameError, IndexError, PermissionError)  as e:
            print(e)
        self.close()

    def save_to_clipboard(self):
        shot_bytes = self.get_shot_bytes()
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(CF_BITMAP, shot_bytes[14:])
        CloseClipboard()
        self.close()

    def upload_to_picbed(self):
        shot_bytes = self.get_shot_bytes()
        filename = "shot" + str(time.time()).split('.')[0] + '.jpg'
        files = {
            "image_field": (filename, shot_bytes, "image/jpeg")
        }
        headers = {
            "Cookie": cfg.get("picbed", 'cookie')
        }
        try:
            res = requests.post(cfg.get("picbed", 'api'), files=files, headers=headers)
        except Exception as e:
            self.showMessage("requests error, message:".format(e))

        if res.status_code == 200:
            self.showMessage(res.json()['data']['img_url'])
        else:
            self.showMessage("http error, code: {}".format(res.status_code))
        self.close()

    def showMessage(self, message):
        dialog = QDialog()
        dialog.adjustSize()
        text = QLineEdit(message, dialog)
        text.adjustSize()
        dialog.exec_()



class text_UI(QDialog):
    def __init__(self,Mtext):
        super(text_UI, self).__init__()
        self.Mtext = Mtext
   # def setupUi(self, Dialog):
        self.setObjectName("Dialog")
        self.resize(604, 568)
        self.textBrowser = QtWidgets.QTextEdit(self)
        self.textBrowser.setGeometry(QtCore.QRect(20, 20, 571, 501))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 530, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(340, 530, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.setWindowTitle("文本")
        self.pushButton_2.setText( "撤销")
        self.pushButton_3.setText("复制全文")
        self.textBrowser.setText(self.Mtext)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.printT)
    def printT(self):
        #print()
        self.textBrowser.selectAll()
        cursor = self.textBrowser.textCursor()
        text = cursor.selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        #self.pushButton_3.clicked.connect(self.textBrowser.selectAll())
        # self.retranslateUi(Dialog)
        # self.pushButton_3.clicked.connect(self.textBrowser.copy)
        # QtCore.QMetaObject.connectSlotsByName(Dialog)

    # def retranslateUi(self):
    #     _translate = QtCore.QCoreApplication.translate




