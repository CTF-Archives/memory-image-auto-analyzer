from PySide6.QtWidgets import *


class Subtab_Pslist(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        Tab_pagelayout = QVBoxLayout()
        self.setLayout(Tab_pagelayout)
        Tab_info_layout = QVBoxLayout()
        Tab_pagelayout.addLayout(Tab_info_layout)

        # 设置信息输出栏
        self.Tab_res = QTableWidget()
        Tab_info_layout.addWidget(self.Tab_res)

        # 设置表格输出形式
        self.Tab_res.setRowCount(5)
        horizontal_header_labels = [
            "Offset(V)",
            "Name",
            "PID",
            "PPID",
            "Thds",
            "Hnds",
            "Sess",
            "Wow64",
            "Start",
        ]
        self.Tab_res.setColumnCount(len(horizontal_header_labels))
        self.Tab_res.setHorizontalHeaderLabels(horizontal_header_labels)

        # 设置平滑滚动
        self.Tab_res.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.Tab_res.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.Tab_res.horizontalScrollBar().setSingleStep(10)
        self.Tab_res.verticalScrollBar().setSingleStep(10)

        # 将 QTableWidget 设置为不可编辑
        self.Tab_res.setEditTriggers(QTableWidget.NoEditTriggers)

        # 隐藏垂直方向表头
        self.Tab_res.verticalHeader().setVisible(False)

        # 设置列的宽度
        self.Tab_res.setColumnWidth(0, 150)
        self.Tab_res.setColumnWidth(1, 150)
        self.Tab_res.setColumnWidth(8, 250)

    def Tab_ClearContents(self):
        self.Tab_res.clearContents()
