# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:53:56 2018

@author: soren
"""

### List Clenaer ###

## We want to clean for quantifier values and/or attribute (p,n,iii) ##
## We want to remove all values if "/" in them (g/ml,km/h)  ##
## Remove all words already in aging terms or synonyms ##

# Import packages #

import os

# Dictionaries #

Sub_in = "New terms mining/New word list"
Sub_in_1 = "Term lists"

# files ##

File1 = "Aging_terms_list_SNOMED_extension.txt"
File2 = "Aging synonyms.txt"

Word_file = "Word_list_tags_added.txt"

file_out = "Word_list_tags_cleaned.txt"

#Load the snomed extended feature list

Terms_list = []

with open(os.path.join(Sub_in_1,File1),'r') as Aging_terms:
    for line in Aging_terms:
        line = line.strip().split(';')
        for term in line:
            Terms_list.append(term.lower())
Aging_terms.close

with open(os.path.join(Sub_in_1,File2),'r') as Aging_synonyms:
    for line in Aging_synonyms:
        line = line.strip()
        Terms_list.append(line.lower())
Aging_synonyms.close

#Load file and remove above mentioned, then write to new file #

with open(os.path.join(Sub_in, file_out), 'w+') as Out:
    with open(os.path.join(Sub_in,Word_file),'r') as Read:
        for line in Read:
            temp1 = line.strip().split('\t')
            if "/" in temp1[0]: #removing units 
                pass
            elif temp1[0] in Terms_list:
                pass
            elif len(temp1) == 3:
                #check if unwanted semantic tags is present and remove term
                if (temp1[2] == "(qualifier value)" or
                    temp1[2] == "(attribute)" or
                    temp1[2] == "(attribute;qualifier value)" or
                    temp1[2] == "(qualifier value;attribute)" or
                    temp1[2] == "(procedure)" or
                    temp1[2] == "(body structure)" or
                    temp1[2] == "(organism)" or
                    temp1[2] == "(person)" or
                    temp1[2] == "(regime/therapy)" or
                    temp1[2] == "(ethnic group)" or
                    temp1[2] == "(environment)" or
                    temp1[2] == "(physical object)" or
                    temp1[2] == "(geographic location)" or
                    temp1[2] == "(qualifier value)" or "tumor staging" in temp1[2]):
                    pass
                else:
                    Out.write(line)
            else:
                Out.write(line)
    Read.close
Out.close