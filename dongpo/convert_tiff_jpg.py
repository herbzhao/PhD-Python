from PIL import Image
im = Image.open(r'C:\Users\My Pc\Documents\GitHub\PhD-Python\dongpo\C3 - top view -03.tif')
# im = im.convert('L')
im.mode = 'I'
im.point(lambda i:i*(1./256)).convert('L').save(r'C:\Users\My Pc\Documents\GitHub\PhD-Python\dongpo\C3 - top view -03.jpg')