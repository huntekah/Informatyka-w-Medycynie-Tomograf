#!/usr/bin/python
import numpy as np
from math import floor, ceil
from utils import bresenhams_line
from matplotlib import pyplot as plt
from skimage.morphology import disk
import skimage.morphology as mp
from skimage import img_as_float, img_as_ubyte, filters
import scipy.signal as sig
import imageio
from sklearn.metrics import mean_squared_error


def sinogram2picture(picture, sinogram, lines):
    
    picture_shape = np.shape(picture)
    width = picture_shape[0]
    height = picture_shape[1]
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    images = []
    iterator = 0
    mse = np.zeros(ceil(number_of_projections/10)+1)
    
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
                        reconstructed[int(x)][int(y)] += value
                        helper[int(x)][int(y)] += 1
         
        if (projection%10 == 0):
            fragment = normalizing_picture(reconstructed, helper)
            images.append(fragment)
            mse[iterator] = mean_squared_error(picture, fragment)
            iterator += 1
     
    reconstructed = normalizing_picture(reconstructed, helper)
    images.append(reconstructed)
    mse[iterator] = mean_squared_error(picture, reconstructed)
    iterator += 1
    save_plot(iterator, mse, 'mse_s2p')
    imageio.mimsave('sin2pic.gif', images)

    return reconstructed

def filtered_sinogram2picture(picture, sinogram, lines):
    
    picture_shape = np.shape(picture)
    width = picture_shape[0]
    height = picture_shape[1]
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    images = []
    iterator = 0
    mse = np.zeros(ceil(number_of_projections/10)+2)
    
    reconstructed = np.zeros(shape = picture_shape)
    helper = np.zeros(shape = picture_shape)
    
    new_sinogram = filtering_sinogram(sinogram)
    
    # obserwacje
    plot_images(picture,new_sinogram)
    plot_diagram(sinogram, new_sinogram)
    
    new_sinogram = normalizing_sinogram(new_sinogram)
    
    # obserwacje
    plot_images(picture,new_sinogram)
    plot_diagram(sinogram, new_sinogram)
    
    for projection in range (0, number_of_projections, 1):
        for detector in range (0, number_of_detectors, 1):
            x0, y0, x1, y1 = lines[projection][detector]
            line = bresenhams_line(x0, y0, x1, y1)
            value = new_sinogram[projection][detector]
            for i in range (0, len(line), 1):
                    x, y = line[i]
                    if x >= 0 and y >= 0 and x < width and y < height:
                        reconstructed[int(x)][int(y)] += value
                        helper[int(x)][int(y)] += 1
        
        if (projection%10 == 0):
            fragment = normalizing_picture(reconstructed, helper)
            images.append(fragment)
            mse[iterator] = mean_squared_error(picture, fragment)
            iterator += 1
    
    
    reconstructed = normalizing_picture(reconstructed, helper)
    images.append(reconstructed)
    mse[iterator] = mean_squared_error(picture, reconstructed)
    iterator += 1
    plot_images(picture,reconstructed)
    reconstructed[reconstructed[:,:] < 0] = 0
    #reconstructed = filtering_picture(reconstructed)
    #images.append(reconstructed)
    mse[iterator] = mean_squared_error(picture, reconstructed)
    iterator += 1
    imageio.mimsave('fil_sin2pic.gif', images)
    save_plot(iterator, mse, 'mse_fs2p')
    return reconstructed

def filtering_sinogram(sinogram):
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    filtered = np.zeros((number_of_projections, number_of_detectors))
    
    # maska jednowymiarowa
    mask_size = floor(number_of_detectors/5)
    #mask_size = 3
    mask = np.zeros(mask_size)
    center = floor(mask_size/2)
    for i in range(0, mask_size, 1):
        k = i - center
        if k % 2 != 0:
            mask[i] = (-4/np.pi**2)/k**2
    mask[center] = 1
    
    # splot każdej projekcji z naszą maską
    for projection in range (0, number_of_projections, 1):
        filtered[projection] = sig.convolve(sinogram[projection], mask, mode = 'same', method='direct')
    
    return filtered

def filtering_picture(img) :
    #new = filters.median(img, disk(2))
    new = filters.gaussian_filter(img, sigma=1)
    # korekcja gamma
    gamma = 1/2.2
    new = (new ** gamma)
    
    perc = 10
    MIN = np.percentile(img, perc)
    MAX = np.percentile(img, 100-perc)
    new = normalizing(img, MIN, MAX)
    #new = normalizing(img, 0, 1)
    #new = mp.erosion(img)
    #new = filters.median(new, disk(2))
    #new = filters.gaussian_filter(img, sigma=1)

    return new

def normalizing_sinogram(sinogram):
    
    norm = np.copy(sinogram)
    #norm[norm[:,:] < 0] = 0
    
    minval = 0
    maxval = sinogram.max()
    
    width = np.shape(sinogram)[0]
    height = np.shape(sinogram)[1]
    for i in range (0, width, 1):
        for j in range (0, height, 1):
            norm[i][j] = (sinogram[i][j] - minval) / (maxval - minval)
    
    # druga normalizacja do "rozciągnięcia" histogramu
    perc = 5
    MIN = np.percentile(norm, perc)
    MAX = np.percentile(norm, 100-perc)
    #norm = normalizing(norm, MIN, MAX)
    
    # korekcja gamma
    #gamma = 1/2.2
    #norm = (norm ** gamma)
   
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

def plot_images(img1, img2):
    fig, plots = plt.subplots(1, 2)
    plots[0].imshow(img1, cmap='gray')
    plots[1].imshow(img2, cmap='gray')
    plt.show()
    
def plot_diagram(img1, img2):
    fig, plots = plt.subplots(1, 2)
    plots[0].plot(range(np.shape(img1)[1]), img1[0])
    plots[1].plot(range(np.shape(img2)[1]), img2[0])
    plt.show()  
    
def save_plot(x, y, filename):
    plt.plot(range(x), y)
    plt.savefig(filename)  