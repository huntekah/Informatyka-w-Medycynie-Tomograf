#!/usr/bin/python

def picture2sinogram(picture, **kwargs ):
    options = {
        'width': 90,
        'detector_amount': 180,
        'alpha': 5
    }
    options.update(kwargs)

    width = options['width']
    detector_amount = options['detector_amount']
    alpha = options['alpha']

    #poruszaj emiterem 360/n razy o kąt alpha i zbierz próbki promieni.
    for i in range(0,360,alpha) :
        pass

    #TODO do transformations
    return picture