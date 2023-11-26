import os
from os import listdir
from os.path import isfile, join
import json
import cv2
import numpy as np
from datetime import datetime, timezone
######################################################################################
paths_ = json.load(open("%s%s" % ("00_resources/","paths.json")))
def calc_color_moments(image):
	b_channel, g_channel, r_channel = cv2.split(image)
	b_mean = np.mean(b_channel)
	g_mean = np.mean(g_channel)
	r_mean = np.mean(r_channel)
	b_std = np.std(b_channel)
	g_std = np.std(g_channel)
	r_std = np.std(r_channel)
	b_skew = np.mean(((b_channel - b_mean) / b_std) ** 3)
	g_skew = np.mean(((g_channel - g_mean) / g_std) ** 3)
	r_skew = np.mean(((r_channel - r_mean) / r_std) ** 3)
	b_kurt = (np.mean((b_channel - b_mean)**4)) / b_std**4
	g_kurt = (np.mean((g_channel - g_mean)**4)) / g_std**4
	r_kurt = (np.mean((r_channel - r_mean)**4)) / r_std**4
	return b_mean, g_mean, r_mean, b_std, g_std, r_std, b_skew, g_skew, r_skew, b_kurt, g_kurt, r_kurt;

def calc_midpoint(point1, point2, point3, point4):
	x_mid = (point1[0] + point2[0] + point3[0] + point4[0]) / 4
	y_mid = (point1[1] + point2[1] + point3[1] + point4[1]) / 4
	z_mid = (point1[2] + point2[2] + point3[2] + point4[2]) / 4
	return x_mid, y_mid, z_mid

def normailize_val(val,d_min,d_max):
	return round(((val-d_min)/(d_max-d_min)),4)

def rgb_to_hex(rgb):
    # Ensure values are in the valid range (0 to 255)
    r, g, b = [min(255, max(0, int(x))) for x in rgb]
    # Convert to hexadecimal format
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_color
######################################################################################
imageStatsRef_ = json.load(open("%s%s" % (r"02_output/","imageStats_ref.json")))
imageStatsRef_keys = list(imageStatsRef_.keys())
imageStats_ = {}
poolData_ = {"mean":[],"std":[],"skew":[],"kurt":[]}
path_images = r"src/viz/"
files_ = [f for f in listdir(path_images) if isfile(join(path_images, f))]
for f in files_:
	print(f)
	parse_f  = f.split(".")
	if parse_f[-1].lower() == "jpg":
		date_modified = None
		if parse_f[0] in imageStatsRef_keys:
			date_modified = imageStatsRef_[parse_f[0]]["date_modified"]
		impath =  "%s%s" % (path_images,f)
		image = cv2.imread(impath)
		try:
			b_mean, g_mean, r_mean, b_std, g_std, r_std, b_skew, g_skew, r_skew, b_kurt, g_kurt, r_kurt = calc_color_moments(image)
			moments_ = [[b_mean,g_mean,r_mean],[b_std, g_std, r_std],[b_skew, g_skew, r_skew],[b_kurt, g_kurt, r_kurt]]
			for mKey,vals_ in zip(list(poolData_.keys()),moments_):
				for v in vals_:
					poolData_[mKey].append(v)
			imageStats_[parse_f[0]] = {
				"b_channel":{
					"mean":b_mean,
					"std":b_std,
					"skew":b_skew,
					"kurt":b_kurt,
					"mean_norm":None,"std_norm":None,"skew_norm":None,"kurt_norm":None
				},
				"g_channel":{
					"mean":g_mean,
					"std":g_std,
					"skew":g_skew,
					"kurt":g_kurt,
					"mean_norm":None,"std_norm":None,"skew_norm":None,"kurt_norm":None
				},
				"r_channel":{
					"mean":r_mean,
					"std":r_std,
					"skew":r_skew,
					"kurt":r_kurt,
					"mean_norm":None,"std_norm":None,"skew_norm":None,"kurt_norm":None
				},
				"plot":{"coords":[],"color":[]},
				"path":None,
				"group":None,
				"source_date_modified":date_modified
			}
		except Exception as e:
			print(e)
			continue
######################################################################################
min_mean = min(poolData_["mean"])
max_mean = max(poolData_["mean"])
min_std = min(poolData_["std"])
max_std = max(poolData_["std"])
min_skew = min(poolData_["skew"])
max_skew = max(poolData_["skew"])
min_kurt = min(poolData_["kurt"])
max_kurt = max(poolData_["kurt"])
######################################################################################
for imKey,imObj in imageStats_.items():
	for channelKey in ["b_channel","g_channel","r_channel"]:
		channelStats = imObj[channelKey]
		norm_mean = normailize_val(channelStats["mean"],min_kurt,max_kurt)
		norm_std = normailize_val(channelStats["std"],min_std,max_std)
		norm_skew = normailize_val(channelStats["skew"],min_skew,max_skew)
		norm_kurt = normailize_val(channelStats["kurt"],min_kurt,max_kurt)
		imObj[channelKey]["mean_norm"] = normailize_val(channelStats["mean"],min_mean,max_mean)
		imObj[channelKey]["std_norm"] = normailize_val(channelStats["std"],min_std,max_std)
		imObj[channelKey]["skew_norm"] = normailize_val(channelStats["skew"],min_skew,max_skew)
		imObj[channelKey]["kurt_norm"] = normailize_val(channelStats["kurt"],min_kurt,max_kurt)
######################################################################################
for imKey,imObj in imageStats_.items():
	b_channel = imObj["b_channel"]
	g_channel = imObj["g_channel"]
	r_channel = imObj["r_channel"]
	pt1 = [r_channel["mean_norm"],b_channel["mean_norm"],g_channel["mean_norm"]]
	pt2 = [r_channel["std_norm"],b_channel["std_norm"],g_channel["std_norm"]]
	pt3 = [r_channel["kurt_norm"],b_channel["kurt_norm"],g_channel["kurt_norm"]]
	pt4 = [r_channel["skew_norm"],b_channel["skew_norm"],g_channel["skew_norm"]]
	imObj["plot"] = calc_midpoint(pt1,pt2,pt3,pt4)
	imObj["rgb"] = [r_channel["mean"],g_channel["mean"],b_channel["mean"]]
	imObj["hex"] = rgb_to_hex((r_channel["mean"],g_channel["mean"],b_channel["mean"]))

######################################################################################
with open(str(
	"%s%s" % (r"02_output/","imageStats.json")
	), "w", encoding='utf-8') as json_manifest:
	json_manifest.write(json.dumps(imageStats_, indent=4, ensure_ascii=False))
print("DONE")
