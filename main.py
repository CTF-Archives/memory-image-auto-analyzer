import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction, QPalette, QColor
import qdarkstyle
import logging
from qtawesome import icon
from layout.window_log import LogWindow
from backend.vol import vol_backend_v2
from backend.res import core_res

os.environ['QT_API'] = 'pyside6'

config = {"imagefile": "", "profile": ""}

res = ""


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory image auto-analyzer")
        self.setMinimumSize(1000, 700)

        # 设置项储存
        # self.settings = QSettings()

        # 设置菜单栏
        self.set_MenuBar()

        # 设置状态栏
        self.setStatusBar(QStatusBar(self))

        # 设置变量
        self.process_vol_v2 = None
        self.w = LogWindow()
        self.w.show()
        self.w.hide()

        # 设置结果输出界面
        self.setResultBlok()

    def setResultBlok(self):
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        # 镜像文件信息页面
        Tab_ImageInfo_pagelayout = QVBoxLayout()
        Tab_ImageInfo_button_layout = QHBoxLayout()
        Tab_ImageInfo_info_layout = QVBoxLayout()

        Tab_ImageInfo_pagelayout.addLayout(Tab_ImageInfo_button_layout)
        Tab_ImageInfo_pagelayout.addLayout(Tab_ImageInfo_info_layout)

        Btn_ImageInfo_start = QPushButton("开始分析")
        Btn_ImageInfo_start.pressed.connect(self.start_process)
        Tab_ImageInfo_button_layout.addWidget(Btn_ImageInfo_start)

        Btn_ImageInfo_export = QPushButton("保存报告")
        Tab_ImageInfo_button_layout.addWidget(Btn_ImageInfo_export)

        # FIXME 镜像信息加上根据profile返回值更新的下拉框，以及展示界面，不使用TabWidget
        self.Tab_ImageInfo_child = QTabWidget()
        Tab_ImageInfo_info_layout.addWidget(self.Tab_ImageInfo_child)

        self.tab_result_raw = QWidget()
        self.tab_result_raw.setLayout(Tab_ImageInfo_pagelayout)
        self.set_tab_ImageInfo(self.Tab_ImageInfo_child)
        self.tabWidget.addTab(self.tab_result_raw, "镜像信息")

        # 基础信息页面
        Tab_BasicInfo_pagelayout = QVBoxLayout()
        Tab_BasicInfo_button_layout = QHBoxLayout()
        Tab_BasicInfo_info_layout = QVBoxLayout()

        Tab_BasicInfo_pagelayout.addLayout(Tab_BasicInfo_button_layout)
        Tab_BasicInfo_pagelayout.addLayout(Tab_BasicInfo_info_layout)

        Btn_BasicInfo_start = QPushButton("开始分析")
        Btn_BasicInfo_start.pressed.connect(self.start_process)
        Tab_BasicInfo_button_layout.addWidget(Btn_BasicInfo_start)

        Btn_BasicInfo_export = QPushButton("保存报告")
        Tab_BasicInfo_button_layout.addWidget(Btn_BasicInfo_export)

        self.Tab_BasicInfo_child = QTabWidget()
        Tab_BasicInfo_info_layout.addWidget(self.Tab_BasicInfo_child)

        self.tab_result_raw = QWidget()
        self.tab_result_raw.setLayout(Tab_BasicInfo_pagelayout)
        self.set_tab_BasicInfo(self.Tab_BasicInfo_child)
        self.tabWidget.addTab(self.tab_result_raw, "基础信息")

        # 进程信息页面
        # TODO 做一个专门展示进程信息的TabWidget
        pass

    def set_tab_BasicInfo(self, widget: QTabWidget):
        """
        设置BasicInfo标签页
        """
        Tab_BasicInfo_child_pslist = QWidget()
        Tab_BasicInfo_child_cmdline = QWidget()
        Tab_BasicInfo_child_iehistory = QWidget()
        widget.addTab(Tab_BasicInfo_child_pslist, "pslist")
        widget.addTab(Tab_BasicInfo_child_cmdline, "cmdline")
        widget.addTab(Tab_BasicInfo_child_iehistory, "iehistory")

    def set_tab_ImageInfo(self, widget: QTabWidget):
        pass

    def set_MenuBar(self):
        menu_bar = self.menuBar()
        menu_bar.setContextMenuPolicy(Qt.PreventContextMenu)  # 禁用右键菜单
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
        # 增加分隔符
        menu_file.addSeparator()
        action_ApplicationQuit = QAction(icon("fa5s.door-open"), "退出", self)
        action_ApplicationQuit.setStatusTip("退出程序")
        action_ApplicationQuit.triggered.connect(self.closeEvent)
        menu_file.addAction(action_ApplicationQuit)

        # 设置帮助菜单栏
        menu_help = menu_bar.addMenu("帮助")
        menu_help.setFont(menu_bar_size)
        action_ShowLog = QAction(icon("ri.newspaper-line"), "显示日志窗口", self)
        action_ShowLog.setStatusTip("显示程序日志")
        action_ShowLog.triggered.connect(self.show_log)
        menu_help.addAction(action_ShowLog)
        action_ShowRes = QAction(icon("ri.newspaper-line"), "Debug 显示输出", self)
        action_ShowRes.setStatusTip("打印最新一次输出")
        action_ShowRes.triggered.connect(self.print_res)
        menu_help.addAction(action_ShowRes)

    def show_log(self):
        self.w.show()

    def print_res(self):
        res = core_res.get_res()
        res = res.split("\n")
        res = [i for i in res if i != ""]
        res = [i.replace(" ", "").split(":") for i in res]
        print(res, sep="\n")

    # 选取镜像文件
    def OpenFile(self):
        filename = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='*')[0]
        if filename:
            config["imagefile"] = filename
            logging.info("select image file:" + filename)

    def start_process(self, module: str):
        if config["imagefile"] == "":
            logging.warning("未指定文件")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            dlg.setText("未选择有效的内存镜像文件!")
            dlg.exec()
            return 0
        if self.process_vol_v2 is None:  # No process running.
            # FIXME 解决多线程同时执行的问题
            logging.info("Executing process")
            self.process_vol_v2 = vol_backend_v2(self)
            self.process_vol_v2.func(config["imagefile"], "pslist", self.process_finished)
            self.process_vol_v2.func(config["imagefile"], "cmdline", self.process_finished)
            self.process_vol_v2.func(config["imagefile"], "iehistory", self.process_finished)

    def process_finished(self):
        logging.info("Process finished.")
        self.p = None

    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dark_mode = False
    if dark_mode:
        app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())