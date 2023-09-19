from datetime import datetime

a = {"imageinfo": {0: {"data": "test_imageinfo_1", "time": datetime.now().isoformat()}}, "pslist": {0: {"data": "test_pslist_1", "time": datetime.now().isoformat()}}}

data = "test_imageinfo_2"

a["imageinfo"][list(a["imageinfo"].keys())[-1] + 1] = {"data": data, "time": datetime.now().isoformat()}

print(a["imageinfo"])
print(list(a["imageinfo"].keys()))
