import json
import os
import numpy as np
from sklearn.cluster import KMeans
import math
import csv
import warnings
warnings.filterwarnings("ignore")

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

def rgb_to_hex(r, g, b):
	hex_code = "#{:02x}{:02x}{:02x}".format(r, g, b)
	return hex_code

with open(r"02_output/sampledColors.json", 'r') as data_:
	data_string = data_.read()
sampledColors_json = json.loads(data_string)
n = 1

pantoneColors = {}
with open(r"00_resources/pantone.csv", mode='r',newline='') as data_csv:
	csv_reader = csv.reader(data_csv)
	next(csv_reader)
	for row in csv_reader:
		hexcode = row[4]
		pantoneColors[hexcode] = {
			"name":row[5],
			"r":int(row[1]),
			"g":int(row[2]),
			"b":int(row[3])
		}

colorSpace = []
for rgb in sampledColors_json["rgb"]:
	#rgb = rgb.split(",")
	colorSpace.append([int(rgb[0]),int(rgb[2]),int(rgb[1])])
	
colorSpace = np.array(colorSpace)
n_clusters = 250
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(colorSpace)
labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

cluster_labels = kmeans.predict(kmeans.cluster_centers_)
output = {"colors":[]}
for label,clusterCenter in zip(cluster_labels,cluster_centers):
	print(label)
	cluster_rgb = [int(clusterCenter[0]),int(clusterCenter[2]),int(clusterCenter[1])]
	colorObj = {
		"cluster_id": str(label),
		"cluster_size":0,
		"cluster_size_rank":None,
		"rgb":[cluster_rgb[0],cluster_rgb[1],cluster_rgb[2]],
		"hex":rgb_to_hex(cluster_rgb[0],cluster_rgb[1],cluster_rgb[2]),
		"hue":computeHue(cluster_rgb[0],cluster_rgb[1],cluster_rgb[2]),
		"gs":round((cluster_rgb[0]*0.298+cluster_rgb[1]*0.587+cluster_rgb[2]*0.114),2),
		"pantone_hex":None,
		"pantone_name":None,
		"cluster":[]
		}
	
	for key,pantoneColor in pantoneColors.items():
		dist_to_pantone = math.sqrt(
			(int(pantoneColor["r"])-int(clusterCenter[0]))**2 + 
			(int(pantoneColor["b"])-int(clusterCenter[2]))**2 + 
			(int(pantoneColor["g"])-int(clusterCenter[1]))**2
			)
		if dist_to_pantone <= 15:
			colorObj["pantone_hex"] = key
			colorObj["pantone_name"] = pantoneColor["name"]
			break

	idx_points = [i for i, val in enumerate(labels) if val == label]
	for idx in idx_points:
		pt = colorSpace[idx]
		r = int(pt[0])
		g = int(pt[2])
		b = int(pt[1])
		dist_to_center = math.sqrt((int(clusterCenter[0])-r)**2 + (int(clusterCenter[1])-b)**2 + (int(clusterCenter[2])-g)**2)
		if dist_to_center <= 20:
			pantone_hex = None
			pantone_name = None
			for key,pantoneColor in pantoneColors.items():
				dist_to_pantone = math.sqrt(
					(int(pantoneColor["r"])-r)**2 + 
					(int(pantoneColor["b"])-b)**2 + 
					(int(pantoneColor["g"])-g)**2
					)
				if dist_to_pantone <= 10:
					pantone_hex = key
					pantone_name = pantoneColor["name"]
					break

			gs = round((r*0.298+g*0.587+b*0.114),2)
			hex = rgb_to_hex(r,g,b)
			colorObj["cluster_size"]+=1
			'''colorObj["cluster"].append(
				{
					"hex":hex,
					"rgb":[r,g,b],
					"gs":float(gs),
					"pantone_hex":pantone_hex,
					"pantone_name":pantone_name,
					"prct": 0,
				}
			)'''
	output["colors"].append(colorObj)

with open(str(
	"%s%s" % (r"02_output//","pallet.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(output, indent=2, ensure_ascii=False))

print("DONE")
