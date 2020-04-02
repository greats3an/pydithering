import ditherers,palettes
from PIL import Image
import numpy,os

ditherer,palette = ditherers.ordered,palettes.bw
dither = ditherers.Ditherer(ditherer,palette)

os.chdir('demos')
demos = [
    i for i in os.listdir() if i [-3:] == 'png' or i [-3:] == 'jpg'
]

src = Image.open(src_path := input(f'Image path\n   Demos:{"|".join(demos)}\n'))

print(f"""Rendering...
Ditherer :: {ditherer.__name__.split('.')[-1]}
Palette  :: {palette.__name__.split('.')[-1]}""")

img = Image.new('RGB',src.size)
img.paste(src)
try:
    arr = dither(numpy.array(img))
    img_out = Image.fromarray(arr)
    img_out.show()
except Exception as e:
    input(e)
if (target := input(f'Save as...')):img_out.save(target)