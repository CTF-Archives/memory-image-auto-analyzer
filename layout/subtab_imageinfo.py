from PySide6.QtWidgets import *


class Subtab_ImageInfo(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置表格输出形式
        self.setRowCount(5)
        horizontal_header_labels = ["Key", "Value"]
        self.setColumnCount(len(horizontal_header_labels))
        self.setHorizontalHeaderLabels(horizontal_header_labels)

        # 设置平滑滚动
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalScrollBar().setSingleStep(10)
        self.verticalScrollBar().setSingleStep(10)

        # 将 QTableWidget 设置为不可编辑
        self.setEditTriggers(QTableWidget.NoEditTriggers)

        # 隐藏垂直方向表头
        self.verticalHeader().setVisible(False)

        # 设置 Key 列的宽度为 100
        self.setColumnWidth(0, 250)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
