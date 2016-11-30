import sys
import re
import math
import ModelNotEmptyException
sys.setrecursionlimit(9999)


class Model:
    prior = None
    ld = None

    def __init__(self):
        self.prior = {}
        self.ld = {}

    def train(self, sl, ul, class_list):

        # training using the supervised learning list
        for file, classification in sl:
            if classification in self.prior:
                self.prior[classification] += 1
            else:
                self.prior[classification] = 1
            for word_list in file:
                for w in word_list:
                    if classification in self.ld:
                        if w in self.ld[classification]:
                            self.ld[classification][w] += 1
                        else:
                            self.ld[classification][w] = 1
                    else:
                        tmp = {}
                        tmp[w] = 1
                        self.ld[classification] = tmp

        # Convert counts of the prior table to probability
        sum = 0.0
        for keys in self.prior:
            sum += self.prior[keys]
        for keys in self.prior:
            self.prior[keys] = math.log(1 / (self.prior[keys] / float(sum)))

        # Convert counts of the likelihood table to probability
        sum_dict = {}
        for classification in self.ld:
            for word in self.ld[classification]:
                if word not in sum_dict:
                    sum_dict[word] = self.ld[classification][word]
                else:
                    sum_dict[word] += self.ld[classification][word]
        for classification in self.ld:
            for word in self.ld[classification]:
                self.ld[classification][word] = math.log(1 / (self.ld[classification][word] / float(sum_dict[word])))

        # training using unsupervised learning list
        # print len(class_list)
        # for path, file in ul:
        #     with open(path + "/" + file, 'r') as f:
        #         for line in f:
        #             word = re.split(' |\@|\+|\*|_|/|\\|-|--|:|\.|,|\n|=|!|\t|<|>|"|;|\)|\(|\[|\]|\'|\$|\?|\#|\^|%|&', line)
        #             word = [x for x in word if x]
        #             for w in word:
        #                 for classification in class_list:
        #                     if classification in ld:
        #                         if w in ld[classification]:
        #                             ld[classification][w] += 1
        #                         else:
        #                             ld[classification][w] = 1
        #                     else:
        #                         tmp = {}
        #                         tmp[w] = 1
        #                         ld[classification] = tmp

        # for classes in ld:
        #     for word in ld[classes]:
        #         print classes, word, ld[classes][word]

    def save(self, file_path):
        with open(file_path, "w") as fp:
            fp.write("Priors:" + str(len(self.prior)) + "\n")
            for prior, count in self.prior.iteritems():
                fp.write(prior + ":" + str(count) + "\n")
            fp.write("LL:\n")
            for prior, word_counts in self.ld.iteritems():
                for word, count in word_counts.iteritems():
                    fp.write(prior + ":" + word + ":" + str(count) + "\n")

    def test(self,):

        pass

    def load(self, file_path):
        with open(file_path, "r") as fp:
            content = [x.strip('\n') for x in fp.readlines()]
        while True:
            next_row = content.pop(0)
            if "LL" in next_row:
                break
            split_value = next_row.split(":")
            self.prior[split_value[0]] = float(split_value[1])
        print content[0]
        for likelihoods in content:
            split_value = likelihoods.split(":")
            word = split_value[1]
            for index in range(2, len(split_value) - 1):
                print split_value[index]
                word += ":" + split_value[index]
            if split_value[0] in self.ld:
                self.ld[split_value[0]][word] = float(split_value[len(split_value) - 1])
            else:
                tmp = {}
                tmp[word] = float(split_value[len(split_value) - 1])
                self.ld[split_value[0]] = tmp

        print self.ld

