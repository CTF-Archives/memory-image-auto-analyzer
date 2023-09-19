from PySide6.QtWidgets import *
import logging
from backend.core import core_control, core_res
from PySide6.QtCore import Qt


class Tab_Credential(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_Tab_Credential()

    def set_Tab_Credential(self):
        # 设置主布局
        Tab_pagelayout = QVBoxLayout()
        self.setLayout(Tab_pagelayout)
        Tab_control_layout = QHBoxLayout()
        Tab_info_layout = QVBoxLayout()
        Tab_pagelayout.addLayout(Tab_control_layout)
        Tab_pagelayout.addLayout(Tab_info_layout)

        # 设置第一栏控制栏, 开始分析的按钮
        self.Btn_start = QPushButton("开始分析")

        Tab_control_layout.addWidget(self.Btn_start)
        # 导出报告的按钮
        self.Btn_export = QPushButton("导出报告")

        # TODO 增加导出报告的功能
        Tab_control_layout.addWidget(self.Btn_export)