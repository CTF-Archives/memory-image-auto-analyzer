from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self.headers = headers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]


class Subtab_Filescan(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        Tab_pagelayout = QVBoxLayout()
        self.setLayout(Tab_pagelayout)
        Tab_control_layout = QHBoxLayout()
        Tab_info_layout = QVBoxLayout()
        Tab_pagelayout.addLayout(Tab_control_layout)
        Tab_pagelayout.addLayout(Tab_info_layout)
        
        # 设置搜索栏
        self.Label_Search = QLabel("搜索（支持 regex ）:")
        
        # self.Label_Search.setFixedWidth(50)
        Tab_control_layout.addWidget(self.Label_Search)
        self.Tab_searchbar = QLineEdit()
        self.Tab_searchbar.textChanged.connect(self.set_filter_data)
        Tab_control_layout.addWidget(self.Tab_searchbar)
        
        # 设置信息输出栏
        self.Tab_res = QTableView()
        Tab_info_layout.addWidget(self.Tab_res)
        
        # 设置表格表头和筛选器，将模型定义部分抽出为独立函数
        self.Tab_res_header = ["Offset(P)", "File Path", "#Ptr", "#Hnd", "Access"]
        Tab_res_model = TableModel([["", "", "", "", ""]], self.Tab_res_header)
        self.Tab_res_ProxyModel = QSortFilterProxyModel()
        self.Tab_res_ProxyModel.setFilterKeyColumn(-1)
        self.Tab_res_ProxyModel.setSourceModel(Tab_res_model)
        self.Tab_res_ProxyModel.sort(0, Qt.AscendingOrder)
        self.Tab_res.setModel(self.Tab_res_ProxyModel)
        
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
        self.Tab_res.setColumnWidth(1, 800)

    def set_filter_data(self, text):
        regex = QRegularExpression(text)
        self.Tab_res_ProxyModel.setFilterRegularExpression(regex)
        self.Tab_res_ProxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def set_table_header(self):
        header = self.Tab_res.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
