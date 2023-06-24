import sys
from time import sleep
from PySide6.QtCore import Qt, QRunnable, QThreadPool
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class MyTask(QRunnable):

    def __init__(self, data: str) -> None:
        super().__init__()
        self.data = data

    def run(self, tmp=None):
        # 执行需要在后台线程中完成的任务
        print("Task started")
        print(tmp)
        sleep(3)  # 模拟耗时操作
        print(self.data)
        print("Task finished")


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Thread Example")
        self.layout = QVBoxLayout()
        self.button = QPushButton("Start Threads")
        self.button.clicked.connect(self.startThreads)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def startThreads(self):
        threadpool = QThreadPool()
        threadpool.setMaxThreadCount(3)  # 设置最大线程数为 3
        for i in range(3):
            task = MyTask(data=str(i))
            threadpool.start(task)
    def test(self):
        print("all done")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
