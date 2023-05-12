from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QProcess
from time import sleep

class core(QProcess):

    def __init__(self) -> None:
        pass

    def w(self, imagefile, res):
        self.imagefile = imagefile
        self.res = res

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.res = stdout

    def test(self):
        self.process = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.start("vol.py", ["-f", self.imagefile, "imageinfo"])
        return self.res


if __name__ == "__main__":
    test = core()
    res = ""
    test.w("/home/randark/Snapshot6.vmem", res)
    res = test.test()
    sleep(10)
    print(res)