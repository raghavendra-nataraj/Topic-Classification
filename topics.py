import sys
import os
import glob

MODES = {"train", "test"}

try:
    mode = sys.argv[1]
    directory = sys.argv[2]
    model_path = sys.argv[3]
    fraction = sys.argv[4]
except IndexError:
    print("Usage: python topics.py mode dataset-directory model-file")
    sys.exit(1)

if mode not in MODES:
    print("Invalid mode. Allowed values: train, test")
    sys.exit(2)

if not os.path.isdir(directory):
    print("Directory" + directory + " does not exist")
    sys.exit(3)

try:
    fraction = float(fraction)
except ValueError:
    print("Fraction should be equal or between 0 and 1")
    sys.exit(4)

if fraction < 0 or fraction > 1:
    print("Fraction should be equal or between 0 and 1")
    sys.exit(5)

file_list = []
for path, dirs, files in os.walk(directory):
    for dir in dirs:
        pa = path + "/" + dir
        for p,d,f in os.walk(pa):
            for fil in f:
                file_list.append((path,dir,fil))

for file in file_list:
    f = open(file[0]+"/"+file[1]+"/"+file[2],'r')
    text = f.readlines()
    print text



