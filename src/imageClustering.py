import json
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
######################################################################################
paths_ = json.load(open("%s%s" % ("00_resources/","paths.json")))
######################################################################################
with open(r"02_output/imageStats.json", 'r') as data_:
    data_string = data_.read()
imageStats_ = json.loads(data_string)
######################################################################################
shuttleFIles = False
######################################################################################
imPoints_ = []
imColors_ = []
imPaths_ = []
imIds_ = []
n = 10
for imKey,imStats in imageStats_.items():
    coords = imStats["plot"]
    color = imStats["color"]
    imPoints_.append([
        float(coords[0])*n,
        float(coords[1])*n,
        float(coords[2])*n
        ])
    imPaths_.append(imStats["path"])
    imIds_.append(imKey)
######################################################################################
imPoints_ = np.array(imPoints_)
n_clusters = 50
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(imPoints_)
labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
######################################################################################
'''If shuttoeFiles is set to True, the script will generate a new folder for each cluster
and will copy the image into its respective folder'''
if shuttleFIles == True:
    for label in list(dict.fromkeys(labels)):
        os.mkdir("%s%s" % (paths_["content"]["images_grouped"],label))
for i in range(len(labels)):
    pt = imPoints_[i]
    label = labels[i]
    path_source = imPaths_[i]
    imId = imIds_[i]
    imageStats_[imId]["group"] = str(label)
    if shuttleFIles == True:
        shutil.copy(path_source, "%s%s%s%s%s" % (paths_["content"]["images_grouped"],"\\",label,"\\",imId+".jpg"))
######################################################################################
for i in range(n_clusters):
    cluster_points = imPoints_[labels == i]
    ax.scatter(cluster_points[:, 0], cluster_points[:, 1], cluster_points[:, 2])
######################################################################################
with open(str(
	"%s%s" % (r"02_output/","imageStats.json")
	), "w", encoding='utf-8') as json_imageStats:
	json_imageStats.write(json.dumps(imageStats_, indent=4, ensure_ascii=False))
######################################################################################
#visualize the results with matplotlib
ax.scatter(cluster_centers[:, 0], cluster_centers[:, 1], cluster_centers[:, 2], c='black', marker='x', s=200, label='Cluster Centers')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Image Similarity - Clustered')
ax.legend()
plt.show()
print("DONE")
