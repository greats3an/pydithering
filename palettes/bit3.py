'''3-bit quantization'''
import numpy
def palette(rgb):
    return [(int(i) >> 7) * 255 for i in rgb]