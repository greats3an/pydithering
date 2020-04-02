'''
Ordered Dithering using Bayer Matrix

        src         :     A 2-D `numpy.ndarray`
        palette     :     Palette method from `palettes`
        n           :     Scale of the matrix
        threshold   :     Decides the dither threshold,a list [255,255,255] or a string '255;255;255'
'''
from PIL import Image
from . import clamp
import numpy

def dither(src : numpy.ndarray,palette,n=4,threshold='255;255;255'):
    src = src.astype(numpy.int)
    def BayerMatrix(n):
        # Recurisly generate a Bayer Matrix from Threshold Map
        def ThresholdMap(n):
            if n == 2:
                return numpy.array([[0, 2], [3, 1]], dtype='int')
            else:
                smaller_map = ThresholdMap(n >> 1)  # Equvilant of n / 2
                return numpy.bmat([
                    [4 * smaller_map,     4 * smaller_map + 2],
                    [4 * smaller_map + 3, 4 * smaller_map + 1]
                ])
        return numpy.array((ThresholdMap(n) + 1) / n ** 2 - 0.5)
    n = int(n);threshold = numpy.squeeze(numpy.array(numpy.mat(threshold), 'uint8'))
    bayer_matrix = BayerMatrix(n)
    for y in range(0,len(src)):
        for x in range(0,len(src[y])):
           # Applies threshold to every pixel
           src[y][x] = palette(clamp(src[y][x] + threshold * (bayer_matrix[y % n][x % n])))
    
    return src.astype(numpy.uint8)