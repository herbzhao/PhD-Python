from PIL import Image
import os
file_names = (os.listdir(r"images/"))
tiff_file_names = [name for name in file_names if '.tif' in name ]

for file_name in tiff_file_names:
    im = Image.open(r'images/{}'.format(file_name))
    # im = im.convert('L')
    im.mode = 'I'
    im.point(lambda i:i*(1./256)).convert('L').save(r'images/{}'.format(file_name).replace('.tif', '.jpg'))