from PIL import Image
import os
folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis"
file_names = (os.listdir(r"{}\images\\".format(folder_name)))
tiff_file_names = [name for name in file_names if '.tif' in name ]

for file_name in tiff_file_names:
    #  ignore the jpeg already existed
    if file_name.replace('.tif', '.jpg') not in file_names:
        print(file_name)
        im = Image.open(r'{}\images\{}'.format(folder_name, file_name))
        # im = im.convert('L')
        im.mode = 'I'
        im.point(lambda i:i*(1./256)).convert('L').save(r'{}\images\{}'.format(folder_name, file_name).replace('.tif', '.jpg'))