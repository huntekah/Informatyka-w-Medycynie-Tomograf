#!/usr/bin/python
from utils import bresenhams_line
import numpy as np


def picture2sinogram(picture, **kwargs):
    options = {
        'width': 90,
        'detector_amount': 180,
        'alpha': 5
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

    # poruszaj emiterem 360/n razy o kąt alpha i zbierz próbki promieni.
    for i in range(0, 360, alpha):
        x0 = r * np.cos(i * np.pi / 180)
        y0 = r * np.sin(i * np.pi / 180)
        x1 = r * np.cos( i + 180)
        pass

    # TODO do transformations
    return picture


def ray(a, b):
    pass

    ## Ray from alha to  180+alpha
