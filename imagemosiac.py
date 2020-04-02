import ditherers,palettes
from PIL import Image
import numpy,os,copy,argparse,sys

parser = argparse.ArgumentParser(description='PyDithering Image Mosiac Tool',formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('src', metavar='SRC_PATH',help='Path to the source image to be processed')
parser.add_argument('dir',metavar='MOSIAC_DIR',help='Path to folder containing the "mosiac block" images')
parser.add_argument('dst',metavar='DESTINATION',help='File save path')

parser.add_argument('--ditherer', metavar='DITHERER',help=ditherers.__doc__,default='ordered')
parser.add_argument('--dit-extra', metavar='EXTRA',help=f'Extra arguments for the ditherer e.g. diffmap=floydstienberg',default='?')

parser.add_argument('--mosiac-size',metavar='MSIZE',help='Width (in square) of the mosiac block',default=32)
parser.add_argument('--mosiac-alpha',metavar='MALPHA',help='Alpha (0~255) of the mosiac block',default=255)
parser.add_argument('--resize-factor',metavar='RFACTOR',help='Resize factor for the source image',default=0.1)
parser.add_argument('--show',help='Show the image when done',action='store_true')
parser.add_argument('--only-overlay',help='Generate transparent overlay only',action='store_true')
if len(sys.argv) < 2:
    parser.print_help()
    print('\nDefaults:',' '.join([f'{k}:{v}' for k,v in parser.parse_args('? ?').__dict__.items()]))
    sys.exit(2)
else:
    args = parser.parse_args()
    args = args.__dict__

src_image = Image.open(args['src'])
mosiac_dir = args['dir']
dst = args['dst']
mosiac_size = int(args['mosiac_size'])
mosiac_alpha = int(args['mosiac_alpha'])
resize_factor = float(args['resize_factor'])
show = args['show']
only_overlay = args['only_overlay']

ditherer,extra = (cfg := ditherers.parse_config(args))['ditherer'],cfg['extra']

src_fsize = (int(src_image.size[0] * resize_factor),int(src_image.size[1] * resize_factor))
dither = ditherers.Ditherer(ditherer,palettes.custom)
output_size = (mosiac_size * src_fsize[0],mosiac_size * src_fsize[1])
mosiacs = [
    os.path.join(mosiac_dir,i) for i in os.listdir(mosiac_dir) if i.split('.')[-1] in 'jpg|png|gif|jpeg|tiff'
]

print(f'''PyDithering Image Mosiac Tool
Ditherer                      ::  {ditherer.__name__}
Mosiac size                   ::  {mosiac_size}
Mosiac alpha                  ::  {mosiac_alpha}
Output size                   ::  {output_size}
Resize Factor                 ::  {resize_factor}
Base (resized) size           ::  {src_fsize}
Overlay only                  ::  {only_overlay}
Loading mosiacs...''')

def GetImage(src):
    try:
        img = Image.open(src)
        return img.resize((mosiac_size,mosiac_size))
    except Exception:return None
mosiacs = [
    pic for i in mosiacs if (pic := GetImage(i))
]
# Resizes all mosiacs

def GetDominantColor(img,count=1):
    img = img.resize((8,8))
    img = img.convert('RGB', palette=Image.ADAPTIVE, colors=count)
    return palettes.fromRGB(img.getcolors()[0][1])
print('Extracting dominant colors of mosiac blocks...')    
# Extract dominant colors

mosiac_palette = {}
for mosiac in mosiacs:
    domniant = GetDominantColor(mosiac)
    def UnqiueKey(k):
        if not k in mosiac_palette.keys():return k
        return UnqiueKey(k+1)
    mosiac.putalpha(mosiac_alpha)
    mosiac_palette[UnqiueKey(domniant)] = mosiac.convert('RGBA')

palettes.custom.custom_palette = mosiac_palette.keys()
# Creates a dictionary where the image as the data ,and its domniant color as key

print('Total of',len(mosiac_palette.keys()),'colors were extracted from images')
print('Rendering dithered image...')

if not only_overlay:
    plot = src_image.resize(output_size);plot = plot.convert('RGBA');
else:
    plot = Image.new('RGBA',output_size)
src_image = src_image.resize(src_fsize);src_image = src_image.convert('RGB');src_image = dither(src_image)

# Dithers the Image with the newly created palette

print('Rendering plotted image...')
for y in range(0,len(src_image)):
    for x in range(0,len(src_image[y])):
        col = palettes.fromRGB(src_image[y][x])
        if col in mosiac_palette.keys():pass
        else:col = palettes.fromRGB(palettes.custom.palette(src_image[y][x]))
        # Sometimes the error got diffused yet not compeletly quantaized
        # I'm looking forward to solutions more elegant than this
        im = mosiac_palette[col]
        # Image,Box,Mask
        plot.paste(im,(x * mosiac_size,y * mosiac_size),im)

plot.save(dst)
if show:os.system(dst)