'''Rough grayscale quantization via `(R*38 + G*75 + B*15 + 50) / 128)`'''
import numpy
def palette(src : numpy.ndarray):    
    gray = int(src[0] * 38 + src[1] * 75 + src[2] * 15) >> 7
    return [gray,gray,gray]