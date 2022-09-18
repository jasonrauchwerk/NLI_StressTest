from curses.ascii import isupper
import sys
import json
import jsonlines
import data_preprocessing as dp
import numpy as np
import math
import re
import random
import copy
import argparse

'''Types of perturbations: both character swaps and keyboard typos
Content words and function words'''

def tokenize(string):
    string = re.sub(r'\(|\)', '', string)
    return string.lower().split()

# Load data
parser = argparse.ArgumentParser(description='Directory with MultiNLI datasets')
parser.add_argument('--base_dir', dest='base_dir', help='Directory with MultiNLI datasets')
args = parser.parse_args()
base_dir = args.base_dir
dev_data = dp.load_nli_data(base_dir+"/multinli_0.9_dev_matched.jsonl")

# Load homophones from file
homophones_dict = {}
with open('homophones-1.01.txt', 'r') as f:
    for line in f:
        word,*homophones = line.split(',')
        homophones_dict[word.lower()] = homophones

# Replace words in samples
replaced_data = []
for sample in dev_data:
    sentence = tokenize(sample["sentence2_binary_parse"])
    
    possible_substitutions = []
    for i,word in sentence:
        l_word = word.lower()
        if l_word in homophones_dict:
            possible_substitutions.extend([(word,hom) for hom in homophones_dict[l_word]])

    if len(possible_substitutions) > 0:
        orig,sub = random.choice(possible_substitutions)
        # Keep capitalization
        if orig[0].isupper():
            sub = sub.capitalize()
        sample["sentence2_binary_parse"] = sample["sentence2_binary_parse"].replace(orig, sub, 1)
        sample["sentence2"] = sample["sentence2"].replace(orig, sub, 1)
        sample["sentence2_parse"] = sample["sentence2_parse"].replace(orig, sub, 1)

    replaced_data.append(sample)

print(len(replaced_data))
with jsonlines.open("./multinli_0.9_matched_dev_gram_functionword_swap_pertubed.jsonl", mode='w') as writer:
    writer.write_all(replaced_data)
    writer.close()

