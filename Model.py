from collections import Counter
import operator
import math
from copy import deepcopy

class Model():
    def __init__(self):
        self.words_col = {}
        self.prior = {}
        self.likelyhood = {}
        self.cross_vlist = []
        
    def cost_of(self, prob):
        return math.log(1/prob)

    def clear_probs(self):
        self.words_col = {}
        self.prior = {}
        self.likelyhood = {}
    
    def calculate_probs(self,s_list):
        tot_sup_list = float(len(s_list))
        self.clear_probs()
        for sl in s_list:
            if sl[1] not in self.words_col:
                self.prior[sl[1]] = 1
                self.words_col[sl[1]] = Counter()
            tmp_lst = self.words_col[sl[1]]
            self.words_col[sl[1]] = tmp_lst+sl[0]
            self.prior[sl[1]]+= 1

        for topic in self.prior:
            self.prior[topic]/=tot_sup_list
            self.prior[topic] = self.cost_of(self.prior[topic])

        for topic in self.words_col.keys():
            length = float(len(list(self.words_col[topic].elements())))
            if topic not in self.likelyhood:
                self.likelyhood[topic] = {}
            for word in self.words_col[topic]:
                self.likelyhood[topic][word] = self.cost_of(self.words_col[topic][word]/length)
            self.likelyhood[topic]["missing"] = self.cost_of(0.1/length)
    
    def train(self,supervised_list,unsupervised_list):
        if len(unsupervised_list) > 0:
            self.calculate_probs(supervised_list)
            for i in range(3):
                self.cross_vlist = deepcopy(supervised_list)
                ul = deepcopy(unsupervised_list)
                self.cross_validate(ul)
                self.calculate_probs(self.cross_vlist)
        else:
            self.calculate_probs(supervised_list)

    def cross_validate(self,test_list):
        result = {}
        len_test = float(len(test_list))
        count = 0
        for doc in test_list:
            for topic in self.prior.keys():
                res = sum([self.likelyhood[topic][word] +self.prior[topic] if word in self.likelyhood[topic] else self.likelyhood[topic]["missing"]+self.prior[topic] for word in doc[0]])
                result[topic] = res
            prediction = min(result.iteritems(),key = operator.itemgetter(1))[0]
            self.cross_vlist.append((Counter(doc[0]),prediction))
            if prediction == doc[1]:
                count+=1
        print count/len_test

            
    def test(self,test_list):
        len_test = float(len(test_list))
        count = 0
        result = {}
        for doc in test_list:
            for topic in self.prior.keys():
                res = sum([self.likelyhood[topic][word] +self.prior[topic] if word in self.likelyhood[topic] else self.likelyhood[topic]["missing"]+self.prior[topic] for word in doc[0]])
                result[topic] = res
            if min(result.iteritems(),key = operator.itemgetter(1))[0] == doc[1]:
                count+=1
        print count/len_test


    def save(self, file_path):
        with open(file_path, "w") as fp:
            fp.write("Priors:" + str(len(self.prior)) + "\n")
            for prior, cost in self.prior.iteritems():
                fp.write(prior + ":" + str(cost) + "\n")
            for prior, word_costs in self.likelyhood.iteritems():
                for word, costs in word_costs.iteritems():
                    fp.write(prior + ":" + word + ":" + str(costs) + "\n")

    def load(self, file_path):
        with open(file_path, "r") as fp:
            content = [x.strip('\n') for x in fp.readlines()]
        current_counter = int(content.pop(0).split(":")[1])

        while current_counter > 0:
            current_counter -= 1
            next_row = content.pop(0)
            split_value = next_row.split(":")
            self.prior[split_value[0]] = float(split_value[1])
        for likelihoods in content:
            topic,word,cost = likelihoods.split(":")
            if topic not in self.likelyhood:
                self.likelyhood[topic] = {}
            self.likelyhood[topic][word] = float(cost)
 
