from PIL import Image
import os
import numpy as np

folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis\images\20200318 - 1to50\tiff"
file_names = (os.listdir(r"{}".format(folder_name)))
tiff_file_names = [name for name in file_names if '.tif' in name ]

for file_name in tiff_file_names:
    #  ignore the jpeg already existed
    if file_name.replace('.tif', '.jpg') not in file_names:
        print(file_name)
        im = Image.open(r'{}\{}'.format(folder_name, file_name))
        im.mode = "L"

        # im = im.convert('L')
        # im.mode = 'I'
        # im.convert('L')
        im.save(r'{}\{}'.format(folder_name, file_name).replace('.tif', '.jpg'))
        # im.convert('L').save(r'{}\{}'.format(folder_name, file_name).replace('.tif', '.jpg'))
