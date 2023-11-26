import csv
import json
######################################################################################
paths_ = json.load(open("%s%s" % ("00_resources/","paths.json")))
######################################################################################
with open(r"02_output/imageStats.json", 'r') as data_:
	data_string = data_.read()
imageStats_ = json.loads(data_string)
######################################################################################
with open("%s%s" % (r"src/viz/","imageStats.csv"), 'w',newline='', encoding='utf-8') as write_dataOut:
	writer_dataOut = csv.writer(write_dataOut)
	writer_dataOut.writerow([
		"id","x","y","z","r","g","b","hex","datemod",
		"location_tag","year","month"
		])
	###################################################################################### 
	#Washington_00062_2016_06_18"  
	for imKey,imObj in imageStats_.items():
		parse_imKey = imKey.split("_")
		imLocationTag = parse_imKey[0]
		imYear = parse_imKey[2]
		imMonth = parse_imKey[3]
		coords_ = imObj["plot"]
		rgb_ = imObj["rgb"]
		chex = imObj["hex"]
		dateMod = imObj["source_date_modified"]

		writer_dataOut.writerow([
			imKey,
			coords_[0],coords_[1],coords_[2],
			rgb_[0],rgb_[1],rgb_[2],
			chex,dateMod,imLocationTag,
			imYear,imMonth
		])
print("DONE")
