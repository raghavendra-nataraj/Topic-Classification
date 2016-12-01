import sys
import os
import random
import EmailParser
import Model
import pprint

MODES = {"train", "test"}

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


# Probability Coin flip function  (stack overflow)
def flip(p):
    return True if random.random() < p else False


p = EmailParser.Parser()

supervised_list = []
unsupervised_list = []
file_list = []
i = 0
dirs = []
for path, dirs, files in os.walk(directory):
    break
for folders in dirs:
    email_text = p.parse(directory + "/" + folders + "/")
    if mode == "train":
        decision = flip(fraction)
        if decision == True:
            classification = folders
            supervised_list.append((email_text, folders))
        else:
            unsupervised_list.append((email_text, folders))
    elif mode == "test":
        unsupervised_list.append((email_text, folders))

if mode == "train":
    model = Model.Model()
    model.train(supervised_list, unsupervised_list, dirs)
    model.save(file_path)
if mode == "test":
    model = Model.Model()
    model.load(file_path)
    # print model

    result_dictionary = {}
    for classes in dirs:
        result_dictionary[classes] = {"yes": 0, "no": 0}
    successes=0
    totals=0
    for file_list, topic in unsupervised_list:
        for text in file_list:
            if len(text) == 0:
                prediction = "atheism"
            else:
                prediction = model.test(text, dirs)
            if prediction != None:
                totals+=1
                if prediction == topic:
                    result_dictionary[topic]['yes'] += 1
                    successes+=1
                else:
                    result_dictionary[topic]['no'] += 1

    pprint.pprint(result_dictionary)
    pprint.pprint((1.0*successes)/totals)
