from datetime import datetime
import logging
from PySide6.QtWidgets import *


class control:
    def __init__(self) -> None:
        self.VolProcess = None
        self.BasicInfo_status = 0
        self.BasicInfo_modules = ["pslist", "filescan", "cmdline", "iehistory"]
        self.config = {"imagefile": "", "profile": ""}

    def check_imagefile(self, window: QMainWindow):
        if self.config["imagefile"] == "":
            logging.warning("未指定文件")
            dlg = QMessageBox(window)
            dlg.setWindowTitle("Warning!")
            dlg.setText("未选择有效的内存镜像文件!")
            dlg.exec()
            return False
        return True

    def check_profile(self, window: QMainWindow):
        if self.config["profile"] == "":
            logging.warning("未指定 profile")
            dlg = QMessageBox(window)
            dlg.setWindowTitle("Warning!")
            dlg.setText("未选择有效的 profile 参数!")
            dlg.exec()
            return False
        return True


class result:
    def __init__(self) -> None:
        self.res = {}

    def clear_res(self, module: str) -> None:
        """
        对指定模块的储存进行清空
        """
        if module in self.res.keys():
            self.res.pop(module)
        else:
            return "Module is empty"

    def add_res(self, module: str, data: str) -> None:
        """
        将结果储存到指定模块
        """
        # 储存扫描结果，module以vol模块格式
        if module not in self.res.keys():
            self.res[module] = data
        else:
            self.res[module] += data

    def get_res(self, module: str) -> str:
        """
        读取特定模块的结果
        """
        # 调用扫描结果，module以vol模块格式
        if module in self.res.keys():
            return self.res[module]
        else:
            return "Module is empty"

    def format_res(self, data: str, module: str) -> str:
        """
        针对特定模块的数据进行格式化处理
        """
        data = [i for i in data.split("\n") if i != ""]
        match module:
            case "imageinfo":
                res = [i.strip().split(":", maxsplit=1) for i in data]
            case "pslist":
                res = data[2:]
                res = [i.split(" ") for i in res]
                for offset, sub in enumerate(res):
                    tmp = [i for i in sub if i != ""]
                    res[offset] = tmp[0:8] + [" ".join(tmp[8:])]
            case "cmdline":
                res_tmp = [i for i in data if i != "*" * 72]
                res_tmp = res_tmp[1:]
                res = []
                for i in range(0, len(res_tmp), 2):
                    tmp = [i for i in res_tmp[i].strip().split(" ") if i != ""]
                    name = tmp[0]
                    pid = tmp[2]
                    command = res_tmp[i + 1].strip().split(":", 1)[1].strip()
                    res.append([name, pid, command])
            case "iehistory":
                res_tmp = [i for i in data if i != "*" * 50]
                res = []
                for i in range(0, len(res_tmp), 7):
                    pid, name = [i for i in res_tmp[i].strip().split(" ") if i != ""][1:3]
                    user, filepath = res_tmp[i + 3].strip().split(" ")[2].split(r"@")
                    modified_time = res_tmp[i + 4].strip().split(":", 1)[1].strip()
                    accessed_time = res_tmp[i + 5].strip().split(":", 1)[1].strip()
                    File_Offset, Data_Offset, Data_Length = [i.strip().split(":")[1].strip() for i in res_tmp[i + 6].strip().split(",")]
                    res.append([name, pid, user, filepath, modified_time, accessed_time, File_Offset, Data_Offset, Data_Length])
            case "filescan":
                res = [i.strip().split(" ") for i in data[2:]]
                for offset, sub in enumerate(res):
                    res[offset] = [i for i in sub if i != ""]
                    res[offset] = [res[offset][0], res[offset][4]] + res[offset][1:4]
            case _:
                res = [data]
        return res


core_res = result()
core_control = control()
