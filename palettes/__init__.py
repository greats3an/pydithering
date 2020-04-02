'''
palettes Module

    Includes palettes for color quantization

        bit3       :        2^3 (8) Colors,aka pure RGB
        bit8       :        2^8 (256) Colors
        bw         :        Black & White from grayscale (<127)
        gray       :        Gray scale
        custom     :        Custom palettes.Used euclidian distance to match colors
'''
import os
def toRGB(src : int):
    return [src >> 16,src >> 8 & 0b11111111,src & 0b11111111]
def fromRGB(src):
    i = 0
    for n in list(src):
        i <<= 8;i |= n
    return i

__all__ = [i[:-3] for i in os.listdir(os.path.dirname(__file__)) if i[-2:] == 'py' and i != '__init__.py']
from . import *