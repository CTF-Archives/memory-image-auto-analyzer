from PySide6.QtCore import QProcess
import logging
from backend.res import core_res


class vol_backend_v2(QProcess):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.process = None

    def func(self, imagefile: str, module: str, func_finished, profile=None):
        """
        调用Volatility2进行镜像分析
        """
        self.process = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.stateChanged.connect(self.handle_state)
        # self.process.finished.connect(self.process_finished)  # Clean up once complete.
        self.process.finished.connect(func_finished)
        self.process.start("vol.py", ["-f", imagefile, module])

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode()
        logging.error(stderr)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode()
        logging.info(stdout)
        core_res.add_res("imageinfo", stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        logging.debug(f"State changed: {state_name}")
