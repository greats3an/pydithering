'''black-and-white quantization'''
import numpy
from . import gray
def palette(src : numpy.ndarray):    
    return [(int(i) >> 7) * 255 for i in gray.palette(src)]