# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 09:05:52 2018

@author: soren
"""

### Find new terms in aging-related abstracts ###

## import packages ##

import os
import re

## Directories ##

Sub_in = "Term lists"
Sub_in_2 = Sub_in_2 = "New terms mining/PMID shared Clinical terms and Aging keywords"
Sub_in_3 = "PMID with Abstracts"

Sub_out_main = "New terms mining"
Sub_out = "New terms mining/Found SNOMED terms"

try:
    os.mkdir(Sub_out_main)
except Exception:
    pass
try:
    os.mkdir(Sub_out)
except Exception:
    pass

## Variables and lists ##

terms_list = []
pmid_list = []

Found_terms = {}
Abstracts = {}

## files ##

file1 = "SNOWMED_Terms_list_cleaned.txt"
file2 = "Combined_Clinical_terms_and_keywords_PMID_list.txt"
file3 = "pmid_abstract.txt"

## Load files ##
with open(os.path.join(Sub_in,file1), "r",encoding="utf8") as list_file:
    for line in list_file:
        line = line.strip()
        terms_list.append(line)
list_file.close

with open(os.path.join(Sub_in_2,file2), "r",encoding="utf8") as pmid_list_file:
    #skip header
    next(pmid_list_file)
    #create pmid list with found aging terms
    for line in pmid_list_file:
        line = line.strip().split(';')
        pmid_list.append(line[0])
pmid_list_file.close

with open(os.path.join(Sub_in_3,file3), "r",encoding="utf8") as pmid_file:
    for line in pmid_file:
        line = line.strip().split(';')
        if line[0] in pmid_list:
            Abstracts[line[0]]= line[1:]
        else:
            pass
pmid_file.close

#For the vast number of pmid and process time, it was decided to break the process into piece and saving to files on the go
Length = len(pmid_list)
step = 1000
Start = 0
Abstract_counter = Start

X=Start

PMID_with_features_found = {}
Printing_dict = {}

print("Loaded files and start mining.")
for X in range(Start,len(Abstracts),step):
    percent_counter = 0
    
    for pmid in list(Abstracts)[X:X+step]:
        # Reset variables
        Found_features = {}
        Abstract_counter += 1 
        # Run through list of features and count appearance in abstract
        print("pmid: {} / {} (saving to file each {} pmid)".format(Abstract_counter,len(Abstracts),step))
        #check if ";" is incorporated in an abstract and handle if present, else search abstracts for features
        if len(Abstracts[pmid]) > 1:
            for abstract_piece in Abstracts[pmid]:    
                for feature in terms_list:
                    if feature.lower() in abstract_piece.lower():
                        counts = len(re.findall(r'(?=\b{}\b)'.format(feature.lower()), Abstracts[pmid][0].lower()))
                        if counts > 0:
                            if feature not in Found_features:
                                Found_features[feature] = int(counts)
                            else:
                                Found_features[feature] += int(counts)
            if Found_features:
                PMID_with_features_found[pmid] = []
                for key in Found_features:
                    PMID_with_features_found[pmid].append("{};{}".format(key,Found_features[key]))
        else:
            for feature in terms_list:
                if feature.lower() in Abstracts[pmid][0].lower():
                    counts = len(re.findall(r'(?=\b{}\b)'.format(feature.lower()), Abstracts[pmid][0].lower()))
                    if counts > 0:
                        Found_features[feature] = int(counts)
            if Found_features:
                PMID_with_features_found[pmid] = []
                for key in Found_features:
                    PMID_with_features_found[pmid].append("{};{}".format(key,Found_features[key]))
    
    #Print segment to file
    print("Printing to file: step {} to {}".format(X,X+step))
    with open(os.path.join(Sub_out,"PMID_terms_found_{}_to_{}.txt".format(X,X+step)),'w+',encoding="utf8") as out_file:
        for key in PMID_with_features_found:
            out_file.write('{}\t{}\n'.format(key,'\t'.join(map(str,PMID_with_features_found[key]))))
    out_file.close
    
    #reseting file printing list
    PMID_with_features_found = {}
    Printing_dict = {}
