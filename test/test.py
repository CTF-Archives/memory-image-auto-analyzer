import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QWidget
from PySide6.QtCore import Qt
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__(parent=None)
        self.centralwidget = QWidget()  # QMainWindow必须
        # 菜单栏
        self.menuBar = QMenuBar(self.centralwidget)
        self.setMenuBar(self.menuBar)
        self.topAction = QAction('&窗口置顶', self.centralwidget)
        self.topAction.triggered.connect(self.toggle_topmost)
        self.menuBar.addAction(self.topAction)
    def toggle_topmost(self):
        # 切换窗口的置顶状态
        if self.windowFlags() & Qt.WindowType.WindowStaysOnTopHint:
            self.topAction.setText("窗口置顶")
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.topAction.setText("取消置顶")
        # 更新窗口的显示
        self.show()
if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
