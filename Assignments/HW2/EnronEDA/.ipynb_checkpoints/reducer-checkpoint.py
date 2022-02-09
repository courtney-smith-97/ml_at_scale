#!/usr/bin/env python
"""
Reducer takes words with their class and partial counts and computes totals.
INPUT:
    word \t class \t partialCount 
OUTPUT:
    word \t class \t totalCount  
"""
import re
import sys

# initialize trackers
current_word = None
spam_count, ham_count = 0,0

# read from standard input
for line in sys.stdin:
    # parse input
    word, is_spam, count = line.split('\t')
    
############ YOUR CODE HERE #########

    # tally counts from current key
    if word == current_word:
        if is_spam == '1':
            spam_count += int(count)
        else:
            ham_count += int(count)
    else:
        if current_word:
            if spam_count:
                print("%s\t%s\t%s" % (current_word, '1', spam_count))
            if ham_count:
                print("%s\t%s\t%s" % (current_word, '0', ham_count))
        #start a new tally 
        if is_spam == '1':
            current_word, spam_count = word, int(count)
            ham_count = 0
        else:
            current_word, ham_count = word, int(count)
            spam_count = 0
    
if spam_count:
    print(f'{current_word}\t{1}\t{spam_count}')
if ham_count:
    print(f'{current_word}\t{0}\t{ham_count}')



############ (END) YOUR CODE #########