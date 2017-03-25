#!/usr/bin/python
import numpy as np
from math import floor
from utils import bresenhams_line
from matplotlib import pyplot as plt
from skimage.morphology import disk
import skimage.morphology as mp
from skimage import img_as_float, img_as_ubyte, filters
import scipy.signal as sig

def sinogram2picture(picture, sinogram, lines):
    
    picture_shape = np.shape(picture)
    width = picture_shape[0]
    height = picture_shape[1]
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    reconstructed = np.zeros(shape = picture_shape)
    helper = np.zeros(shape = picture_shape)
     
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
         
        #if (projection%10 == 0):
        #    fig, plots = plt.subplots(1, 2)
        #    plots[0].imshow(picture, cmap='gray')
        #    plots[1].imshow(normalizing_picture(reconstructed, helper), cmap='gray')
        #    plt.show()
     
    normalized = normalizing_picture(reconstructed, helper)

    return normalized

def filtered_sinogram2picture(picture, sinogram, lines):
    
    picture_shape = np.shape(picture)
    width = picture_shape[0]
    height = picture_shape[1]
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    reconstructed = np.zeros(shape = picture_shape)
    helper = np.zeros(shape = picture_shape)
    
    new_sinogram = filtering_sinogram(sinogram)
    
    # obserwacje
    fig, plots = plt.subplots(1, 2)
    plots[0].imshow(picture, cmap='gray')
    plots[1].imshow(new_sinogram, cmap='gray')
    plt.show()
    fig, plots = plt.subplots(1, 2)
    plots[0].plot(range(number_of_detectors), sinogram[0])
    plots[1].plot(range(number_of_detectors), new_sinogram[0])
    plt.show()
    
    new_sinogram = normalizing_sinogram(new_sinogram)
    
    # obserwacje
    fig, plots = plt.subplots(1, 2)
    plots[0].imshow(picture, cmap='gray')
    plots[1].imshow(new_sinogram, cmap='gray')
    plt.show()
    fig, plots = plt.subplots(1, 2)
    plots[0].plot(range(number_of_detectors), sinogram[0])
    plots[1].plot(range(number_of_detectors), new_sinogram[0])
    plt.show()
    
    for projection in range (0, number_of_projections, 1):
        for detector in range (0, number_of_detectors, 1):
            x0, y0, x1, y1 = lines[projection][detector]
            line = bresenhams_line(x0, y0, x1, y1)
            value = new_sinogram[projection][detector]
            for i in range (0, len(line), 1):
                    x, y = line[i]
                    if x >= 0 and y >= 0 and x < width and y < height:
                        reconstructed[x][y] += value
                        helper[x][y] += 1
        
        #if (projection%10 == 0):
        #    fig, plots = plt.subplots(1, 2)
        #    plots[0].imshow(picture, cmap='gray')
        #    plots[1].imshow(normalizing_picture(reconstructed, helper), cmap='gray')
        #    plt.show()
    
    reconstructed = normalizing_picture(reconstructed, helper)
    reconstructed = filtering_picture(reconstructed)
    return reconstructed

def filtering_sinogram(sinogram):
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    filtered = np.zeros((number_of_projections, number_of_detectors))
    
    # maska jednowymiarowa
    mask_size = floor(number_of_detectors/5)
    #mask_size = 5
    mask = np.zeros(mask_size)
    center = floor(mask_size/2)
    for i in range(0, mask_size, 1):
        k = i - center
        if k % 2 != 0:
            mask[i] = (-4/np.pi**2)/k**2
    mask[center] = 1
    
    # splot każdej projekcji z naszą maską
    for projection in range (0, number_of_projections, 1):
        filtered[projection] = sig.convolve(sinogram[projection], mask, mode = 'same')
    
    return filtered

def filtering_picture(img) :
    #new = filters.median(img, disk(5))
    perc = 10
    MIN = np.percentile(img, perc)
    MAX = np.percentile(img, 100-perc)
    normalizing(img, MIN, MAX)
    new = mp.erosion(img)
    return new

def normalizing_sinogram(sinogram):

    # pierwsza normalizacja do zakresu 0-1
    MIN = sinogram.min()
    MAX = sinogram.max()
    normalizing(norm, MIN, MAX)
    
    # druga normalizacja do "rozciągnięcia" histogramu
    perc = 10
    MIN = np.percentile(norm, perc)
    MAX = np.percentile(norm, 100-perc)
    normalizing(norm, MIN, MAX)
    
    # korekcja gamma
    gamma = 1/2.2
    norm = (norm ** gamma)
   
    return norm
    

def normalizing_picture(reconstructed, helper):
    normalized = np.copy(reconstructed)
    picture_shape = np.shape(normalized)
    width = picture_shape[0]
    height = picture_shape[1]
    for i in range (0, width, 1):
        for j in range (0, height, 1):
            if helper[i][j] != 0:
                normalized[i][j] = normalized[i][j]/helper[i][j]
    return normalized

def normalizing(img, minval, maxval):
    norm = (img - minval) / (maxval - minval)
    norm[norm[:,:] > 1] = 1
    norm[norm[:,:] < 0] = 0
    return norm