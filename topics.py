import sys
import os
import random
import EmailParser
import Model

MODES = {"train", "test"}

try:
    mode = sys.argv[1]
    directory = sys.argv[2]
    file_path = sys.argv[3]
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


# Probability Coin flip function  (stack overflow)
def flip(p):
    return True if random.random() < p else False


p = EmailParser.Parser()

supervised_list = []
unsupervised_list = []
file_list = []
class_list = []
i = 0
dirs = []
for path, dirs, files in os.walk(directory):
    break
for folders in dirs:
    email_text = p.parse(directory + "/" + folders + "/")
    decision = flip(fraction)
    if decision == True:
        classification = folders
        supervised_list.append((email_text,folders))
    else:
        unsupervised_list.append(email_text)

if mode == "train":
    model = Model.Model()
    model.train(supervised_list, unsupervised_list, class_list)
    model.save(file_path)
if mode == "test":
    model = Model.Model()
    model.load(file_path)
    print model
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for text in email_texts:
        prediction = model.test(text)
        if prediction == "spam":
            true_positive += 1
        else:
            false_negative += 1
    for text in non_spam_email_texts:
        prediction = model.test(text)
        if prediction == "notspam":
            true_negative += 1
        else:
            false_positive += 1
    print len(spam_email_texts)
    print len(non_spam_email_texts)
    print("True Positive" + str(true_positive))
    print("True Negative" + str(true_negative))
    print("False Positive" + str(false_positive))
    print("False Negative" + str(false_negative))
