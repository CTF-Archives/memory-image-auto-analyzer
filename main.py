import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction
import qdarkstyle
import logging
from qtawesome import icon
from layout.window_log import LogWindow
from layout.tab_general import Tab_General
from layout.tab_basicinfo import Tab_BasicInfo
from backend.vol import vol_backend_v2
from backend.core import core_control, core_res

os.environ["QT_API"] = "pyside6"
res = ""
DEBUG = False
dark_mode = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory image auto-analyzer")
        self.setMinimumSize(1300, 700)

        # 设置框体部件
        self.LogWindow = LogWindow()
        self.set_Tabs()
        self.set_MenuBar()

    def set_MenuBar(self):
        menu_bar = self.menuBar()
        menu_bar.setContextMenuPolicy(Qt.PreventContextMenu)  # 禁用右键菜单
        menu_bar_size = menu_bar.font()
        menu_bar_size.setPointSize(9)
        menu_bar.setFont(menu_bar_size)

        # 设置文件菜单栏
        menu_file = menu_bar.addMenu(" {} ".format("文件"))
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
        menu_help = menu_bar.addMenu(" {} ".format("帮助"))
        menu_help.setFont(menu_bar_size)
        action_ShowLog = QAction(icon("ri.newspaper-line"), "显示日志窗口", self)
        action_ShowLog.setStatusTip("显示程序日志")
        action_ShowLog.triggered.connect(self.show_log)
        menu_help.addAction(action_ShowLog)
        action_Debug = QAction(icon("ri.newspaper-line"), "Debug 显示输出", self)
        action_Debug.setStatusTip("打印最新一次输出")
        action_Debug.triggered.connect(self.Tab_BasicInfo.Tab_ClearContents)
        menu_help.addAction(action_Debug)

    def set_Tabs(self):
        """
        设置结果输出页面
        """
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        # 概览信息页面
        self.Tab_General = Tab_General()
        self.Tab_General.Btn_start.clicked.connect(self.process_General)
        self.Tab_General.Combo_profile.currentTextChanged.connect(self.set_profile)
        self.tabWidget.addTab(self.Tab_General, "镜像信息")

        # 基础信息页面
        self.Tab_BasicInfo = Tab_BasicInfo()
        self.Tab_BasicInfo.Btn_start.pressed.connect(self.process_BasicInfo)
        self.tabWidget.addTab(self.Tab_BasicInfo, "基础信息")

        # 进程信息页面
        # TODO 做一个专门展示进程信息的TabWidget

    def process_General(self):
        self.start_process("General")

    def process_BasicInfo(self):
        self.start_process("BasicInfo")

    def set_profile(self):
        core_control.config["profile"] = self.Tab_General.Combo_profile.currentText()
        logging.info("select profile:" + self.Tab_General.Combo_profile.currentText())
        logging.debug("current config:" + str(core_control.config))

    def show_log(self):
        self.LogWindow.show()

    def print_res(self):
        """
        仅为测试用,用于测试数据输出
        """
        module = "iehistory"
        res = core_res.get_res(module)
        print(res)
        res = core_res.format_res(res, module)
        print(res)

    # 选取镜像文件
    def OpenFile(self):
        filename = QFileDialog.getOpenFileName(parent=self, caption="选择镜像文件", dir=".", filter="*")[0]
        if filename:
            core_control.config["imagefile"] = filename
            logging.info("select image file:" + filename)

    def start_process(self, module: str):
        """
        开始启动分析线程，仅在这里使用集合化模块指令
        """
        if not core_control.check_imagefile(self):
            return 0
        if core_control.VolProcess is None:
            logging.info("Executing process: {}".format(module))
            match module:
                case "General":
                    self.Tab_General.Btn_start.setEnabled(False)
                    self.Tab_General.Tab_ClearContents()
                    self.Tab_General.Btn_start.setText("分析中")
                    core_control.VolProcess = [vol_backend_v2(core_control.config["imagefile"], "imageinfo", self.Tab_General.process_finished)]
                    core_res.clear_res("imageinfo")
                    for i in core_control.VolProcess:
                        i.run()
                case "BasicInfo":
                    if core_control.check_profile(self):
                        for i in core_control.BasicInfo_modules:
                            core_res.clear_res(i)
                        self.Tab_BasicInfo.Tab_ClearContents()
                        # 设置状态变量，跟踪所有子线程是否都已经完成
                        core_control.BasicInfo_status = 0
                        self.Tab_BasicInfo.Btn_start.setEnabled(False)
                        self.Tab_BasicInfo.Btn_start.setText("分析中")
                        # 核心线程储存变量使用列表对象进行复用
                        core_control.VolProcess = [
                            vol_backend_v2(core_control.config["imagefile"], "pslist", self.Tab_BasicInfo.process_finished_pslist, profile=core_control.config["profile"]),
                            vol_backend_v2(core_control.config["imagefile"], "filescan", self.Tab_BasicInfo.process_finished_filescan, profile=core_control.config["profile"]),
                            vol_backend_v2(core_control.config["imagefile"], "cmdline", self.Tab_BasicInfo.process_finished_cmdline, profile=core_control.config["profile"]),
                            vol_backend_v2(core_control.config["imagefile"], "iehistory", self.Tab_BasicInfo.process_finished_iehistory, profile=core_control.config["profile"]),
                        ]
                        for i in core_control.VolProcess:
                            i.run()
        else:
            self.warning_ProcessConflict()
            return 0

    def warning_ProcessConflict(self):
        logging.warning("程序正忙")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning!")
        dlg.setText("当前正在运行: {muddle_name}".format(muddle_name=", ".join([i.module for i in core_control.VolProcess])))
        dlg.exec()

    def closeEvent(self, event):
        """
        覆写程序关闭行为
        """
        for window in QApplication.topLevelWidgets():
            window.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if dark_mode:
        app.setStyleSheet(qdarkstyle.load_stylesheet())
    if DEBUG:
        core_control.config = {"imagefile": "/home/randark/Snapshot19.vmem", "profile": "Win7SP1x64"}
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
