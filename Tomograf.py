#!/usr/bin/python
import sys
#from plikKrzysia import picture2sinogram
#from plikAgi import sinogram2picture
import plikKrzysia
import plikAgi


class Result:
    def __init__(self, picture = []):
        self.raw = picture
        self.imporved = picture

class Picture_struct:
    'Structure of our picture'
    oryginal = []
    sinogram = []
    filtered = []
    result = Result()

    def picture2sinogram(self):
        #Should return array [n][n] which is result of the function  .. from  plikKrzysia
        self.sinogram = plikKrzysia.picture2sinogram(self.oryginal)
        return self.sinogram

    def sinogram2picture(self):
        self.result.raw = plikAgi.sinogram2picture(self.sinogram)
        self.result.improved = plikAgi.sinogram2picture(self.filtered)
        return self.result

    def filtering(self):
        self.filtered = plikAgi.filtered(self.sinogram)
        return self.filtered

def tomograf( picture_ ):
    picture = Picture_struct(picture_)
    picture.picture2sinogrm()
    picture.filtered()
    picture.sinogram2picture()
    return picture

if __name__ == "main":
    if(len(sys.argv) != 2):
        print("This program requires a bitmap picture as an argument")
    tomograf(sys.argv[1])