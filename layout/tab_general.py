from PySide6.QtWidgets import *
import logging
from backend.res import core_res
from backend.control import core_status
from PySide6.QtCore import Qt


class Tab_General(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_Tab_General()

    def set_Tab_General(self):
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

        # 显示Profile的标签
        self.Label_Profile = QLabel("Profile:")
        self.Label_Profile.setFixedWidth(50)
        Tab_control_layout.addWidget(self.Label_Profile)

        # 选择Profile的下拉框
        self.Combo_profile = QComboBox()
        self.Combo_profile.addItem("还未分析")
        Tab_control_layout.addWidget(self.Combo_profile)

        # 设置子选项卡
        from layout.subtab_imageinfo import Subtab_ImageInfo

        self.Subtab_ImageInfo = Subtab_ImageInfo()
        Tab_info_layout.addWidget(self.Subtab_ImageInfo)

    def process_finished(self):
        """
        imageinfo模块执行完毕
        """
        logging.info("Process finished.")
        core_status.VolProcess=None
        self.Btn_start.setEnabled(True)
        self.Btn_start.setText("开始分析")
        res = core_res.get_res("imageinfo")
        res = core_res.format_res(res, "imageinfo")
        # 设置表格的行数和列数
        self.Subtab_ImageInfo.setRowCount(len(res))
        self.Subtab_ImageInfo.setColumnCount(len(res[0]))
        # 遍历二维数组，将数据添加到表格中
        for i, row in enumerate(res):
            for j, item in enumerate(row):
                # 创建 QTableWidgetItem 实例，并设置文本
                table_item = QTableWidgetItem(item)
                # 将 QTableWidgetItem 添加到表格的指定位置
                self.Subtab_ImageInfo.setItem(i, j, table_item)
        # 设置 Key 列的文本居中对齐
        key_column = 0
        for row in range(self.Subtab_ImageInfo.rowCount()):
            self.Subtab_ImageInfo.item(row, key_column).setTextAlignment(Qt.AlignCenter)
        self.Combo_profile.clear()
        for i in res[0][1].split(","):
            self.Combo_profile.addItem(i.strip())
