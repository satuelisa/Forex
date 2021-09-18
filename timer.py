from sys import argv
seconds = float(argv[1]) - float(argv[2])
minutes = seconds / 60
hours = minutes / 60
print(hours)
