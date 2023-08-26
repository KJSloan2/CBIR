import os
from os import listdir
from os.path import isfile, join
import json
######################################################################################
paths_ = {
	"00_resources":r"00_resources",
	"content":{"main":None,"manifest":None,"images":None,"images_grouped":None}
}
######################################################################################
folders_ = list(listdir(paths_["01_data"]))
if "content" not in folders_:
    path_content = r"%s%s%s" % (paths_["01_data"],"/","content")
    paths_["content"]["main"] = path_content
    os.mkdir(path_content)
    for sf in ["manifest","images","images_grouped"]:
        path_sf = r"%s%s%s%s%s%s" % (paths_["01_data"],"/","content","/",sf,"/")
        paths_["content"][sf] = path_sf
        os.mkdir(path_sf)
######################################################################################
with open(str("%s%s%s" % (paths_["00_resources"],"/","paths.json")), "w", encoding='utf-8') as json_paths:
	json_paths.write(json.dumps(paths_, indent=4, ensure_ascii=False))
print("DONE")
