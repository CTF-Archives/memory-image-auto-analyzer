class status:
    def __init__(self) -> None:
        self.VolProcess = None
        self.BasicInfo_status = 0
        self.BasicInfo_modules = ["pslist", "filescan", "cmdline", "iehistory"]


core_status = status()
