from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction
import sys

# 创建 QApplication 实例
app = QApplication(sys.argv)

# 创建 QWidget 实例
window = QWidget()

# 创建 QTableWidget 实例
table_widget = QTableWidget()

# 定义表格数据
data = [
    ['A1', 'B1', 'C1'],
    ['A2', 'B2', 'C2'],
    ['A3', 'B3', 'C3']
]

# 设置表格的行数和列数
table_widget.setRowCount(len(data))
table_widget.setColumnCount(len(data[0]))

# 将数据添加到表格中
for i, row in enumerate(data):
    for j, item in enumerate(row):
        table_widget.setItem(i, j, QTableWidgetItem(item))

# 设置表头标签
header_labels = ['Column 1', 'Column 2', 'Column 3']
table_widget.setHorizontalHeaderLabels(header_labels)

# 设置第一列的宽度为固定值
table_widget.setColumnWidth(0, 100)

# 设置其他列的宽度自适应窗口大小
table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

# 创建垂直布局管理器，并设置窗口的布局为该管理器
layout = QVBoxLayout()
window.setLayout(layout)

# 将表格添加到布局中
layout.addWidget(table_widget)

# 显示窗口
window.show()

# 运行应用程序
sys.exit(app.exec())