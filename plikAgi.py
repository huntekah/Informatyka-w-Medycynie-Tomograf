#!/usr/bin/python
import numpy as np
from utils import bresenhams_line
from matplotlib import pyplot as plt
import skimage.morphology as mp

def sinogram2picture(picture, sinogram, lines):
    #TODO transformations
    picture_shape = np.shape(picture)
    width = picture_shape[0]
    height = picture_shape[1]
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    reconstructed = np.zeros(shape = picture_shape)
    helper = np.zeros(shape = picture_shape)
    
    # k-ta projekcja
    for projection in range (0, number_of_projections, 1):
        for detector in range (0, number_of_detectors, 1):
            x0, y0, x1, y1 = lines[projection][detector]
            line = bresenhams_line(x0, y0, x1, y1)
            value = sinogram[projection][detector]
            for i in range (0, len(line), 1):
                    x, y = line[i]
                    if x >= 0 and y >= 0 and x < width and y < height:
                        reconstructed[x][y] += value
                        helper[x][y] += 1
                        
#        reconstructed = filtering(reconstructed)
        
        if (projection%10 == 0):
            fig, plots = plt.subplots(1, 2)
            plots[0].imshow(picture, cmap='gray')
            plots[1].imshow(normalizing(reconstructed, helper), cmap='gray')
            plt.show()
        

    print("lol")
    
    
    return normalizing(reconstructed, helper)

#def filtering(picture):
#    return mp.erosion(picture)

def normalizing(reconstructed, helper):
    normalized = np.copy(reconstructed)
    picture_shape = np.shape(normalized)
    width = picture_shape[0]
    height = picture_shape[1]
    for i in range (0, width, 1):
        for j in range (0, height, 1):
            if helper[i][j] != 0:
                normalized[i][j] = normalized[i][j]/helper[i][j]
    return normalized