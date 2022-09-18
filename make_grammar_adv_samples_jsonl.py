from curses.ascii import isupper
import sys
import json
import jsonlines
#import data_preprocessing as dp
#import numpy as np
import math
import re
import random
import copy
import argparse
import os

'''Types of perturbations: both character swaps and keyboard typos
Content words and function words'''

def tokenize(string):
    string = re.sub(r'\(|\)', '', string)
    return string.lower().split()


random.seed(12345)

# Load data
parser = argparse.ArgumentParser(description='Directory with MultiNLI datasets')
parser.add_argument('--base_dir', dest='base_dir', help='Directory with MultiNLI datasets')
args = parser.parse_args()
base_dir = args.base_dir

dev_data = []
with jsonlines.open(os.path.join(base_dir,'multinli_1.0_dev_matched.jsonl')) as reader:
    for obj in reader:
        dev_data.append(obj)

# Load homophones from file
replacement_dict = {}
with open('homophones-1.01.txt', 'r') as f:
    for line in f:
        word,*homophones = line.rstrip().split(',')
        replacement_dict[word.lower()] = homophones

# Replace words in samples
replaced_data = []
for sample in dev_data:
    sentence = tokenize(sample["sentence2_binary_parse"])
    
    possible_substitutions = []
    for word in sentence:
        l_word = word.lower()
        if l_word in replacement_dict:
            possible_substitutions.extend([(word,hom) for hom in replacement_dict[l_word]])

    # substitute if possible
    if len(possible_substitutions) > 0:
        orig,sub = random.choice(possible_substitutions)
        # Keep capitalization
        if orig[0].isupper():
            sub = sub.capitalize()
        sample["sentence2"] = re.sub(rf'{orig}(?=\W|$)', sub, sample["sentence2"], count=1)
        sample["sentence2_parse"] = re.sub(rf'{orig}(?=\W|$)', sub, sample["sentence2_parse"], count=1)
        sample["sentence2_binary_parse"] = re.sub(rf'{orig}(?=\W|$)', sub, sample["sentence2_binary_parse"], count=1)

    replaced_data.append(sample)

print(len(replaced_data))
with jsonlines.open("./multinli_1.0_matched_dev_homophones.jsonl", mode='w') as writer:
    writer.write_all(replaced_data)
