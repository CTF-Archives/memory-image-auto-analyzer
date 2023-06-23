import sys
import os
sys.path.append(os.environ.get('PS_SITEPACKAGES'))
from PySide6 import QtGui, QtWidgets, QtCore

from functools import partial


class FilterProxy(QtCore.QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super(FilterProxy, self).__init__(*args, **kwargs)
        self.filters_colums = set()
        self.mText = ""

    def setText(self, text):
        self.mText = text
        self.invalidateFilter()

    def appendColumn(self, name):
        self.filters_colums.add(name.lower())
        self.invalidateFilter()

    def removeColumn(self, name):
        self.filters_colums.discard(name.lower())
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if self.mText:
            for i in range(self.sourceModel().columnCount()):
                header = self.sourceModel().headerData(i, QtCore.Qt.Horizontal) 
                text = self.sourceModel().index(source_row, i).data()
                if header in self.filters_colums and self.mText in text.lower():
                    return True
            return False
        return True


class QDictTableView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(QDictTableView, self).__init__(*args, **kwargs)
        self.resize(400,300)

        # controls
        self.ui_search_input = QtWidgets.QLineEdit()
        self.ui_search_input.setPlaceholderText('Search...')

        self.ui_item_table = QtWidgets.QTableView()
        self.ui_item_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui_item_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui_item_table.verticalHeader().hide()

        lay_filters = QtWidgets.QHBoxLayout()
        lay_main = QtWidgets.QVBoxLayout(self)
        lay_main.setAlignment(QtCore.Qt.AlignTop)
        lay_main.addWidget(self.ui_search_input)
        lay_main.addLayout(lay_filters)
        lay_main.addWidget(self.ui_item_table)

        model = self.populate_table()
        self.proxy = FilterProxy()
        self.proxy.setSourceModel(model)
        self.ui_item_table.setModel(self.proxy)

        for text in ("Name", "Age", "Career"):
            checkbox = QtWidgets.QCheckBox(text)            
            checkbox.stateChanged.connect(partial(self.update_columns, text))
            checkbox.setChecked(True)
            lay_filters.addWidget(checkbox)

        self.ui_search_input.textChanged.connect(self.proxy.setText)

    def update_columns(self, text, state):
        cols = self.ui_item_table.model().columnCount()
        i = [self.ui_item_table.model().headerData(i, QtCore.Qt.Horizontal) for i in range(cols)].index(text.lower())
        self.ui_item_table.setColumnHidden(i, state == QtCore.Qt.Unchecked)
        if state == QtCore.Qt.Unchecked:
            self.proxy.removeColumn(text)
        else:
            self.proxy.appendColumn(text)

    def populate_table(self):
        peoples = [
            {'name': 'Kevin', 'age': 5, 'career': 'athlete'},
            {'name': 'Maggie', 'age': 13, 'career': 'banker'},
            {'name': 'Leslie', 'age': 32, 'career': 'banker'},
            {'name': 'Emily', 'age': 45, 'career': 'athlete'},
            {'name': 'David', 'age': 27, 'career': 'banker'},
            {'name': 'Marie', 'age': 63, 'career': 'secretary'}
        ]

        model = QtGui.QStandardItemModel()

        headers = ["name", "age", "career"]
        model.setHorizontalHeaderLabels(headers)

        for row, people in enumerate(peoples):
            items = []
            for key, value in people.items():
                col = headers.index(key)
                item = QtGui.QStandardItem(str(value))
                items.append(item)
            model.insertRow(row, items)
        return model

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = QDictTableView()
    ex.show()
    sys.exit(app.exec_())