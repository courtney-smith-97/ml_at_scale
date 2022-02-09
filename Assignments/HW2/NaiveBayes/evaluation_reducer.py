#!/usr/bin/env python
"""
Reducer to calculate precision and recall as part
of the inference phase of Naive Bayes.
INPUT:
    ID \t true_class \t P(ham|doc) \t P(spam|doc) \t predicted_class
OUTPUT:
    precision \t ##
    recall \t ##
    accuracy \t ##
    F-score \t ##

"""
import sys

# initialize counters
FP = 0.0 # false positives
FN = 0.0 # false negatives
TP = 0.0 # true positives
TN = 0.0 # true negatives

# read from STDIN
for line in sys.stdin:
    # parse input
    docID, class_, pHam, pSpam, pred = line.split()
    # emit classification results first
    print(line[:-2], class_ == pred)
    
    # then compute evaluation stats
#################### YOUR CODE HERE ###################
    if (class_ == '1') & (pred == '1'):
        TP += 1
    if (class_ == '0') & (pred == '0'):
        TN += 1
    if (class_ == '1') & (pred == '0'):
        FN += 1
    if (class_ == '0') & (pred == '1'):
        FP += 1

accuracy = (TP + TN)/(TP + TN + FP + FN)
precision = TP / (TP + FP)
recall = TP / (TP + FN)
if TP > 0:
    f1_score = 2*(recall * precision) / (recall + precision)
else:
    f1_score = 'Could not compute f1 score'

print(f'Num documents:{FP+FN+TP+TN}')
print(f'True positives:{TP}')
print(f'True negatives:{TN}')
print(f'False positives:{FP}')
print(f'False negatives:{FN}')
print(f'precision\t{precision}')
print(f'recall\t{recall}')
print(f'accuracy\t{accuracy}')
print(f'F-score\t{f1_score}')


#################### (END) YOUR CODE ###################
    