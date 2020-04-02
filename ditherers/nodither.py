'''
No dithering yet still applies the palette        
        src         :     A 2-D `numpy.ndarray`
        palette     :     Palette method from `palettes`        
'''
from PIL import Image
import numpy
def dither(src : numpy.ndarray,palette):
    for y in range(0,len(src)):
        for x in range(0,len(src[y])):
           src[y][x] = palette(src[y][x])

    return src    
