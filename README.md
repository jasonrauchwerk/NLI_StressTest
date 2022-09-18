# NLI_StressTest

[Stress testing](https://en.wikipedia.org/wiki/Stress_testing) is a methodology where systems are tested in order to confirm that intended specifications are being met and identify weaknesses.

For Natural Language Inference, our stress tests are large-scale automatically constructed suites of datasets which evaluate systems on a phenomenon-by-phenomenon basis. Each evaluation set focuses on a single phenomenon so as to not introduce confounding factors, thereby providing a testbed for fine-grained evaluation and analysis.

Stress tests for word overlap, negation, length mismatch, antonym, noise and numerical reasoning stress tests as described in the paper [[1]](https://arxiv.org/abs/1806.00692) can directly be downloaded  [here](https://drive.google.com/file/d/1faGA5pHdu5Co8rFhnXn-6jbBYC2R1dhw/view). You can also find other resources related to this work on our [website](https://abhilasharavichander.github.io/NLI_StressTest/). 

This repository contains the code used to automatically generate stress tests for word overlap, negation, length mismatch, antonym, spelling error and numerical reasoning, intended to help generate stress tests for _new_ data. To evaluate your models, please use the generated [stress tests](https://abhilasharavichander.github.io/NLI_StressTest/). 

## Competence Tests
1. gen_num_test.py, quant_ner.py: These files are used to perform the preprocessing steps (such as splitting word problems into sentences, removing sentences with long rationales and removing sentences which do not contain named entities) and create a set of useful premise sentences for the quantitative reasoning stress test
2. quant_example_gen.py: This file uses the set of useful premise sentences generated after preprocessing to create entailed, contradictory and neutral hypotheses for the quantitative reasoning stress test
3. make_antonym_adv_samples.py: This file contains the code to sample sentences from the MultiNLI development set as possible premises and generate contradicting hypotheses.

### How to Run

Numerical Reasoning:
1. Run python gen_num_test.py INPUT_FILE OUTPUT_FILE
2. Run python quant_ner.py
3. Run python quant_example_gen.py

Antonyms
1. Run python make_antonym_adv_samples.py --base_dir MULTINLI_DIRECTORY

## Distraction Tests
1. make_distraction_adv_samples_jsonl.py: This file generates the word overlap, negation and length mismatch tests

### How to Run

How to run the code:
1. Run python make_distraction_adv_samples_jsonl.py TAUTOLOGY_STRING INPUT_FILE OUTPUT_FILE ( this file needs the data_preprocessing.py file provided by MultiNLI creators to run)


## Noise Tests
1. make_grammar_adv_samples_jsonl.py : Noise test, file generates premise-hypothesis pairs with a word perturbed by a keyboard swap spelling error.

### How to Run
1. Run python make_grammar_adv_samples_jsonl.py --base_dir MULTINLI_DIRECTORY 

The generated stress tests are also available at: https://abhilasharavichander.github.io/NLI_StressTest/

## Evaluation Script
If you want to directly evaluate your system on all stress tests at once you can. 
 Usage is as follows-
1. You will need to report your predictions on the test file found [here](https://drive.google.com/file/d/1Gw3YgA63rFMqAEpzDtO0PKFJ3WsHPQ5d/view?usp=sharing)
2. Write out model predictions as "prediction" field for each sample in the evaluation set. (Sample submission files are available as [sample_submission.jsonl](https://drive.google.com/file/d/18r2lb0sU_YmOZ1mRjHdtyFhsfADD4Qje/view?usp=sharing) and [sample_submission.txt](https://drive.google.com/file/d/14MbtSB-G6RZ87hJNX9AS3I5cVSfz7PDh/view?usp=sharing))
3. Run the [evaluation script](https://github.com/AbhilashaRavichander/NLI_StressTest/blob/master/eval.py) with the command
	python eval.py --eval_file SUBMISSION_FILE > REPORT_FILE.txt

Alternatively, you may write your own evaluation function: our script simply evaluates models on classification accuracy for each stress test at once.

## Changes by Jason

* Added the homophones dataset from [CMU Artificial Intelligence Repository](https://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/speech/database/homofonz/0.html). Removed the beginning of the txt file so only a list of words remains.

HOMOPHONES

This is a list of homophones in "General American English". It is based on 
the book _Handbook of Homophones_ by William Cameron Townsend, 1975. 
For the purpose at hand, the list contains words that sound the same (or 
very nearly the same) but are spelled differently. Thus the list includes 
"bear" and "bare" but not "bear" (noun) and "bear" (verb). However, the list 
does occasionally include spelling variants of the same word when there 
is another word in the same entry; for instance, "ax,axe,acts" is in the list 
but not "blessed,blest".(Note that the only difference between 
"homophones" and "spelling variant" is whether or not the words are 
lexically "the same".)

Obviously, the determination of what counts as sounding the "same" 
depends on the dialect of the speaker. Some of the entries in this list may 
be homophones in my speech but not yours (for instance, "awed" and "odd". 
The designation "General American English" should be sufficient to 
disallow strong regional dialects (in the south, "tire" and "tar" can be 
homophones!) while allowing for some minor variation. For instance, there
are entries for "cot,caught" and "marry,merry,Mary".

The list contains a few proper names, which are capitalized; e.g. "Pete" 
and "peat". I think this is useful as long as proper names are limited to 
common ones. (Proper names that differ only in case from common nouns
are not included, e.g. "bill,"Bill".) If any and all proper names were fair 
game, I fear we would be off and running (how about "Malays" and 
"malaise"?). But I am open to advice.

The format of the list is as follows. Each set of homophones is on a single  
line terminated by a return. The members of a set are separated by 
commas with no trailing spaces. (Thus it is essentially the same as 
"comma-delimited" database format.) The list is alphabetized by the first 
word (the headword) in each set (line). Each word in the list occurs as a 
headword; thus each word occurs at least twice: once as a headword and at 
least once in the tail of the list. This scheme permits retrieval from the 
list by examining the headword of each line only. For instance:

ascent,assent

assent,ascent

In general, regularly inflected forms of an entry are not included; thus the
list contains "bough,bow" but not "boughs,bows". Do you think it is worth
adding such entries?

Version history

10-May-93  Released first version based on Townsend 1975.
11-May-93 Added entries derived from the 1964 Websters Pocket 
                   Dictionary by Lee Hetherington of MIT.
14-May-93 Added entries suggested by various reviewers and entries 
                  derived from the Moby Pronounced dictionary by Lee 
                  Hetherington of MIT.
17-May-93 Added more entries, deleted a few.

Fair use policy

Please use this list as the common property of the general academic 
community. You may redistribute the list in its original form (or at least 
its "official" form), but you should not sell it or use it in a commercial 
product without permission. If you use it in a research project or 
publication, please give due credit. You may freely modify it for your own 
use, but if you distribute a modified version, you should make clear what 
changes you have made to the original list. Above all, if you make 
enhancements to the list, please send such enhancements to us so that we 
can pass them along to the rest of the users of the list. All 
correspondence regarding this list should be sent to:

Evan Antworth
Summer Institute of Linguistics
7500 W. Camp Wisdom Road
Dallas, TX  75236
U.S.A.

Internet email evan.antworth@sil.org
phone 214/709-3346, -2418
fax 214/709-2433


## References

Please considering citing [[1]](https://arxiv.org/abs/1806.00692) if using these stress tests to evaluate Natural Language Inference models.

### Stress Test Evaluation for Natural Language Inference (COLING 2018)

[1] A. Naik, A. Ravichander, N. Sadeh, C. Rose, G.Neubig, [*Stress Test Evaluation for Natural Language Inference*](https://arxiv.org/abs/1806.00692)

```
@inproceedings{naik18coling, 
title = {Stress Test Evaluation for Natural Language Inference},
author = {Aakanksha Naik and Abhilasha Ravichander and Norman Sadeh and Carolyn Rose and Graham Neubig}, 
booktitle = {The 27th International Conference on Computational Linguistics (COLING)}, 
address = {Santa Fe, New Mexico, USA},
month = {August},
year = {2018} }
