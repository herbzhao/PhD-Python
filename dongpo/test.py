import csv
#  read xyzr from the csv generated from SEM image
with open(r'C:\Users\My Pc\Documents\GitHub\PhD-Python\dongpo\test.csv', newline='\n') as file:
    csv_reader = csv.reader(file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
            x,y,z,r = row
            print([float(x),float(y),float(z),float(r)])