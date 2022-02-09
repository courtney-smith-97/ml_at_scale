#!/usr/bin/env python
"""
Mapper reads in text documents and emits word counts by class.
INPUT:                                                    
    DocID \t true_class \t subject \t body                
OUTPUT:                                                   
    partitionKey \t word \t class0_partialCount,class1_partialCount       
       
Partitioning:
    In order to send the totals to each reducer, we need to implement
    a custom partitioning strategy.
    
    We will generate a list of keys based on the number of reduce tasks 
    that we read in from the environment configuration of our job.
    
    We'll prepend the partition key by hashing the word and selecting the
    appropriate key from our list. This will end up partitioning our data
    as if we'd used the word as the partition key - that's how it worked
    for the single reducer implementation. This is not necessarily "good",
    as our data could be very skewed. However, in practice, for this
    exercise it works well. The next step would be to generate a file of
    partition split points based on the distribution as we've seen in 
    previous exercises.
    
    Now that we have a list of partition keys, we can send the totals to 
    each reducer by prepending each of the keys to each total.
       
"""

import re                                                   
import sys                                                  
import numpy as np      

from operator import itemgetter
import os

#################### YOUR CODE HERE ###################
#extract the number of reducers
if os.getenv('mapreduce_job_reduces') == None:
    n = 1
else:
    n = int(os.getenv('mapreduce_job_reduces'))
#n = 3 #num reducers -- change to env var
keys = list(map(chr, range(ord('A'), ord('Z')+1)))[:n]

#helper functions
def makeKeyHash(key, num_reducers):
    """
    Mimic the Hadoop string-hash function.
    
    key             the key that will be used for partitioning
    num_reducers    the number of reducers that will be configured
    """
    byteof = lambda char: int(format(ord(char), 'b'), 2)
    current_hash = 0
    for c in key:
        current_hash = (current_hash * 31 + byteof(c))
    return current_hash % num_reducers 

def getPartition(word):  
    a = makeKeyHash(word,n)
    return keys[int(a)]
    
#initialize counts
total_c1 = 0
total_c0 = 0
class_priors_c1 = 0
class_priors_c0 = 0

for line in sys.stdin:
    # parse input and tokenize
    docID, _class, subject, body = line.lower().split('\t')
    words = re.findall(r'[a-z]+', subject + ' ' + body)
    
    #get count of docs and words for each class
    if _class == '1':
        #add 1 to class doc count
        class_priors_c1 += 1
        for word in words:
            #increment class word count
            print(f'{getPartition(word)}\t{word}\t{0},{1}')
            total_c1 += 1
    else:
        class_priors_c0 += 1
        for word in words:
            print(f'{getPartition(word)}\t{word}\t{1},{0}')
            total_c0 += 1
    
for key in keys:            
    print(f'{key}\t!total\t{total_c0},{total_c1}')
    print(f'{key}\tClassPriors\t{class_priors_c0},{class_priors_c1}')

#################### (END) YOUR CODE ###################