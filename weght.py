import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainWindow import *
import requests
from ui.text_UI import text_UI
import uuid

def get_mac_address():

    node = uuid.getnode()

    mac = uuid.UUID(int = node).hex[-12:]
    print(mac)
get_mac_address()
def urlPing():
    url='https://www.baidu.com'
    response = requests.request("GET", url)
    return(response.status_code)

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        urlCode=urlPing()
        if urlCode!=int('200'):
            print(1)
            self.show_message()
            self.closeEvent()

        # urlCode=urlPing()
        # if urlCode==int('200'):
        #     print(1)
        #     self.show_message()


        else:

            print(2)
            self.setupUi(self)
            self.pushButton.clicked.connect(self.showText)
    def show_message(self):
        QtWidgets.QMessageBox.critical(self, "错误", "主机未联网")


    def showText(self):
        """开始截图"""
        self.hide()
        # time.sleep(0.2)  # 保证隐藏窗口
        # pixmap = self.screen.grabWindow(0)
        # painter = QPainter()
        # painter.setOpacity(0.5)
        # painter.begin(pixmap)
        # painter.end()
        self.label = ScreenLabel()
        # self.label.setPixmap(pixmap)
        self.label.showFullScreen()
        self.label.signal.connect(self.callback)
    def callback(self, pixmap):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        dialog = ShotDialog(pixmap)
        dialog.exec_()

        if not self.isMinimized():
            self.show()  # 截图完成显示窗口


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
