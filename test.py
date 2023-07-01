import sys
from PySide6.QtWidgets import QApplication, QTreeView, QFileSystemModel, QVBoxLayout,QWidget
from PySide6.QtCore import QDir

# 创建应用程序对象
app = QApplication(sys.argv)

# 创建树状视图和布局
tree_view = QTreeView()
layout = QVBoxLayout()
layout.addWidget(tree_view)

# 创建文件系统模型
model = QFileSystemModel()
model.setRootPath(QDir.currentPath())

# 设置模型为树状结构
tree_view.setModel(model)
tree_view.setRootIndex(model.index(QDir.currentPath()))

# 显示树状视图窗口
window = QWidget()
window.setLayout(layout)
window.setWindowTitle("Tree View Demo")
window.show()

# 启动应用程序主循环
sys.exit(app.exec())
