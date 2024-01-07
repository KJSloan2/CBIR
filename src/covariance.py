import json
import math

import numpy as np
import matplotlib.pyplot as plt

imageSamples = json.load(open("%s%s" % (r"02_output/images_resized/image_data/","samples.json")))

imKeys = list(imageSamples["gs"].keys())

gsMatrix_average = []
gsMatrix = []

for i in range(len(imKeys)):
    gsVals = imageSamples["gs"][imKeys[i]]
    gsMean = sum(gsVals)/len(gsVals)
    gsMatrix_average.append([gsMean])
    gsMatrix.append(gsVals)

gsMatrix_average = np.array(gsMatrix_average)
gsMatrix = np.array(gsMatrix)
#gaMatricAverage = np.mean(gsMatrix, axis=1, keepdims=True)
bMatrix = np.zeros((len(imKeys),300**2),dtype=float)

for i in range(len(gsMatrix_average)):
    gsRowMean = gsMatrix_average[i][0]
    for j in range(len(gsMatrix[i])):
        bMatrix[i][j] = gsMatrix[i][j] - gsRowMean

def calc_covMatrix(data_matrix):
    num_rows, num_cols = data_matrix.shape
    means = np.mean(data_matrix, axis=1, keepdims=True)
    centered_data = data_matrix - means
    covariance_matrix = (centered_data @ centered_data.T) / (num_cols - 1)
    return covariance_matrix


def viz_covMatrix(covariance_matrix):
    plt.imshow(covariance_matrix, cmap='viridis', interpolation='nearest')
    plt.title('Covariance Matrix')
    plt.colorbar(label='Covariance')
    plt.show()

covMatrix = calc_covMatrix(gsMatrix)
eigenvalues, eigenvectors = np.linalg.eig(covMatrix)

# Print the eigenvalues and eigenvectors
print("Eigenvalues:")
print(eigenvalues)
print("\nEigenvectors:")
print(eigenvectors)

viz_covMatrix(covMatrix)
