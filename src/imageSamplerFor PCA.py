from os import listdir
from os.path import isfile, join
import imageio.v2 as imageio
from imageio import imread
import numpy as np
import math
import json
 
import time

#maxGSVal = round((((255*0.298)+(255*0.587)+(255*0.114))),2)
path_textures = r"02_output/images_resized/"
files = [f for f in listdir(path_textures) if isfile(join(path_textures, f))]
imPad = 2
sampleWindowSize = [3,3]
n = 0

samples = {"gs":{}}
#for f in files:
for n in range(0,5,1):
	f = files[n]
	fileName = str(path_textures)+"%s" % (f)
	split_fileName = f.split(".")
	image_name = split_fileName[0]
	image_ext = split_fileName[-1].lower()
	if image_ext in ["jpg"]:
		src_image = imageio.imread("%s%s" % (path_textures,f))
		src_image_shape = src_image.shape
		store_gs = []
		#gsArray = np.zeros((src_image_shape[0],src_image_shape[1]),dtype=int)
		for i in range(1,src_image_shape[0]-1,1):
			for j in range(1,src_image_shape[1]-1,1):
				pxl = src_image[i, j, :]
				gs = round((((pxl[0]*0.299)+(pxl[1]*0.587)+(pxl[2]*0.114))),2)
				store_gs.append(gs)
		samples["gs"][image_name] = store_gs
			
with open(str(
	"%s%s" % (r"02_output/images_resized/image_data/","samples.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(samples, ensure_ascii=False))

print("DONE")
