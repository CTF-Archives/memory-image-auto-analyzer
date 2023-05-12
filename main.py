import sys
import os
from PySide6.QtCore import QProcess, QSettings, Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction
import qdarkstyle
import logging
from qtawesome import icon
from layout.QTextEditLogger import QTextEditLogger
from backend.vol import Worker

os.environ['QT_API'] = 'pyside6'

config = {"imagefile": ""}


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Memory image auto-analyzer")
        self.setMinimumSize(800, 500)

        # 设置项储存
        # self.settings = QSettings()

        # 设置菜单栏
        self.set_MenuBar()

        # 设置状态栏
        self.setStatusBar(QStatusBar(self))

        # 设置日志窗体
        self.set_LogTextBox()

        # 设置工具栏
        self.set_ToolBar()

        self.ToolsBTN = QPushButton('go P1', self)
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.ToolsBTN)
        self.setCentralWidget(self.stack)
        self.show()

    def set_MenuBar(self):
        menu_bar = self.menuBar()
        menu_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        menu_bar_size = menu_bar.font()
        menu_bar_size.setPointSize(9)
        menu_bar.setFont(menu_bar_size)

        # 设置文件菜单栏
        menu_file = menu_bar.addMenu("文件")
        menu_file.setFont(menu_bar_size)
        action_OpenNewFile = QAction(icon("fa5.file"), "打开内存镜像文件", self)
        action_OpenNewFile.setStatusTip("打开内存镜像文件")
        action_OpenNewFile.triggered.connect(self.OpenFile)
        menu_file.addAction(action_OpenNewFile)
        menu_file.addSeparator()
        action_ApplicationQuit = QAction(icon("fa5s.door-open"), "退出", self)
        action_ApplicationQuit.setStatusTip("退出程序")
        action_ApplicationQuit.triggered.connect(self.ApplicationQuit)
        menu_file.addAction(action_ApplicationQuit)

        # 设置帮助菜单栏
        menu_help = menu_bar.addMenu("帮助")
        menu_help.setFont(menu_bar_size)
        action_ShowLog = QAction(icon("ri.newspaper-line"), "显示日志窗口", self)
        action_ShowLog.setStatusTip("显示程序日志")
        action_ShowLog.triggered.connect(self.show_log)
        menu_help.addAction(action_ShowLog)

    def set_ToolBar(self):
        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        button_action = QAction("show log", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.show_log)
        self.toolbar.addAction(button_action)

        button_action = QAction("imageinfo", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.start_process)
        self.toolbar.addAction(button_action)

    def set_LogTextBox(self):
        layout = QGridLayout()
        self.setLayout(layout)
        self.groupbox = QGroupBox("GroupBox Example")
        layout.addWidget(self.groupbox)

        self.logTextBox = QTextEditLogger(self)
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s\n--> module: %(module)s\n--> funcName: %(funcName)s\n--> %(message)s'))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        vbox = QVBoxLayout()
        self.groupbox.setLayout(vbox)
        vbox.addWidget(self.logTextBox.widget)

    def show_log(self):
        self.groupbox.setVisible(True)

    def OpenFile(self):
        filename = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='*')
        if filename:
            print(filename)
            config["imagefile"] = filename
            logging.info("select image file:" + filename)

    def ApplicationQuit(self):
        QApplication.instance, quit()

    def message(self, s):
        logging.info(s)

    def start_process(self):
        if config["imagefile"] == "":
            logging.warning("未指定文件")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            dlg.setText("未选择有效的内存镜像文件!")
            dlg.exec()
            return 0
        if self.p is None:  # No process running.
            self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("vol.py", ['-f', config["imagefile"], "imageinfo"])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    app.exec()