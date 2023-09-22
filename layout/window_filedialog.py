import logging
from PySide6.QtWidgets import *
from backend.core import core_control, core_MainWIndow


FileType = {
    "Txt": ".txt",
    "Excel": ".xlsx",
    "Markdown": ".md",
    "Html": ".html",
    "CSV": ".csv",
}


class Window_FileDialog:
    def __init__(self) -> None:
        super().__init__()

    def OpenFile():
        filename = QFileDialog.getOpenFileName(parent=core_MainWIndow, caption="选择镜像文件", dir=".", filter="*")[0]
        if filename:
            core_control.config["imagefile"] = filename
            logging.info("select image file:" + filename)

    def SaveReport():
        file_filter = ";;".join([FileType[i] for i in FileType.keys()])
        print(file_filter)
        filename, suffix = QFileDialog.getSaveFileName(parent=core_MainWIndow, caption="选择报告文件位置", dir=".", filter=file_filter)
        if filename:
            core_control.config["reportfile"] = filename + suffix
            logging.info("select report path:" + filename + suffix)
