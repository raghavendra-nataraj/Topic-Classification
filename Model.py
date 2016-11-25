import sys
import re

sys.setrecursionlimit(9999)


class Model:
    def __init__(self):
        True

    def train(self, sl, ul, class_list):

        ld = {}
        # training using the supervised learning list
        for classification, file in sl:
            with open("train/" + classification + "/" + file, 'r') as f:
                for line in f:
                    word = re.split(' |\@|\+|\*|_|/|\\|-|--|:|\.|,|\n|=|!|\t|<|>|"|;|\)|\(|\[|\]|\'|\$|\?|\#|\^|%|&',
                                    line)
                    word = [x for x in word if x]
                    for w in word:
                        if classification in ld:
                            if w in ld[classification]:
                                ld[classification][w] += 1
                            else:
                                ld[classification][w] = 1
                        else:
                            tmp = {}
                            tmp[w] = 1
                            ld[classification] = tmp

        # training using unsupervised learning list
        print len(class_list)
        for path, file in ul:
            with open(path + "/" + file, 'r') as f:
                for line in f:
                    word = re.split(' |\@|\+|\*|_|/|\\|-|--|:|\.|,|\n|=|!|\t|<|>|"|;|\)|\(|\[|\]|\'|\$|\?|\#|\^|%|&', line)
                    word = [x for x in word if x]
                    for w in word:
                        for classification in class_list:
                            if classification in ld:
                                if w in ld[classification]:
                                    ld[classification][w] += 1
                                else:
                                    ld[classification][w] = 1
                            else:
                                tmp = {}
                                tmp[w] = 1
                                ld[classification] = tmp

        for classes in ld:
            for word in ld[classes]:
                print classes, word, ld[classes][word]


