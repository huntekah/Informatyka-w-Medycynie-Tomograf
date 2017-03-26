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
from skimage.exposure import rescale_intensity, equalize_adapthist


def sinogram2picture(picture, sinogram, lines):
    reconstructed = sin2pic(picture, sinogram, lines, 'sin2pic.gif', 'mse_s2p', False)    
    return reconstructed

def filtered_sinogram2picture(picture, sinogram, lines):    
    sinogram = filtering_sinogram(sinogram)
    sinogram = normalizing_sinogram(sinogram) 
    reconstructed = sin2pic(picture, sinogram, lines, 'fil_sin2pic.gif', 'mse_fs2p', True)    
    return reconstructed

def filtering_sinogram(sinogram):
    
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    
    filtered = np.zeros((number_of_projections, number_of_detectors))
    mask = do_mask(number_of_detectors)
    
    # splot każdej projekcji z naszą maską
    for projection in range (0, number_of_projections, 1):
        filtered[projection] = sig.convolve(sinogram[projection], mask, mode = 'same', method='direct')
    
    return filtered

def do_mask(detectors):
    # maska jednowymiarowa
    mask_size = floor(detectors/2)
    mask = np.zeros(mask_size)
    center = floor(mask_size/2)
    for i in range(0, mask_size, 1):
        k = i - center
        if k % 2 != 0:
            mask[i] = (-4/np.pi**2)/k**2
    mask[center] = 1
    return mask

def filtering_picture(img) :
    #new = filters.median(img, disk(2))
    new = filters.gaussian_filter(img, sigma=1)

    #new = gamma(new, 1/2.2)
    MIN = new.min()
    MAX = new.max()
    print("max ", MAX);
    MAX = 0.2
    #new = normalizing(new, MIN, MAX)
    new = rescale_intensity(new)
    new = mp.dilation(mp.erosion(new))
    #new = normalizing(new, MIN, MAX)
    
    """
    perc = 10
    MIN = np.percentile(new, perc)
    MAX = np.percentile(new, 100-perc)
    new = normalizing(new, MIN, MAX)
    new = normalizing(img, 0, 1)
    new = mp.erosion(img)
    new = filters.median(new, disk(2))
    new = filters.gaussian_filter(img, sigma=1)
    """
    #new = mp.dilation(mp.erosion(new))
    return new


def gamma(img, gamma):
    new = img ** gamma
    return new

def normalizing_sinogram(sinogram):
    
    norm = np.copy(sinogram)
    #norm[norm[:,:] < 0] = 0
    """
    minval = 0
    maxval = sinogram.max()
    
    width = np.shape(sinogram)[0]
    height = np.shape(sinogram)[1]
    for i in range (0, width, 1):
        for j in range (0, height, 1):
            norm[i][j] = (sinogram[i][j] - minval) / (maxval - minval)
    """
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
    
def sin2pic(picture, sinogram, lines, filename1, filename2, filtr):
    
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
    
    # obserwacje
    plot_images(picture, sinogram)
    plot_diagram(sinogram, sinogram)
    
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
        fragment = normalizing_picture(reconstructed, helper)
        fragment[fragment[:,:] < 0] = 0
        images.append(gamma(fragment, 0.3))
        if (projection%10 == 0):
            mse[iterator] = mean_squared_error(picture, fragment)
            iterator += 1
    
    reconstructed = normalizing_picture(reconstructed, helper)
    images.append(gamma(reconstructed, 0.3))
    mse[iterator] = mean_squared_error(picture, reconstructed)
    iterator += 1
    plot_images(picture,reconstructed)
    if (filtr):
        reconstructed[reconstructed[:,:] < 0] = 0
        reconstructed = filtering_picture(reconstructed)
    images.append(gamma(reconstructed, 0.3))
    #images.append(reconstructed)
    mse[iterator] = mean_squared_error(picture, reconstructed)
    iterator += 1
    imageio.mimsave(filename1, images)
    save_plot(iterator, mse, filename2)
    return reconstructed

    