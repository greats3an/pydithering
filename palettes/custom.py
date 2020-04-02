'''
Custom palette color quantization

Defaults to Bisqwit's palette (https://bisqwit.iki.fi/story/howto/dither/jy/) as shown here

To modify the palette,access this module's `custom_palette` property
'''
import math,numpy
from . import toRGB,fromRGB
custom_palette = [
    0x080000, 0x201A0B, 0x432817, 0x492910,
    0x234309, 0x5D4F1E, 0x9C6B20, 0xA9220F,
    0x2B347C, 0x2B7409, 0xD0CA40, 0xE8A077,
    0x6A94AB, 0xD5C4B3, 0xFCE76E, 0xFCFAE2
]
# Colors are in R,G,B format
def palette(src : numpy.ndarray):
    if fromRGB(src) in custom_palette:return src
    def dist(r1,b1,g1,r2,b2,g2):
        # Euclidean Distance,gets the distance between two points in space
        # √(ΔRed² + ΔGreen² + ΔBlue²)
        dr,dg,db = r1-r2,b1-b2,g1-g2
        return dr**2 + dg**2 + db ** 2
    dmin,match = 512,0
    for pal in custom_palette:
        dnow = dist(*toRGB(pal),*src)
        if (dnow < dmin):
            dmin = dnow;match = pal

    return toRGB(match)