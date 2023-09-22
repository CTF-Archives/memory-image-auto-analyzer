import pandas as pd
import logging
from tabulate import tabulate
from layout.window_filedialog import Window_FileDialog, FileType
from backend.core import core_control, core_res


class report:
    def __init__(self) -> None:
        super().__init__()

    def set_ReportPath(self):
        Window_FileDialog.SaveReport()
        if "reportfile" in core_control.config.keys():
            self.reportpath = core_control.config["reportfile"]
            core_control.config.pop("reportfile")
            print(self.reportpath)
        else:
            logging.info("Select report path is canceled")
            return -1

    def generate_Txt(self, data_raw: tuple, mode: str) -> str:
        data = core_res.format_res(data_raw["data"], "imageinfo")
        time = data_raw["time"]
        config = data_raw["config"]
        data = pd.DataFrame(data)
        res = "{}\n".format(time)
        res += "mode: {}\n".format(mode)
        for key in list(config.keys()):
            res += "{key}: {value}\n".format(key=key, value=config[key])
        res += "\n"
        res += tabulate(data, headers="keys", tablefmt="fancy_grid")
        print("a:" + self.reportpath)
        with open(self.reportpath, "w+") as f:
            f.write(res)

    def generate_Excel(self):
        pass

    def generate_Markdown(self):
        pass

    def generate_Html(self):
        pass

    def get_data(self, module: str, index: int = None):
        pass

    def get_data_all(self, module: str, index: int = None):
        pass

    def run(self):
        if self.set_ReportPath() == -1:
            return None
        self.generate_Txt(core_res.res["imageinfo"][1], "imageinfo")


core_report = report()

if __name__ == "__main__":
    data = {
        "imageinfo": {
            1: {
                "data": "          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_24000, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_24000, Win7SP1x64_23418\n                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)\n                     AS Layer2 : FileAddressSpace (/home/randark/Snapshot6.vmem)\n                      PAE type : No PAE\n                           DTB : 0x187000L\n                          KDBG : 0xf80002c4a0a0L\n          Number of Processors : 1\n     Image Type (Service Pack) : 1\n                KPCR for CPU 0 : 0xfffff80002c4bd00L\n             KUSER_SHARED_DATA : 0xfffff78000000000L\n           Image date and time : 2020-12-27 06:20:05 UTC+0000\n     Image local date and time : 2020-12-26 22:20:05 -0800\n",
                "time": "2023-09-22T00:33:02.665950",
                "config": {
                    "imagefile": "/home/randark/Snapshot6.vmem",
                    "profile": "Win7SP1x64",
                },
            }
        }
    }
    a = core_report.generate_Txt(data["imageinfo"][1], "imageinfo")
    print(a)
