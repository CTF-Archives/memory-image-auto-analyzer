class result():

    def __init__(self) -> None:
        self.res_imageinfo = ""

    def add_res(self, data):
        self.res_imageinfo += data

    def get_res(self):
        return self.res_imageinfo


core_res = result()
