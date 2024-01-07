import os
from os import listdir
from os.path import isfile, join
import numpy as np
from PIL import Image, ImageOps

dirpath_images = r"PATH TO IMAGES"
if dirpath_images[-1:] != "/":
	dirpath_images = dirpath_images+"/"
######################################################################################
max_dimension = input("set the maximum pixel dimension for the output gif: ")
max_dimension = int(max_dimension)
print("Creating your gif...")
# create an empty list called images
images_ = []
images_names = []
timestr = time.strftime("%Y%m%d-%H%M%S")
files_ = [f for f in listdir(dirpath_images) if isfile(join(dirpath_images, f))]
for file in files_:
	split_fileName = file.split(".")
	fExtension = str(split_fileName[-1]).lower()
	if fExtension in ["jpg","jpeg"]:
		images_names.append(int(split_fileName[0].split("_")[1]))
		path_image = "%s%s" % (dirpath_images,file)
		im = Image.open(path_image) # open the image
		width, height = im.size
		if width > height:
			new_width = max_dimension
			new_height = int(height * (max_dimension / width))
		else:
			new_height = max_dimension
			new_width = int(width * (max_dimension / height))
		imageResized = im.resize((new_width, new_height), resample=0)
		imageResized = ImageOps.exif_transpose(imageResized)
		images_.append(imageResized)
######################################################################################
images_sorted = []
for idx in list(np.argsort(images_names)):
	images_sorted.append(images_[idx])
# calculate the frame number of the last frame (ie the number of images)
last_frame = (len(images_sorted)) 
######################################################################################
# create 10 extra copies of the last frame (to make the gif spend longer on the most recent data)
for x in range(0, 3):
	im = images_sorted[last_frame-1]
	images_sorted.append(im)
######################################################################################
split_path = []
for item in str(dirpath_images).split("/"):
	if item != "":
		split_path.append(item)
outputName = split_path[-1]
images_sorted[0].save("%s%s%s" % (r"02_output/",outputName,".gif")
		      ,save_all=True, append_images=images_sorted[1:], 
			  optimize=False, duration=100, loop=25)

print("DONE")
