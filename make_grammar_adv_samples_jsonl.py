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


# Load data
parser = argparse.ArgumentParser(description='Directory with MultiNLI datasets')
parser.add_argument('--base_dir', dest='base_dir', help='Directory with MultiNLI datasets')
args = parser.parse_args()
base_dir = args.base_dir

dev_data = []
with jsonlines.open(os.path.join(base_dir,'multinli_1.0_dev_matched.jsonl')) as reader:
    for obj in reader:
        dev_data.append(obj)

# Replace words in samples
replaced_data = []
changed_lines = 0
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

print(changed_lines)
with jsonlines.open("./multinli_1.0_matched_dev_replaced.jsonl", mode='w') as writer:
    writer.write_all(replaced_data)
