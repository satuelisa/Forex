from sys import argv
filename = argv[1].split('/')[-1]
filename = filename.replace('-', '')
filename = filename.replace('=X', '')
print(filename[:-4]) # remove .csv
