import os
folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis\data"
file_names = (os.listdir(folder_name))
txt_file_names = [name.replace('.txt','') for name in file_names if '.txt' in name ]

print(txt_file_names) 