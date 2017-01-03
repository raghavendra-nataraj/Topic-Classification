   
import sys
import os
import random
import EmailParser
import Model
import pprint
from collections import Counter
MODES = {"train", "test"}

def flip():
    if random.random() > fraction:
        return False
    else:
        return True

try:
    mode = sys.argv[1]
    directory = sys.argv[2]
    file_path = sys.argv[3]
except IndexError:
    print("Usage: python topics.py mode dataset-directory model-file")
    sys.exit(1)
fraction=1
try:
    fraction = sys.argv[4]
except IndexError:
    pass
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

p = EmailParser.Parser()

supervised_list = []
unsupervised_list = []
test_list = []
for path, dirs, files in os.walk(directory):
    break
for folders in dirs:
    email_text = p.parse(directory + "/" + folders + "/")
    for f in email_text:
        if mode == "train":
            if(flip()):
                supervised_list.append((Counter(f), folders))
            else:
                unsupervised_list.append((f, folders))
        elif mode == "test":
            test_list.append((f, folders))


if mode == "train":
    model = Model.Model()
    model.train(supervised_list,unsupervised_list)
    model.save(file_path)

if mode == "test":
    model = Model.Model()
    model.load(file_path)
    model.test(test_list)
    
