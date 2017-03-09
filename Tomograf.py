#!/usr/bin/python
import sys
# from plikKrzysia import picture2sinogram
# from plikAgi import sinogram2picture
import plikKrzysia
import plikAgi
from matplotlib import pyplot as plt
from skimage import data


class Result:
    def __init__(self, picture=[]):
        self.raw = picture
        self.imporved = picture


class Picture_struct:
    'Structure of our picture'
    oryginal = []
    sinogram = []
    filtered = []
    result = Result()

    def __init__(self, picture_):
        self.oryginal = picture_

    def picture2sinogram(self):
        # Should return array [n][n] which is result of the function  .. from  plikKrzysia
        # lines n x n x 4 array of lines
        self.sinogram, self.lines = plikKrzysia.picture2sinogram(self.oryginal, width=45, detector_amount=5, aplha=36)
        fig, plots = plt.subplots(1, 2)
        plots[0].imshow(self.oryginal, cmap='gray')
        plots[1].imshow(self.sinogram, cmap='gray')
        for line in self.lines[60]:
            line_ = plikKrzysia.bresenhams_line(line[2], line[3], line[0], line[1])
            x = [x[0] for x in line_]
            y = [x[1] for x in line_]
            plots[0].scatter(x=x, y=y, c='red', s=4)
        plt.show(block=True)
        return self.sinogram

    def sinogram2picture(self):
        self.result.raw = plikAgi.sinogram2picture(self.sinogram)
        self.result.improved = plikAgi.sinogram2picture(self.filtered)
        return self.result

    def filtering(self):
        self.filtered = plikAgi.filtered(self.sinogram)
        return self.filtered


def tomograf(picture_):
    picture = Picture_struct(picture_)
    picture.picture2sinogram()
    #    picture.filtered()
    #    picture.sinogram2picture()
    return picture


if __name__ == "__main__":
    # if (len(sys.argv) != 2):
    #    print("This program requires a bitmap picture as an argument")
    # tomograf(sys.argv[1])
    picture = data.binary_blobs(length=10, blob_size_fraction=0.1, n_dim=2, volume_fraction=0.5, seed=None)
    tomograf(picture)
