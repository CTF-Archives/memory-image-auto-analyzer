import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction
import qdarkstyle
import logging
from qtawesome import icon
from layout.window_log import LogWindow
from backend.vol import vol_backend_v2
from backend.res import core_res

os.environ['QT_API'] = 'pyside6'

config = {"imagefile": "", "profile": ""}

res = ""

DEBUG = True


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        if DEBUG == True:
            config["profile"] = "Win7SP1x64"
            config["imagefile"] = "/home/randark/Snapshot6.vmem"

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
        action_ShowRes = QAction(icon("ri.newspaper-line"), "Debug 显示输出", self)
        action_ShowRes.setStatusTip("打印最新一次输出")
        action_ShowRes.triggered.connect(self.print_res)
        menu_help.addAction(action_ShowRes)

    def setResultBlok(self):
        """
        设置结果输出页面
        """
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        # 镜像文件信息页面
        self.Tab_ImageInfo = QWidget()
        self.tabWidget.addTab(self.Tab_ImageInfo, "镜像信息")
        self.set_tab_ImageInfo()

        # 基础信息页面
        self.Tab_BasicInfo = QWidget()
        self.tabWidget.addTab(self.Tab_BasicInfo, "基础信息")
        self.set_tab_BasicInfo()

        # 进程信息页面
        # TODO 做一个专门展示进程信息的TabWidget

    def process_ImageInfo(self):
        self.start_process("ImageInfo")

    def set_tab_ImageInfo(self):
        # 设置主布局
        Tab_ImageInfo_pagelayout = QVBoxLayout()
        self.Tab_ImageInfo.setLayout(Tab_ImageInfo_pagelayout)
        Tab_ImageInfo_control_layout = QHBoxLayout()
        Tab_ImageInfo_info_layout = QVBoxLayout()
        Tab_ImageInfo_pagelayout.addLayout(Tab_ImageInfo_control_layout)
        Tab_ImageInfo_pagelayout.addLayout(Tab_ImageInfo_info_layout)
        # 设置第一栏控制栏, 开始分析的按钮
        self.Btn_ImageInfo_start = QPushButton("开始分析")
        self.Btn_ImageInfo_start.clicked.connect(self.process_ImageInfo)
        Tab_ImageInfo_control_layout.addWidget(self.Btn_ImageInfo_start)
        # 导出报告的按钮
        self.Btn_ImageInfo_export = QPushButton("导出报告")
        # TODO 增加导出报告的功能
        Tab_ImageInfo_control_layout.addWidget(self.Btn_ImageInfo_export)
        # 显示Profile的标签
        self.Label_Imageinfo = QLabel("Profile:")
        self.Label_Imageinfo.setFixedWidth(50)
        Tab_ImageInfo_control_layout.addWidget(self.Label_Imageinfo)
        # 选择Profile的下拉框
        self.Combo_profile = QComboBox()
        self.Combo_profile.addItem("还未分析")
        self.Combo_profile.currentTextChanged.connect(self.set_profile)
        Tab_ImageInfo_control_layout.addWidget(self.Combo_profile)

        # 设置第二栏信息输出栏
        self.Tab_ImageInfo_res = QTableWidget()
        Tab_ImageInfo_info_layout.addWidget(self.Tab_ImageInfo_res)

        # 设置表格输出形式
        self.Tab_ImageInfo_res.setRowCount(5)
        horizontal_header_labels = ['Key', 'Value']
        self.Tab_ImageInfo_res.setColumnCount(len(horizontal_header_labels))
        self.Tab_ImageInfo_res.setHorizontalHeaderLabels(horizontal_header_labels)
        # 设置平滑滚动
        self.Tab_ImageInfo_res.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.Tab_ImageInfo_res.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.Tab_ImageInfo_res.horizontalScrollBar().setSingleStep(10)
        self.Tab_ImageInfo_res.verticalScrollBar().setSingleStep(10)
        # 将 QTableWidget 设置为不可编辑
        self.Tab_ImageInfo_res.setEditTriggers(QTableWidget.NoEditTriggers)
        # 隐藏垂直方向表头
        self.Tab_ImageInfo_res.verticalHeader().setVisible(False)
        # 设置 Key 列的宽度为 100
        self.Tab_ImageInfo_res.setColumnWidth(0, 250)
        self.Tab_ImageInfo_res.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def process_BasicInfo(self):
        self.start_process("BasicInfo")

    def set_profile(self):
        config["profile"] = self.Combo_profile.currentText()
        logging.info("select profile:" + self.Combo_profile.currentText())
        logging.debug("current config:" + str(config))

    def set_tab_BasicInfo(self):
        """
        设置BasicInfo标签页
        """
        # 设置主布局
        Tab_BasicInfo_pagelayout = QVBoxLayout()
        self.Tab_BasicInfo.setLayout(Tab_BasicInfo_pagelayout)
        Tab_BasicInfo_button_layout = QHBoxLayout()
        Tab_BasicInfo_info_layout = QVBoxLayout()
        Tab_BasicInfo_pagelayout.addLayout(Tab_BasicInfo_button_layout)
        Tab_BasicInfo_pagelayout.addLayout(Tab_BasicInfo_info_layout)

        # 设置子窗口
        self.Tab_BasicInfo_result = QTabWidget()
        Tab_BasicInfo_info_layout.addWidget(self.Tab_BasicInfo_result)
        Tab_BasicInfo_subtab_pslist = QWidget()
        Tab_BasicInfo_subtab_cmdline = QWidget()
        Tab_BasicInfo_subtab_iehistory = QWidget()
        self.Tab_BasicInfo_result.addTab(Tab_BasicInfo_subtab_pslist, "pslist")
        self.Tab_BasicInfo_result.addTab(Tab_BasicInfo_subtab_cmdline, "cmdline")
        self.Tab_BasicInfo_result.addTab(Tab_BasicInfo_subtab_iehistory, "iehistory")
        # 设置第一栏控制栏, 开始分析的按钮
        self.Btn_BasicInfo_start = QPushButton("开始分析")
        self.Btn_BasicInfo_start.pressed.connect(self.process_BasicInfo)
        Tab_BasicInfo_button_layout.addWidget(self.Btn_BasicInfo_start)
        # 导出报告的按钮
        self.Btn_BasicInfo_export = QPushButton("保存报告")
        Tab_BasicInfo_button_layout.addWidget(self.Btn_BasicInfo_export)
        # 设置pslist模块的页面
        self.set_tab_BasicInfo_pslist(Tab_BasicInfo_subtab_pslist)

    def set_tab_BasicInfo_pslist(self,subtab:QWidget):
        Tab_BasicInfo_pslist_pagelayout = QVBoxLayout()
        subtab.setLayout(Tab_BasicInfo_pslist_pagelayout)
        Tab_BasicInfo_pslist_control_layout = QHBoxLayout()
        Tab_BasicInfo_pslist_info_layout = QVBoxLayout()
        Tab_BasicInfo_pslist_pagelayout.addLayout(Tab_BasicInfo_pslist_control_layout)
        Tab_BasicInfo_pslist_pagelayout.addLayout(Tab_BasicInfo_pslist_info_layout)
        # 设置信息输出栏
        self.Tab_BasicInfo_pslist_res = QTableWidget()
        Tab_BasicInfo_pslist_info_layout.addWidget(self.Tab_BasicInfo_pslist_res)
        # 设置表格输出形式
        self.Tab_BasicInfo_pslist_res.setRowCount(5)
        horizontal_header_labels = ["Offset(V)", "Name","PID","PPID","Thds","Hnds","Sess","Wow64","Start"]
        self.Tab_BasicInfo_pslist_res.setColumnCount(len(horizontal_header_labels))
        self.Tab_BasicInfo_pslist_res.setHorizontalHeaderLabels(horizontal_header_labels)
        # 设置平滑滚动
        self.Tab_BasicInfo_pslist_res.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.Tab_BasicInfo_pslist_res.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.Tab_BasicInfo_pslist_res.horizontalScrollBar().setSingleStep(10)
        self.Tab_BasicInfo_pslist_res.verticalScrollBar().setSingleStep(10)
        # 将 QTableWidget 设置为不可编辑
        self.Tab_BasicInfo_pslist_res.setEditTriggers(QTableWidget.NoEditTriggers)
        # 隐藏垂直方向表头
        self.Tab_BasicInfo_pslist_res.verticalHeader().setVisible(False)
        # 设置列的宽度
        self.Tab_BasicInfo_pslist_res.setColumnWidth(0, 150)
        self.Tab_BasicInfo_pslist_res.setColumnWidth(1, 150)
        self.Tab_BasicInfo_pslist_res.setColumnWidth(8, 250)

    def show_log(self):
        self.w.show()

    def print_res(self):
        """
        仅为测试用,用于测试数据输出
        """
        module = "pslist"
        res = core_res.get_res(module)
        print(res)
        res = core_res.sort_res(res, module)
        print(res)

    # 选取镜像文件
    def OpenFile(self):
        filename = QFileDialog.getOpenFileName(parent=self, caption='选择镜像文件', dir='.', filter='*')[0]
        if filename:
            config["imagefile"] = filename
            logging.info("select image file:" + filename)

    def start_process(self, module: str, profile=None):
        """
        开始启动分析线程，仅在这里使用集合化模块指令
        """
        if config["imagefile"] == "":
            logging.warning("未指定文件")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            dlg.setText("未选择有效的内存镜像文件!")
            dlg.exec()
            return 0
        if self.process_vol_v2 is None:  # No process running.
            logging.info("Executing process")
            if module == "ImageInfo":
                self.Btn_ImageInfo_start.setEnabled(False)
                self.Tab_ImageInfo_res.clearContents()
                self.Btn_ImageInfo_start.setText("分析中")
                self.process_vol_v2 = vol_backend_v2(config["imagefile"], "imageinfo", self.process_finished_imageinfo)
                core_res.clear_res("imageinfo")
                self.process_vol_v2.run()
            elif config["imagefile"] != "":
                if module == "BasicInfo":
                    sub_modules = ["pslist", "cmdline", "iehistory"]
                    for i in sub_modules:
                        core_res.clear_res(i)
                    # 设置状态变量，跟踪所有子线程是否都已经完成
                    self.Status_BasicInfo = 0
                    self.Btn_BasicInfo_start.setEnabled(False)
                    self.Btn_BasicInfo_start.setText("分析中")
                    self.process_vol_v2 = [
                        vol_backend_v2(config["imagefile"], "pslist", self.process_finished_pslist, profile=config["profile"]),
                        # vol_backend_v2(config["imagefile"], "cmdline", self.process_finished_cmdline, profile=config["profile"]),
                        # vol_backend_v2(config["imagefile"], "iehistory", self.process_finished_iehistory, profile=config["profile"])
                    ]
                    for i in self.process_vol_v2:
                        i.run()
        else:
            logging.warning("程序正忙")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            dlg.setText("当前存在其他模块正在运行!")
            dlg.exec()
            return 0

    def process_finished_imageinfo(self):
        """
        imageinfo模块执行完毕
        """
        logging.info("Process finished.")
        self.process_vol_v2 = None
        self.Btn_ImageInfo_start.setEnabled(True)
        self.Btn_ImageInfo_start.setText("开始分析")
        res = core_res.get_res("imageinfo")
        res = core_res.sort_res(res, "imageinfo")
        # 设置表格的行数和列数
        self.Tab_ImageInfo_res.setRowCount(len(res))
        self.Tab_ImageInfo_res.setColumnCount(len(res[0]))
        # 遍历二维数组，将数据添加到表格中
        for i, row in enumerate(res):
            for j, item in enumerate(row):
                # 创建 QTableWidgetItem 实例，并设置文本
                table_item = QTableWidgetItem(item)
                # 将 QTableWidgetItem 添加到表格的指定位置
                self.Tab_ImageInfo_res.setItem(i, j, table_item)
        # 设置 Key 列的文本居中对齐
        key_column = 0
        for row in range(self.Tab_ImageInfo_res.rowCount()):
            self.Tab_ImageInfo_res.item(row, key_column).setTextAlignment(Qt.AlignCenter)
        self.Combo_profile.clear()
        for i in res[0][1].split(","):
            self.Combo_profile.addItem(i.strip())

    def process_finished_pslist(self):
        logging.info("Process finished.")
        res = core_res.get_res("pslist")
        res = core_res.sort_res(res, "pslist")

        # 设置表格的行数和列数
        self.Tab_BasicInfo_pslist_res.setRowCount(len(res))
        self.Tab_BasicInfo_pslist_res.setColumnCount(len(res[0]))
        # 遍历二维数组，将数据添加到表格中
        for i, row in enumerate(res):
            for j, item in enumerate(row):
                # 创建 QTableWidgetItem 实例，并设置文本
                table_item = QTableWidgetItem(item)
                # 将 QTableWidgetItem 添加到表格的指定位置
                self.Tab_BasicInfo_pslist_res.setItem(i, j, table_item)
        # 设置 Key 列的文本居中对齐
        key_column = 0
        for row in range(self.Tab_BasicInfo_pslist_res.rowCount()):
            self.Tab_BasicInfo_pslist_res.item(row, key_column).setTextAlignment(Qt.AlignCenter)
        self.Combo_profile.clear()
        for i in res[0][1].split(","):
            self.Combo_profile.addItem(i.strip())

        self.Status_BasicInfo += 1
        if self.Status_BasicInfo == 3:
            self.process_vol_v2 = None
            self.Btn_BasicInfo_start.setEnabled(True)
            self.Btn_BasicInfo_start.setText("开始分析")

    def process_finished_cmdline(self):
        res = core_res.get_res("cmdline")
        self.Status_BasicInfo += 1
        if self.Status_BasicInfo == 3:
            self.process_vol_v2 = None
            self.Btn_BasicInfo_start.setEnabled(True)
            self.Btn_BasicInfo_start.setText("开始分析")

    def process_finished_iehistory(self):
        res = core_res.get_res("iehistory")
        self.Status_BasicInfo += 1
        if self.Status_BasicInfo == 3:
            self.process_vol_v2 = None
            self.Btn_BasicInfo_start.setEnabled(True)
            self.Btn_BasicInfo_start.setText("开始分析")

    def closeEvent(self, event):
        """
        覆写程序关闭行为
        """
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