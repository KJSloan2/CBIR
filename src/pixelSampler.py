from datetime import datetime
from os import listdir
from os.path import isfile, join
import imageio.v2 as imageio
from imageio import imread
import numpy as np
import math
import json
import csv

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def computeHue(r,g,b):
	r_depth = r/255
	g_depth = g/255
	b_depth = b/255
	cMax = max(r_depth,g_depth,b_depth)
	cMin = min(r_depth,g_depth,b_depth)
	delta = (cMax - cMin)+1
	if cMax == r_depth:
		hue = (g_depth - b_depth) / (delta);
	elif cMax == g_depth:
		hue = 2 +(b_depth - r_depth) / (delta);
	elif cMax == b_depth:
		hue = 4 + (r_depth - g_depth) / (delta); 
	if hue > 0:
		hue = (round(hue*60,2))
	else:
		hue = (round(math.floor(360 + hue),2))
	return(hue)

step_size = 25
bounds = (0, 255-step_size
# Create a meshgrid
x = np.arange(bounds[0], bounds[1] + step_size, step_size)
y = np.arange(bounds[0], bounds[1] + step_size, step_size)
z = np.arange(bounds[0], bounds[1] + step_size, step_size)

# Create a 3D grid using meshgrid
xx, yy, zz = np.meshgrid(x, y, z)

# Stack the points into a 3D array
ref = np.column_stack((xx.ravel(), yy.ravel(), zz.ravel()))
tableSize = ref.shape[0]
######################################################################################
def format_number(number):
    number_str = str(number)
    num_zeros = 3 - len(number_str)
    num_zeros = max(0, min(num_zeros, 2))
    formatted_number = '0' * num_zeros + number_str
    return formatted_number
######################################################################################
samples = {}
for i in range(len(ref)):
	key = "".join(map(str,list(map(format_number,ref[i]))))
	samples[key] = {
		"rgb":[int(ref[i][0]),int(ref[i][2]),int(ref[i][1])],
		"count":0, "images":{}}

refPointMaxDist =  math.sqrt((0 - 25)**2 + (0 - 25)**2 + (0 - 25)**2)
print(refPointMaxDist)
######################################################################################
path_textures = r"01_data/content/images/"
files = [f for f in listdir(path_textures) if isfile(join(path_textures, f))]
imPad = 2
sampleWindowSize = [3,3]
n = 0

ref_rgb = []

def round_to_5(value):
	return round(value / 5) * 5

pool_gs = []
pool_rbg = []
pool_hue = []
rgb_normalized = []
ref_rgbKeys = []
for f in files:
	print(f)
	fileName = str(path_textures)+"%s" % (f)
	split_fileName = f.split(".")
	image_name = split_fileName[0]
	image_ext = split_fileName[-1].lower()
	if image_ext in ["jpg", "jpeg"]:
		src_image = imageio.imread("%s%s" % (path_textures,f))
		src_image_shape = src_image.shape
		  
		(palX,palY) = (
			   int(src_image_shape[0]*.5/sampleWindowSize[0]),
				int(src_image_shape[1]*.5/sampleWindowSize[1])
				)
		  
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
					dn = [mean_r, mean_b, mean_g]

					store_dist = []
					for refKey,refItem in samples.items():
						dist = math.sqrt(
							(float(refItem["rgb"][0])-float(dn[0]))**2 + 
							(float(refItem["rgb"][1])-float(dn[1]))**2 + 
							(float(refItem["rgb"][2])-float(dn[2]))**2)
						if dist < refPointMaxDist:
							refItem["count"] += 1
							if image_name not in list(refItem["images"].keys()):
								refItem["images"][image_name] = {
									"pts":[[int(x),int(y)]]
								}
							else:
								refItem["images"][image_name]["pts"].append([int(x),int(y)])
							break

with open(str(
	"%s%s" % (r"02_output//","samples.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(samples, indent=1, ensure_ascii=False))

print("DONE")
