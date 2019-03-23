# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 08:28:52 2018

@author: soren
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 13:27:40 2018

@author: soren
"""
### New Features ###

## Importing relevant packages ##

import os

## Sub directories ##

Sub_in = "New terms mining/Found SNOMED terms/Test"

Sub_out_main = "New terms mining"
Sub_out = "New terms mining/New word list"

try:
    os.mkdir(Sub_out_main)
except Exception:
    pass
try:
    os.mkdir(Sub_out)
except Exception:
    pass
## Files ##

concatenated_PMID_terms_found = "concatenated_PMID_terms_found.txt"
file_out = "Word_list.txt"

## variables ##

Word_list = {}
Total_line_count = 0

#Progress Variables
line_count = 0
percent_count = 0

## get line count ##
with open(os.path.join(Sub_in,concatenated_PMID_terms_found), "r") as list_file:
    for line in list_file:
        Total_line_count += 1
list_file.close


## Load files ##

with open(os.path.join(Sub_in,concatenated_PMID_terms_found),'r') as file1:
    for line in file1:
        #progress writer
        line_count += 1
        if line_count % int(Total_line_count/100) == 0:
            percent_count += 1
            print("Progress: {}/100 %".format(percent_count))
        #main script
        line = line.strip().split('\t')
        for feature_and_count in line[1:]:
            feature_and_count = feature_and_count.split(';')
            feature = feature_and_count[0].lower()
            count = int(feature_and_count[1])
            if feature in Word_list:
                Word_list[feature] += count
            else:
                Word_list[feature] = count
file1.close

## write word list ##

with open(os.path.join(Sub_out,file_out),'w+') as output:
    for key,value in sorted(Word_list.items(),key=lambda i:i[1],reverse=True):
        output.write("{}\t{}\n".format(key, value))
output.close
