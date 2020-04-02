'''8-bit quantization in 3-2-3 fashion'''
import numpy
def palette(rgba):
    return [
        (int(rgba[0]) & 0b11100000),
        (int(rgba[1]) & 0b11000000),
        (int(rgba[2]) & 0b11100000),
    ]