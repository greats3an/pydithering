'''
Error Diffusion dithering

        src         :     A 2-D `numpy.ndarray`
        palette     :     Palette method from `palettes`
        diffmap     :     Diffusion Map 'key'       

The list of diffusion map keys:
    
        floyd-steinberg|atkinson|jarvis-judice-ninke|stucki|burkes|sierra3|sierra2|sierra-2-4a|stevenson-arce
'''
from PIL import Image
from . import clamp
import numpy

def dither(src: numpy.ndarray, palette,diffmap='floyd-steinberg'):
    # diffusion maps from https://github.com/hbldh/hitherdither/blob/master/hitherdither/diffusion.py
    diffusionmaps = {
        'floyd-steinberg': (
            (1, 0,  7 / 16),
            (-1, 1, 3 / 16),
            (0, 1,  5 / 16),
            (1, 1,  1 / 16)
        ),
        'atkinson': (
            (1, 0,  1 / 8),
            (2, 0,  1 / 8),
            (-1, 1, 1 / 8),
            (0, 1,  1 / 8),
            (1, 1,  1 / 8),
            (0, 2,  1 / 8),
        ),
        'jarvis-judice-ninke': (
            (1, 0,  7 / 48),
            (2, 0,  5 / 48),
            (-2, 1, 3 / 48),
            (-1, 1, 5 / 48),
            (0, 1,  7 / 48),
            (1, 1,  5 / 48),
            (2, 1,  3 / 48),
            (-2, 2, 1 / 48),
            (-1, 2, 3 / 48),
            (0, 2,  5 / 48),
            (1, 2,  3 / 48),
            (2, 2,  1 / 48),
        ),
        'stucki': (
            (1, 0,  8 / 42),
            (2, 0,  4 / 42),
            (-2, 1, 2 / 42),
            (-1, 1, 4 / 42),
            (0, 1,  8 / 42),
            (1, 1,  4 / 42),
            (2, 1,  2 / 42),
            (-2, 2, 1 / 42),
            (-1, 2, 2 / 42),
            (0, 2,  4 / 42),
            (1, 2,  2 / 42),
            (2, 2,  1 / 42),
        ),
        'burkes': (
            (1, 0,  8 / 32),
            (2, 0,  4 / 32),
            (-2, 1, 2 / 32),
            (-1, 1, 4 / 32),
            (0, 1,  8 / 32),
            (1, 1,  4 / 32),
            (2, 1,  2 / 32),
        ),
        'sierra3': (
            (1, 0,  5 / 32),
            (2, 0,  3 / 32),
            (-2, 1, 2 / 32),
            (-1, 1, 4 / 32),
            (0, 1,  5 / 32),
            (1, 1,  4 / 32),
            (2, 1,  2 / 32),
            (-1, 2, 2 / 32),
            (0, 2,  3 / 32),
            (1, 2,  2 / 32),
        ),
        'sierra2': (
            (1, 0,  4 / 16),
            (2, 0,  3 / 16),
            (-2, 1, 1 / 16),
            (-1, 1, 2 / 16),
            (0, 1,  3 / 16),
            (1, 1,  2 / 16),
            (2, 1,  1 / 16),
        ),
        'sierra-2-4a': (
            (1, 0,  2 / 4),
            (-1, 1, 1 / 4),
            (0, 1,  1 / 4),
        ),
        'stevenson-arce': (
            (2, 0,   32 / 200),
            (-3, 1,  12 / 200),
            (-1, 1,  26 / 200),
            (1, 1,   30 / 200),
            (3, 1,   30 / 200),
            (-2, 2,  12 / 200),
            (0, 2,   26 / 200),
            (2, 2,   12 / 200),
            (-3, 3,   5 / 200),
            (-1, 3,  12 / 200),
            (1, 3,   12 / 200),
            (3, 3,    5 / 200)
        )
    }
    if not diffmap in diffusionmaps.keys():
        raise Exception(f'Invalid diffusion map type.Only the followings are accepted:\n    {"|".join(diffusionmaps.keys())}')
        return None
    quant_error = numpy.array([0, 0, 0]);src = src.astype(numpy.int)
    # in case of overflow,use `numpy.int` instead of `numpy.uint8`
    # overflow will be explicitly processed(`clamp()`)
    for y in range(0, len(src)):
        for x in range(0, len(src[y])):
            pixel = src[y][x];new_pixel = palette(pixel)
            quant_error = pixel - new_pixel
            # caculates quantization error,then spread them via the map 
            src[y][x] = new_pixel           
            for m in diffusionmaps[diffmap]:
                if 0 <= x + m[0] < len(src[y]) and 0 <= y + m[1] < len(src):
                    src[y + m[1]][x + m[0]] = clamp(src[y + m[1]][x + m[0]] + quant_error * m[2])
                      
    # converts the finished int array back to uint8                
    return src.astype(numpy.uint8)