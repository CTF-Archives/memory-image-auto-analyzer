class result():

    def __init__(self) -> None:
        self.res_imageinfo = {}

    def clear_res(self, module: str):
        if module in self.res_imageinfo.keys():
            self.res_imageinfo.pop(module)
        else:
            return "Module is empty"

    def add_res(self, module: str, data: str):
        # 储存扫描结果，module以vol模块格式
        if module not in self.res_imageinfo.keys():
            self.res_imageinfo[module] = data
        else:
            self.res_imageinfo[module] += data

    def get_res(self, module: str):
        # 调用扫描结果，module以vol模块格式
        if module in self.res_imageinfo.keys():
            return self.res_imageinfo[module]
        else:
            return "Module is empty"

    def sort_res(self, data: str, module: str):
        data = data.split("\n")
        data = [i for i in data if i != ""]
        if module == "imageinfo":
            res = [i.strip().split(":", maxsplit=1) for i in data]
        elif module == "pslist":
            res = data[2:]
            res = [i.split(" ") for i in res]
            for offset, sub in enumerate(res):
                tmp = [i for i in sub if i != ""]
                res[offset] = tmp[0:8]+[" ".join(tmp[8:])]
        else:
            res = [data]
        return res


core_res = result()
