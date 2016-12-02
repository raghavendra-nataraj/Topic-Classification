import sys
import pprint
import math
import operator
import ModelNotEmptyException
from copy import deepcopy

sys.setrecursionlimit(9999)


class Model:
    prior_counts = None
    ld_counts = None
    prior_costs = None
    ld_costs = None
    us_prior_counts = None
    us_ld_counts = None
    class_word_counts = None

    def __init__(self):
        self.prior_counts = {}
        self.ld_counts = {}
        self.prior_costs = {}
        self.old_priorlist = {}
        self.ld_costs = {}
        self.us_prior_counts = {}
        self.old_us_prior = {}
        self.us_ld_counts = {}
        self.class_word_counts = {}

    def __str__(self):
        ret_string = ""
        ret_string += "Top 10 words associated with spam (with strength of association):\n"
        ret_string += pprint.pformat(str(self.prior_counts)) + "\n"
        ret_string += pprint.pformat(str(self.prior_costs)) + "\n"
        ret_string += pprint.pformat(str(self.us_prior_counts)) + "\n"
        ret_string += pprint.pformat(str(self.class_word_counts)) + "\n"
        return ret_string

    def checkCountSame(self):
        result=True
        for key in self.us_prior_counts.keys():
            if key not in self.old_us_prior:
                result = False
                break
            if (self.old_us_prior[key] - self.us_prior_counts[key])>10:
                result = False
                break
        return result
    
    def train(self, sl, ul, class_list):
        # training using the supervised learning list

        self.calculate_sl_counts(sl)
        self.calculate_probabilties(use_unsupervised=False)
        train_counter = 0
        if len(ul) > 0:
            while (train_counter < 20):
                train_counter += 1
                ul_with_class = []
                self.old_us_prior = deepcopy(self.us_prior_counts)
                for document, topic in ul:
                    predicted_class = self.test(document, class_list)
                    ul_with_class.append((document, predicted_class))

                self.calculate_ul_counts(ul_with_class)
                self.calculate_probabilties(use_unsupervised=True)
                print "lopper"
                if self.checkCountSame():
                    break

    def calculate_sl_counts(self, sl_list):
        for word_list, topic in sl_list:
            if topic in self.prior_counts:
                self.prior_counts[topic] += 1
            else:
                self.prior_counts[topic] = 1
            for w in word_list:
                if topic in self.ld_counts:
                    if w in self.ld_counts[topic]:
                        self.ld_counts[topic][w] += 1
                    else:
                        self.ld_counts[topic][w] = 1
                else:
                    self.ld_counts[topic] = {}
                    self.ld_counts[topic][w] = 1

    def calculate_ul_counts(self, ul_list):
        self.us_prior_counts = {}
        self.us_ld_counts = {}
        for word_list, classification in ul_list:
            if classification in self.us_prior_counts:
                self.us_prior_counts[classification] += 1
            else:
                self.us_prior_counts[classification] = 1
            for w in word_list:
                if classification in self.us_ld_counts:
                    if w in self.us_ld_counts[classification]:
                        self.us_ld_counts[classification][w] += 1
                    else:
                        self.us_ld_counts[classification][w] = 1
                else:
                    self.us_ld_counts[classification] = {}
                    self.us_ld_counts[classification][w] = 1

    def calculate_probabilties(self, use_unsupervised=False):
        # Convert counts of the prior table to probability
        sums = 0.0
        for keys in self.prior_counts:
            sums += self.prior_counts[keys]
            if use_unsupervised == True:
                if keys in self.us_prior_counts:
                    sums += self.us_prior_counts[keys]

        for keys in self.prior_counts:
            numerator = float(self.prior_counts[keys])
            if use_unsupervised == True:
                if keys in self.us_prior_counts:
                    numerator += float(self.us_prior_counts[keys])
            tmp = numerator / float(sums)
            if tmp == 1.0:
                tmp = .99
            self.prior_costs[keys] = math.log(1 / tmp)

        # Convert counts of the likelihood table to probability
        for prior, word_counts in self.ld_counts.iteritems():
            # for i in word_counts.itervalues():
            #     current_count+= i
            current_count = sum([i for i in word_counts.itervalues()])
            if use_unsupervised == True:
                if prior in self.us_ld_counts:
                    current_count += sum(self.us_ld_counts[prior].itervalues())
            for word, count in word_counts.iteritems():
                numerator = count
                if use_unsupervised == True:
                    if prior in self.us_ld_counts:
                        curr_cost = math.log(1 / (0.1 / self.class_word_counts[prior]))
                        if word in self.us_ld_counts[prior]:
                            curr_cost = self.us_ld_counts[prior][word]
                        numerator += curr_cost
                curr_prob = (1.0 * numerator) / current_count
                if prior not in self.ld_costs:
                    self.ld_costs[prior] = {}
                self.ld_costs[prior][word] = math.log(1 / curr_prob)

        for prior, count in self.prior_counts.iteritems():
            current_count = sum(self.ld_counts[prior].itervalues()) + 0.1
            if use_unsupervised == True:
                if prior in self.us_ld_counts:
                    current_count += sum(self.us_ld_counts[prior].itervalues())
            if prior not in self.class_word_counts:
                self.class_word_counts[prior] = {}
            self.class_word_counts[prior] = current_count

    def save(self, file_path):
        with open(file_path, "w") as fp:
            fp.write("Priors:" + str(len(self.prior_costs)) + "\n")
            for prior, count in self.prior_costs.iteritems():
                fp.write(prior + ":" + str(count) + "\n")
            fp.write("LL Counts:" + str(len(self.prior_costs)) + "\n")
            for prior, count in self.class_word_counts.iteritems():
                fp.write(prior + ":" + str(self.class_word_counts[prior]) + "\n")
            fp.write("LL:\n")
            for prior, word_counts in self.ld_costs.iteritems():
                for word, count in word_counts.iteritems():
                    fp.write(prior + ":" + word + ":" + str(count) + "\n")

    def test(self, text, class_list):
        result_dict = {}
        for classes in class_list:
            cost = 0
            for word in text:
                curr_cost = math.log(1 / (0.1 / self.class_word_counts[classes]))

                if word in self.ld_costs[classes]:
                    curr_cost = self.ld_costs[classes][word]
                cost += curr_cost

            result_dict[classes] = cost # + self.prior_costs[classes]
        return min(result_dict.iteritems(), key=operator.itemgetter(1))[0]

    def load(self, file_path):
        with open(file_path, "r") as fp:
            content = [x.strip('\n') for x in fp.readlines()]
        current_counter = int(content.pop(0).split(":")[1])

        while current_counter > 0:
            current_counter -= 1
            next_row = content.pop(0)
            split_value = next_row.split(":")
            self.prior_costs[split_value[0]] = float(split_value[1])
        current_counter = int(content.pop(0).split(":")[1])
        while (current_counter > 0):
            current_counter -= 1
            next_row = content.pop(0)
            split_value = next_row.split(":")
            self.class_word_counts[split_value[0]] = float(split_value[1])

        for likelihoods in content:
            split_value = likelihoods.split(":")
            word = split_value[1]
            for index in range(2, len(split_value) - 1):
                # print split_value[index]
                word += ":" + split_value[index]
            if split_value[len(split_value) - 1] == "":
                split_value[len(split_value) - 1] = 0
            if split_value[0] in self.ld_costs:
                self.ld_costs[split_value[0]][word] = float(split_value[len(split_value) - 1])
            else:
                tmp = {}
                tmp[word] = (float(split_value[len(split_value) - 1])) / 1.0
                self.ld_costs[split_value[0]] = tmp
