import os
filepath = 'D:/temp/DOngpo opendat/SI Figure 14/BBCP1 - temperature/'
filenames = os.listdir(filepath)


for filename in filenames:
    new_filename = filename.replace('uf-34F-slideB-50x-ball-1-', 'BBCP1-50x-')
    os.rename(filepath+filename, filepath+new_filename)

