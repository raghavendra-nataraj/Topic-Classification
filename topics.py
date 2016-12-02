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
    for f in email_text:
        if mode == "train":
            decision = flip(fraction)
            if decision == True:
                classification = folders
                supervised_list.append((f, folders))
            else:
                unsupervised_list.append((f, folders))
        elif mode == "test":
            unsupervised_list.append((f, folders))

# pprint.pprint(unsupervised_list)
# pprint.pprint(supervised_list)

if mode == "train":
    model = Model.Model(dirs)
    model.train(supervised_list, unsupervised_list, dirs)
    model.save(file_path)
if mode == "test":
    model = Model.Model(dirs)
    model.load(file_path)

    result_dictionary = {}
    for classes in dirs:
        result_dictionary[classes] = {"Correct": 0, "Incorrect": 0}
    successes=0
    totals=0
    predictions={}
    for email_file, topic in unsupervised_list:
        prediction = model.test(email_file, dirs)
        if prediction not in predictions:
            predictions[prediction]=0
        predictions[prediction]+=1

        if prediction != None:
            totals+=1
            if prediction == topic:
                result_dictionary[topic]['Correct'] += 1
                successes+=1
            else:
                result_dictionary[topic]['Incorrect'] += 1

    pprint.pprint(result_dictionary)
    pprint.pprint("Overall Accuracy:" +str((1.0*successes)/totals))
