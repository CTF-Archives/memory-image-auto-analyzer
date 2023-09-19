from PySide6.QtWidgets import *
import logging
from PySide6.QtCore import Qt
from backend.core import core_control, core_res
from layout.subtab_pslist import Subtab_Pslist
from layout.subtab_filescan import Subtab_Filescan, TableModel
from layout.subtab_cmdline import Subtab_Cmdline
from layout.subtab_iehistory import Subtab_Iehistory


class Tab_BasicInfo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_Tab_BasicInfo()

    def set_Tab_BasicInfo(self):
        # 设置主布局
        Tab_pagelayout = QVBoxLayout()
        self.setLayout(Tab_pagelayout)
        Tab_button_layout = QHBoxLayout()
        Tab_info_layout = QVBoxLayout()
        Tab_pagelayout.addLayout(Tab_button_layout)
        Tab_pagelayout.addLayout(Tab_info_layout)
        self_result = QTabWidget()
        Tab_info_layout.addWidget(self_result)

        # 设置第一栏控制栏, 开始分析的按钮
        self.Btn_start = QPushButton("开始分析")
        Tab_button_layout.addWidget(self.Btn_start)

        # 导出报告的按钮
        self.Btn_BasicInfo_export = QPushButton("保存报告")
        Tab_button_layout.addWidget(self.Btn_BasicInfo_export)

        # 设置子窗口布局
        self.Subtab_Pslist = Subtab_Pslist()
        self.Subtab_Filescan = Subtab_Filescan()
        self.Subtab_Cmdline = Subtab_Cmdline()
        self.Subtab_Iehistory = Subtab_Iehistory()
        self_result.addTab(self.Subtab_Pslist, "pslist")
        self_result.addTab(self.Subtab_Filescan, "filescan")
        self_result.addTab(self.Subtab_Cmdline, "cmdline")
        self_result.addTab(self.Subtab_Iehistory, "iehistory")

    def process_finished_check(self):
        """
        对当前窗口的执行阶段进行检查，结束的话进行窗体复位
        """
        if core_control.BasicInfo_status == len(core_control.BasicInfo_modules):
            core_control.VolProcess = None
            self.Btn_start.setEnabled(True)
            self.Btn_start.setText("开始分析")

    def Tab_ClearContents(self):
        self.Subtab_Pslist.Tab_ClearContents()
        self.Subtab_Filescan.Tab_ClearContents()
        self.Subtab_Cmdline.Tab_ClearContents()
        self.Subtab_Iehistory.Tab_ClearContents()

    def process_finished_pslist(self):
        """
        pslist模块执行完毕
        """
        logging.info("Process finished.")
        res = core_res.get_res("pslist")
        res = core_res.format_res(res, "pslist")

        # 设置表格的行数和列数
        self.Subtab_Pslist.Tab_res.setRowCount(len(res))
        self.Subtab_Pslist.Tab_res.setColumnCount(len(res[0]))
        # 遍历二维数组，将数据添加到表格中
        for i, row in enumerate(res):
            for j, item in enumerate(row):
                # 创建 QTableWidgetItem 实例，并设置文本
                table_item = QTableWidgetItem(item)
                # 将 QTableWidgetItem 添加到表格的指定位置
                self.Subtab_Pslist.Tab_res.setItem(i, j, table_item)
        # 设置 Key 列的文本居中对齐
        key_column = 0
        for row in range(self.Subtab_Pslist.Tab_res.rowCount()):
            self.Subtab_Pslist.Tab_res.item(row, key_column).setTextAlignment(Qt.AlignCenter)

        core_control.BasicInfo_status += 1
        self.process_finished_check()

    def process_finished_filescan(self):
        """
        filescan模块执行完毕
        """
        res = core_res.get_res("filescan")
        res = core_res.format_res(res, "filescan")
        Tab_BasicInfo_filescan_res_model = TableModel(res, self.Subtab_Filescan.Tab_res_header)
        self.Subtab_Filescan.Tab_res_ProxyModel.setSourceModel(Tab_BasicInfo_filescan_res_model)
        self.Subtab_Filescan.Tab_res_ProxyModel.sort(0, Qt.AscendingOrder)
        self.Subtab_Filescan.Tab_res.setModel(self.Subtab_Filescan.Tab_res_ProxyModel)

        core_control.BasicInfo_status += 1
        self.process_finished_check()

    def process_finished_cmdline(self):
        """
        cmdline模块执行完毕
        """
        res = core_res.get_res("cmdline")
        res = core_res.format_res(res, "cmdline")

        # 设置表格的行数和列数
        self.Subtab_Cmdline.Tab_res.setRowCount(len(res))
        self.Subtab_Cmdline.Tab_res.setColumnCount(len(res[0]))
        # 遍历二维数组，将数据添加到表格中
        for i, row in enumerate(res):
            for j, item in enumerate(row):
                # 创建 QTableWidgetItem 实例，并设置文本
                table_item = QTableWidgetItem(item)
                # 将 QTableWidgetItem 添加到表格的指定位置
                self.Subtab_Cmdline.Tab_res.setItem(i, j, table_item)
        # 设置 Key 列的文本居中对齐
        key_column = 0
        for row in range(self.Subtab_Cmdline.Tab_res.rowCount()):
            self.Subtab_Cmdline.Tab_res.item(row, key_column).setTextAlignment(Qt.AlignCenter)

        core_control.BasicInfo_status += 1
        self.process_finished_check()

    def process_finished_iehistory(self):
        """
        iehistory模块执行完毕
        """
        res = core_res.get_res("iehistory")
        res = core_res.format_res(res, "iehistory")

        # 设置表格的行数和列数
        self.Subtab_Iehistory.Tab_res.setRowCount(len(res))
        self.Subtab_Iehistory.Tab_res.setColumnCount(len(res[0]))
        # 遍历二维数组，将数据添加到表格中
        for i, row in enumerate(res):
            for j, item in enumerate(row):
                # 创建 QTableWidgetItem 实例，并设置文本
                table_item = QTableWidgetItem(item)
                # 将 QTableWidgetItem 添加到表格的指定位置
                self.Subtab_Iehistory.Tab_res.setItem(i, j, table_item)
        # 设置 Key 列的文本居中对齐
        key_column = 0
        for row in range(self.Subtab_Iehistory.Tab_res.rowCount()):
            self.Subtab_Iehistory.Tab_res.item(row, key_column).setTextAlignment(Qt.AlignCenter)

        core_control.BasicInfo_status += 1
        self.process_finished_check()
