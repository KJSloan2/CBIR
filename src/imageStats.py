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
	# Convert image to the Lab color space
	#lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
	#b_channel,l_channel, a_channel = cv2.split(lab_image)
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

def calc_midpoint(point1, point2, point3):
	x_mid = (point1[0] + point2[0] + point3[0]) / 3
	y_mid = (point1[1] + point2[1] + point3[1]) / 3
	z_mid = (point1[2] + point2[2] + point3[2]) / 3
	return x_mid, y_mid, z_mid

def normailize_val(val,d_min,d_max):
	return round(((val-d_min)/(d_max-d_min)),4)
######################################################################################
imageStatsRef_ = json.load(open("%s%s" % (r"02_output/","imageStats_ref.json")))
imageStatsRef_keys = list(imageStatsRef_.keys())
imageStats_ = {}
poolData_ = {"mean":[],"std":[],"skew":[]}
files_ = [f for f in listdir(paths_["content"]["images"]) if isfile(join(paths_["content"]["images"], f))]
for f in files_:
	parse_f  = f.split(".")
	print(parse_f[0])
	if parse_f[-1].lower() == "jpg" and parse_f[0] in imageStatsRef_keys:
		date_modified = imageStatsRef_[parse_f[0]]["date_modified"]
		impath =  "%s%s" % (paths_["content"]["images"],f)
		image = cv2.imread(impath)
		try:
			b_mean, g_mean, r_mean, b_std, g_std, r_std, b_skew, g_skew, r_skew, b_kurt, g_kurt, r_kurt = calc_color_moments(image)
			'''print(f"L-channel: Mean={l_mean:.2f}, Std={l_std:.2f}, Skewness={l_skewness:.2f}")
			print(f"A-channel: Mean={a_mean:.2f}, Std={a_std:.2f}, Skewness={a_skewness:.2f}")
			print(f"B-channel: Mean={b_mean:.2f}, Std={b_std:.2f}, Skewness={b_skewness:.2f}")'''
			moments_ = [[b_mean,g_mean,r_mean],[b_std, g_std, r_std],[b_skew, g_skew, r_skew]]
			for mKey,vals_ in zip(list(poolData_.keys()),moments_):
				for v in vals_:
					poolData_[mKey].append(v)
			imageStats_[parse_f[0]] = {
				"b_channel":{
					"mean":b_mean,
					"std":b_std,
					"skew":b_skew,
					"kurt":b_kurt,
					"mean_norm":None,
					"std_norm":None,
					"skew_norm":None,
					"kurt_norm":None
				},
				"g_channel":{
					"mean":g_mean,
					"std":g_std,
					"skew":g_skew,
					"kurt":g_kurt,
					"mean_norm":None,
					"std_norm":None,
					"skew_norm":None,
					"kurt_norm":None
				},
				"r_channel":{
					"mean":r_mean,
					"std":r_std,
					"skew":r_skew,
					"kurt":r_kurt,
					"mean_norm":None,
					"std_norm":None,
					"skew_norm":None,
					"kurt_norm":None
				},
				"plot":{"coords":[],"color":[]},
				"path":impath,
				"group":None,
				"source_date_modified":date_modified
			}
		except Exception as e:
			print(e)
			pass
######################################################################################
min_mean = min(poolData_["mean"])
max_mean = max(poolData_["mean"])
min_std = min(poolData_["std"])
max_std = max(poolData_["std"])
min_skew = min(poolData_["skew"])
max_skew = max(poolData_["skew"])
######################################################################################
for isKey,isItem in imageStats_.items():
	for channelKey in ["b_channel","g_channel","r_channel"]:
		channelStats = isItem[channelKey]
		norm_std = normailize_val(channelStats["std"],min_std,max_std)
		norm_skew = normailize_val(channelStats["skew"],min_skew,max_skew)
		isItem[channelKey]["mean_norm"] = normailize_val(channelStats["mean"],min_mean,max_mean)
		isItem[channelKey]["std_norm"] = normailize_val(channelStats["std"],min_std,max_std)
		isItem[channelKey]["skew_norm"] = normailize_val(channelStats["skew"],min_skew,max_skew)
######################################################################################
for isKey,isItem in imageStats_.items():
	b_channel = isItem["b_channel"]
	g_channel = isItem["g_channel"]
	r_channel = isItem["r_channel"]
	pt1 = [b_channel["mean_norm"],b_channel["std_norm"],b_channel["skew_norm"]]
	pt2 = [g_channel["mean_norm"],g_channel["std_norm"],g_channel["skew_norm"]]
	pt3 = [r_channel["mean_norm"],r_channel["std_norm"],r_channel["skew_norm"]]
	isItem["plot"] = calc_midpoint(pt1,pt2,pt3)
	isItem["color"] = [r_channel["mean"],g_channel["mean"],b_channel["mean"]]
######################################################################################
with open(str(
	"%s%s" % (r"02_output/","imageStats.json")
	), "w", encoding='utf-8') as json_manifest:
	json_manifest.write(json.dumps(imageStats_, indent=4, ensure_ascii=False))
