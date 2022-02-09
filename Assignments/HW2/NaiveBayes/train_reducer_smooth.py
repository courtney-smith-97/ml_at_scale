#!/usr/bin/env python
"""
Reducer aggregates word counts by class and emits frequencies.

INPUT:
    partitionKey \t word \t class0_partialCount,class1_partialCount
OUTPUT:
    word \t  
    
"""

import os
import sys                                                  
import numpy as np  

#################### YOUR CODE HERE ###################
vocab = int(sys.argv[1])

total_c1 = 0
total_c0 = 0
curr_word = None
curr_count_c1 = 0
curr_count_c0 = 0
# increment_val = 0
# curr_key = None

for line in sys.stdin:
    part, word, counts = line.lower().split('\t')
    
    #sys.stderr.write(f'reporter:counter:MyCounters,{part},{increment_val}\n')
    
    count_c0, count_c1 = counts.split(',')
    count_c0, count_c1 = int(count_c0), int(count_c1)
    
    #tally counts
    if word == curr_word:
        curr_count_c1 += int(count_c1)
        curr_count_c0 += int(count_c0)
    else:
        #order inversion to get total first
        if curr_word == '!total':
            total_c1 = float(curr_count_c1)
            total_c0 = float(curr_count_c0)
        #get class priors   
        if curr_word == 'classpriors':
            print(f'ClassPriors\t{curr_count_c0},{curr_count_c1},{curr_count_c0/(curr_count_c0+curr_count_c1)},{curr_count_c1/(curr_count_c0+curr_count_c1)}')
        #add 1 to numerator and vocab size to denominator to smooth, print, start new tally    
        if curr_word and curr_word!='!total' and curr_word!='classpriors':
            
            print(f'{curr_word}\t{curr_count_c0},{curr_count_c1},{(curr_count_c0+1)/(total_c0+vocab)},{(curr_count_c1+1)/(total_c1+vocab)}')
            
        curr_word, curr_count_c0, curr_count_c1 = word, int(count_c0), int(count_c1)
        
print(f'{curr_word}\t{curr_count_c0},{curr_count_c1},{(curr_count_c0+1)/(total_c0+vocab)},{(curr_count_c1+1)/(total_c1+vocab)}')



##################### (END) CODE HERE ####################