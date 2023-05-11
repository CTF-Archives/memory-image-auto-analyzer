import sys
import os
from PySide6.QtCore import QProcess, QSize, QSettings
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction, QIcon
import qdarkstyle
import logging
import icon.icon_rc
from layout.QTextEditLogger import QTextEditLogger
from backend.vol import Worker

os.environ['QT_API'] = 'pyside6'

config = {"imagefile": ""}


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Memory image auto-analyzer")

        # 设置项储存
        self.settings = QSettings()

        # 设置菜单栏
        self.set_MenuBar()

        # 设置状态栏
        self.setStatusBar(QStatusBar(self))

        layout = QGridLayout()
        self.setLayout(layout)

        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

        self.groupbox = QGroupBox("GroupBox Example")
        layout.addWidget(self.groupbox)

        self.logTextBox = QTextEditLogger(self)
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        vbox = QVBoxLayout()
        self.groupbox.setLayout(vbox)
        vbox.addWidget(self.logTextBox.widget)

        button_action = QAction("add log", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.add_log)
        self.toolbar.addAction(button_action)

        button_action = QAction("show log", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.show_log)
        self.toolbar.addAction(button_action)

        button_action = QAction("hide log", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.hide_log)
        self.toolbar.addAction(button_action)

        button_action = QAction("select file", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.OpenFIle)
        self.toolbar.addAction(button_action)

        button_action = QAction("imageinfo", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.start_process)
        self.toolbar.addAction(button_action)

        self.p = None

    def set_MenuBar(self):
        menu_bar = self.menuBar()

        # 设置文件菜单栏
        file_menu = menu_bar.addMenu("文件")
        action_OpenNewFile = QAction(QIcon(":file-new.svg"), "打开内存镜像文件", self)
        action_OpenNewFile.setStatusTip("打开内存镜像文件")
        action_OpenNewFile.triggered.connect(self.OpenFIle)
        file_menu.addAction(action_OpenNewFile)

        # 增加分隔
        file_menu.addSeparator()

    def hide_log(self):
        self.groupbox.setVisible(False)

    def show_log(self):
        self.groupbox.setVisible(True)

    def add_log(self, s):
        logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')

    def OpenFIle(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='*')
        if filename:
            print(filename)
            config["imagefile"] = filename
            logging.info("select image file:" + filename)

    def message(self, s):
        logging.info(s)

    def start_process(self):
        if config["imagefile"] == "":
            logging.warning("未指定文件")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            dlg.setText("未选择有效的内存镜像文件!")
            dlg.exec_()
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
    # faulthandler.enable(open("./test.out", "w+"), all_threads=True)
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    app.exec()