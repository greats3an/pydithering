'''
ditherers Module

    Includes some common dithering methods and utilities for dithering

    Implemented methods are:

        diffusion       :       Error diffusion dithering,maps included
        nodither        :       No dithering.Yet still applies palette given
        ordered         :       Bayer-Matrix Threshold Dithering
'''
import numpy,os
class Ditherer():
    def __init__(self,ditherer,palette):
        self.ditherer = ditherer
        self.palette = palette

    def __call__(self,src : numpy.ndarray,*args,**kwargs):
        '''
            src     :       Image /  Array,[R G B] per pixel
        '''
        return(self.ditherer.dither(numpy.array(src),self.palette.palette,*args,**kwargs))

def clamp(arr):
    '''
        Inputs an array,for every value of the array,
        
        Values greater than 255 will be 255,and values less than 0 will be 0

            arr     :       iterable
    '''
    return numpy.array([int(i) if i < 256 and i > -1 else 255 if i > 256 else 0 for i in arr])

def parse_config(config):
    '''
        Returns ditherer,palette,extra via args

        Expecting input like:

        {'ditherer':ordered,'palette':'3bit','extra':"diffmap='floyd-steinberg'"}
    '''
    import ditherers,palettes

    result = {'ditherer':None,'palette':None,'extra':{}}
    for k,v in config.items():
        if k == 'extra':result[k] = {(i := e.split('='))[0] : i[1] for e in v.split(',')} if '=' in v else {}
        if k == 'ditherer':result[k] = getattr(ditherers,v)
        if k == 'palette':result[k] = getattr(palettes,v)
    return result

__all__ = [i[:-3] for i in os.listdir(os.path.dirname(__file__)) if i[-2:] == 'py' and i != '__init__.py']
from . import *    
