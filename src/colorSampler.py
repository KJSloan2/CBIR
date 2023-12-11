from datetime import datetime
from os import listdir
from os.path import isfile, join
import imageio.v2 as imageio
from imageio import imread
import numpy as np
import math
import json
import csv

#maxGSVal = round((((255*0.298)+(255*0.587)+(255*0.114))),2)
path_textures = r"src/textures/"
files = [f for f in listdir(path_textures) if isfile(join(path_textures, f))]
imPad = 2
sampleWindowSize = [3,3]
n = 0

sampledColors = {"rgb":[]}
for f in files:
	print(f)
	fileName = str(path_textures)+"%s" % (f)
	split_fileName = f.split(".")
	image_name = split_fileName[0]
	image_ext = split_fileName[-1].lower()
	if image_ext in ["jpg"]:
		src_image = imageio.imread("%s%s" % (path_textures,f))
		src_image_shape = src_image.shape
		(palX,palY) = (int(src_image_shape[0]*.5/sampleWindowSize[0]),int(src_image_shape[1]*.5/sampleWindowSize[1]))
		(poolX, poolY) = (sampleWindowSize[0],sampleWindowSize[1])
		nPixels = palX*palY

		iLen = palX+imPad
		jLen = palY+imPad

		for i in range(1,palX-1,1):
			x = int(i*poolX)
			for j in range(1,palY-1,1):
				y = int(j*poolY)
				pool = src_image[x:int(x+poolX), y:int(y+poolY), :]
				(pool_r,pool_g,pool_b) = ([],[],[])
				for subArray in pool:
					list(map(lambda rgb: pool_r.append(rgb[0]),subArray))
					list(map(lambda rgb: pool_g.append(rgb[1]),subArray))
					list(map(lambda rgb: pool_b.append(rgb[2]),subArray))
				if len(pool_r) >-0:
					mean_r = int(np.mean(pool_r))
					mean_g = int(np.mean(pool_g))
					mean_b = int(np.mean(pool_b))
					rgb = [mean_r,mean_g,mean_b]
					map(str,rgb)
					sampledColors["rgb"].append(rgb)
			
with open(str(
	"%s%s" % (r"02_output//","sampledColors.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(sampledColors, indent=2, ensure_ascii=False))

print("DONE")
