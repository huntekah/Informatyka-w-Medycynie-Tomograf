#!/usr/bin/python
import numpy as np
from utils import bresenhams_line
from matplotlib import pyplot as plt
import skimage.morphology as mp
from skimage import img_as_float, img_as_ubyte

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
    
    print("Chce pofiltrować")
    filtered_sinogram = filtering_sinogram(sinogram)
    fig, plots = plt.subplots(1, 2)
    plots[0].imshow(picture, cmap='gray')
    plots[1].imshow(filtered_sinogram, cmap='gray')
    plt.show()
    print("Powinnam już skończyć filtrować")
    
    # k-ta projekcja
    for projection in range (0, number_of_projections, 1):
        for detector in range (0, number_of_detectors, 1):
            x0, y0, x1, y1 = lines[projection][detector]
            line = bresenhams_line(x0, y0, x1, y1)
            value = filtered_sinogram[projection][detector]
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
    
    normalized = normalizing(reconstructed, helper)
    #filtered = filtering_picture(normalized)
    return normalized

def filtering_sinogram(sinogram):
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    filtered = np.zeros((number_of_projections, number_of_detectors))
    
    mask = np.zeros((number_of_projections, number_of_detectors))
    
    for projection in range (0, number_of_projections, 1):
        for detector in range (0, number_of_detectors, 1):
            if (detector == 0):
                mask[projection][detector] = 1
            if (detector % 2 == 0):
                mask[projection][detector] = 0
            else:
                mask[projection][detector] = (-4/(np.pi*np.pi))/(detector*detector)
     
    for projection in range (0, number_of_projections, 1):
        for detector in range (0, number_of_detectors, 1):
            if(detector != 0 and detector != number_of_detectors-1):
                for m in range (-1, 2, 1):
                    if(m == -1 or m == 1):
                        filtered[projection][detector] += sinogram[projection][detector+m]*(-4/(np.pi*np.pi))
                    if(m == 0):
                        filtered[projection][detector] += sinogram[projection][detector+m]
            else:
                filtered[projection][detector] += sinogram[projection][detector]
            #print ("f[", projection, "][", detector, "]: " , filtered[projection][detector])
    print("SINGORAM:")
    #print(sinogram[0:5][0:5])
    print("FILTERED SINOGRAM:")
    #print(filtered[0:5][0:5])
    return filtered

def filtering_picture(img) :
    img = img_as_ubyte(img)
    mean = np.mean(img)
    binary = (img > mean*1.05) * 255
    binary = np.uint8(binary)
    return binary
                

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