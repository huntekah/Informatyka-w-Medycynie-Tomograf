#!/usr/bin/python
from utils import bresenhams_line
import numpy as np


class Pixel:
    def __init__(self):
        self.maximum = int(0)
        self.normalized = np.float(0)
        self.raw = np.float(0)


def picture2sinogram(picture, **kwargs):
    options = {
        'width': 90,
        'detector_amount': 360,
        'alpha': 2
    }
    options.update(kwargs)

    # szerokość rozstawu detektorów
    width = options['width']

    # ilość detektorów
    detector_amount = options['detector_amount']

    # kąt obrotu
    alpha = options['alpha']

    picture_size = len(picture[0])
    r = int(np.ceil(np.sqrt(picture_size * picture_size)))

    sinogram = []
    lines = []

    # poruszaj emiterem 360/n razy o kąt alpha i zbierz próbki promieni.
    for i in range(0, 360, alpha):
        sinogram.append([])
        lines.append([])
        for detector in range(0, detector_amount):
            x0 = r * np.cos(i * np.pi / 180)
            y0 = r * np.sin(i * np.pi / 180)

            x1 = r * np.cos((i + 180 - width / 2 + detector * (width / (detector_amount - 1))) * np.pi / 180)
            y1 = r * np.sin((i + 180 - width / 2 + detector * (width / (detector_amount - 1))) * np.pi / 180)

            x0 = int(x0) + np.floor(picture_size / 2)
            x1 = int(x1) + np.floor(picture_size / 2)
            y0 = int(y0) + np.floor(picture_size / 2)
            y1 = int(y1) + np.floor(picture_size / 2)

            # if(np.sqrt(np.power(x0-x1,2) + np.power(y0-y1,2)) < 512 ):
            #    print(x0,y0,x1,y1)
            line = bresenhams_line(x0, y0, x1, y1)

            pixel = get_pixel_value(picture, line)
            sinogram[-1].append(pixel.normalized)
            lines[-1].append([x0, y0, x1, y1])

    return sinogram, lines


def get_pixel_value(picture, line):
    pixel = Pixel()
    for pos in line:
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] < len(picture) and pos[1] < len(picture):
            pixel.raw = pixel.raw + float(picture[pos[0], pos[1]])
            pixel.maximum = pixel.maximum + 1
    if pixel.maximum != 0:
        pixel.normalized = pixel.raw / pixel.maximum
    else:
        print(line[0][0], line[0][1], line[-1][1], line[-1][0])
    return pixel
