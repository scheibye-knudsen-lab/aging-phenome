# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 18:33:45 2019

@author: soren
"""

### Selection of correct shared abstracts ###

## import packages ##

import os
import numpy as np

## Subdirectories ##

Sub_in = "PubMed Search/Aging terms found in abstracts"
Sub_in_2 = "PubMed Search/Aging synonyms found in abstracts"

Sub_out_main = "New terms mining"
Sub_out = "New terms mining/PMID shared Aging terms and Synonyms"

try:
    os.mkdir(Sub_out_main)
except Exception:
    pass

try:
    os.mkdir(Sub_out)
except Exception:
    pass

## Files ##

File1 = "Aging_terms_found_in_abstracts_SNOMED_extension.txt"
File2 = "Aging_synonyms_found_in_abstracts_SNOMED_extension.txt"

File_out = "Combined_Aging_terms_and_synonyms_PMID_list.txt"

## Variables ##

Aging_terms_two_plus = []
Aging_synonyms = []

#Get all pmid for aging terms with 2 or more terms
with open(os.path.join(Sub_in,File1), "r") as Aging_terms_file:
    next(Aging_terms_file)
    for line in Aging_terms_file:
        line = line.strip().split(';')
        #create a array to check if there is more than 1 term present in the abstract
        temp = np.array(line[1:],dtype=int)
        if np.sum(temp) >= 2:
            Aging_terms_two_plus.append(str(line[0]))
        else:
            pass
Aging_terms_file.close

#load all abstract with aging synonyms
with open(os.path.join(Sub_in_2,File2), "r") as Aging_synonyms_file:
    next(Aging_synonyms_file)
    for line in Aging_synonyms_file:
        line = line.strip().split(';')
        Aging_synonyms.append(str(line[0]))
Aging_synonyms_file.close

#Compare the lists and combined shared entries into a list

Combined_list = list(set(Aging_terms_two_plus) & set(Aging_synonyms))

with open(os.path.join(Sub_out,File_out), "w+") as Combined_list_file:
    for key in Combined_list:
        Combined_list_file.write("{}\n".format(key))
Combined_list_file.close
