import argparse
import itertools
import os
import random
import re
from curses.ascii import isupper

import jsonlines

'''Types of perturbations: both character swaps and keyboard typos
Content words and function words'''

def tokenize(string):
    string = re.sub(r'\(|\)', '', string)
    return string.lower().split()


def replace_samples(dev_data, replacement_dict):
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
            changed_lines += 1

            replaced_data.append(sample)

    return replaced_data


random.seed(12345)

# Load homophones from file
homophone_dict = {}
with open('homophones-1.01.txt', 'r') as f:
    for line in f:
        word,*homophones = line.rstrip().split(',')
        homophone_dict[word.lower()] = homophones

# Load misspellings from file
misspell_dict = {}
with open('missp.dat', 'r') as f:
    prev_word = None
    missp_list = []
    for line in f:
        word = line.rstrip()
        if word[0] == '$':
            misspell_dict[prev_word] = missp_list
            prev_word = word[1:].lower()
            missp_list = []
        else:
            missp_list.append(word.replace('_', ' '))
    del misspell_dict[None]

# Combine dicts
replacement_dict = {}
for key in itertools.chain(homophone_dict.keys(), misspell_dict.keys()):
    replacement_dict[key] = homophone_dict.get(key,[]) + misspell_dict.get(key, [])


# Matched dataset
dev_data = []
with jsonlines.open('../data/multinli_1.0_dev_matched.jsonl', mode='r') as reader:
    for obj in reader:
        dev_data.append(obj)

with jsonlines.open("../data/multinli_1.0_dev_matched_replaced.jsonl", mode='w') as writer:
    writer.write_all(replace_samples(dev_data, replacement_dict))

# Mismatched dataset
dev_data = []
with jsonlines.open('../data/multinli_1.0_dev_mismatched.jsonl', mode='r') as reader:
    for obj in reader:
        dev_data.append(obj)

with jsonlines.open("../data/multinli_1.0_dev_mismatched_replaced.jsonl", mode='w') as writer:
    writer.write_all(replace_samples(dev_data, replacement_dict))

# Training dataset
dev_data = []
with jsonlines.open('../data/multinli_1.0_train.jsonl', mode='r') as reader:
    for obj in reader:
        dev_data.append(obj)

with jsonlines.open("../data/multinli_1.0_train.jsonl", mode='w') as writer:
    writer.write_all(replace_samples(dev_data, replacement_dict))