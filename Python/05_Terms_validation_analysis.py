# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 16:52:58 2018

@author: soren
"""

### Random Feature Analysis version 4 ###

import os
import random
import numpy as np
from scipy.stats import chisquare

## Subdirectories ##

Sub_in = "PubMed Search/Aging terms found in abstracts"
Sub_in_2 = "PubMed Search/Aging synonyms found in abstracts"
Sub_in_3 = "PMID with Abstracts"

Sub_out_main = "Validation of the aging terms"
Sub_out = "Validation of the aging terms\Random Terms Found"
Sub_out_2 = "Validation of the aging terms\Random pmid lists"
Sub_out_3 = "Validation of the aging terms\Evaluation table"

#Create folders if they do not exist

try:
    os.mkdir(Sub_out_main)
except Exception:
    pass

try:
    os.mkdir(Sub_out)
except Exception:
    pass

try:
    os.mkdir(Sub_out_2)
except Exception:
    pass

try:
    os.mkdir(Sub_out_3)
except Exception:
    pass

## Files ##

Aging_terms_found_vector_file = "Aging_terms_found_in_abstracts_SNOMED_extension.txt"
Aging_synonyms_found = "Aging_synonyms_found_in_abstracts_SNOMED_extension.txt"

PMID_file = "pmid_abstract.txt"
File_out_concatenated = "All_samples_feature_found.txt"
Evaluation_table = "Evaluation_table.txt"

### sample number and random features number ###

sample = 100
Random_pmid_number = 0
Aging_synonyms_pmid = []
#Get number of pmids of aging synonyms
with open(os.path.join(Sub_in_2,Aging_synonyms_found), "r") as pmid_file:
    #skip header
    next(pmid_file)
    for line in pmid_file:
        line = line.strip().split(";")
        Aging_synonyms_pmid.append(line[0])
        Random_pmid_number += 1
pmid_file.close

## Variables ##

pmid_list = []

Feature_found_vector = {}

Random_PMID_Found_feature = {}

#Get length of pmid list and vector file

pmid_list_length = 0

vector_line_file_length = 0

with open(os.path.join(Sub_in_3,PMID_file), "r",encoding="utf8") as PMID_LIST:
    for line in PMID_LIST:
        pmid_list_length += 1
PMID_LIST.close

with open(os.path.join(Sub_in,Aging_terms_found_vector_file), "r") as Vector_file:
    #skip header
    next(Vector_file)
    for line in Vector_file:
        vector_line_file_length += 1
Vector_file.close

#load feature vector list

Header_flag = 0
with open(os.path.join(Sub_in,Aging_terms_found_vector_file), "r") as Vector_file:
    #reset progress
    File_line_counter = 0
    percentage = 0
    #Handle input
    for line in Vector_file:
        line = line.strip().split(';')
        #Get header - else process lines
        if Header_flag == 0:
            Feature_header = line[1:]
            Header_flag = 1
        else:
            #Print progress
            if File_line_counter % int(vector_line_file_length/100) == 0:
                percentage += 1
                print("Loading vector file: {} / 100 %".format(percentage))
            #Write pmid with array of feature found
            Feature_found_vector[line[0]] = np.array(line[1:],dtype=int)
            File_line_counter += 1
    print("Done!")
Vector_file.close
print("Vector file loaded.")

# load pmid list from file
with open(os.path.join(Sub_in_3,PMID_file), "r",encoding="utf8") as PMID_LIST:
    #reset progress
    File_line_counter = 0
    percentage = 0
    #handle file
    for line in PMID_LIST:
        line = line.strip().split(";")
        pmid_list.append(line[0])
        #Printing progress
        File_line_counter += 1
        if File_line_counter % int(pmid_list_length/100) == 0:
            percentage += 1
            print("Loading pmid list: {} / 100 %".format(percentage))
    print("Done!")
PMID_LIST.close
print("PMID List loaded.")

### OUTER LOOP for "sample number" iterations ###

with open(os.path.join(Sub_out,File_out_concatenated),'w+') as outfile_concatenated:
    for X in range(1,sample+1,1):
        
        print("Processing - sample {}".format(X))
        ## Set outfile ##
        
        File_out = "Sample_{}_Random_features_found_in_Abstract.txt".format(X)
        Random_pmid_list_file = "Random_pmid_list_sample_{}.txt".format(X)
        ## Create random feature list ##
        
        Random_pmid_list = random.sample(pmid_list, Random_pmid_number)
        
        #reset progres parameters  
        File_line_counter = 0
        percentage = 0
        All_feature_found = np.zeros(len(Feature_header),dtype=int)
        
        #print random pmid list to file
        with open(os.path.join(Sub_out_2,Random_pmid_list_file), 'w+',encoding="utf-8") as Random_pmid_list_outfile:
            for pmid in Random_pmid_list:
                Random_pmid_list_outfile.write("{}\n".format(pmid))
        Random_pmid_list_outfile.close
        
        #write to outfile while processing big write
        with open(os.path.join(Sub_out,File_out),'w+') as outfile:
            #run through random list and write lines that are in 
            for key in Random_pmid_list:
                #Printing progress
                File_line_counter += 1
                if File_line_counter % int(Random_pmid_number/100) == 0:
                    percentage += 1
                    print("sample {} - {} / 100 %".format(X,percentage))
                if key in Feature_found_vector.keys():
                    outfile.write("{};{}\n".format(key,";".join(map(str,Feature_found_vector[key]))))
                    All_feature_found = np.add(All_feature_found,Feature_found_vector[key])    
                else:
                    pass
            #write the accumulated amount to file
            outfile_concatenated.write("sample_{};{}\n".format(X,";".join(map(str,All_feature_found))))
            print("Done!")
        outfile.close
outfile_concatenated.close

#Write table with sum of aging terms in synonyms abstracts, plus average sum of aging terms in the X sample number, with fold increase and average fold increase.

Random_sum = np.zeros(len(Feature_header),dtype=int)

with open(os.path.join(Sub_out,File_out_concatenated),'r') as outfile_concatenated:
    for line in outfile_concatenated:
        line = line.strip().split(";")
        vector = np.array(line[1:],dtype=int)
        Random_sum = np.add(Random_sum,vector)
outfile_concatenated.close

Random_average_sum = np.divide(Random_sum,sample)

#get sum of terms in synonym abstracts
Term_sum = np.zeros(len(Feature_header),dtype=int)
for key in Aging_synonyms_pmid:
    if key in Feature_found_vector:
        Term_sum = np.add(Term_sum,Feature_found_vector[key])

#Handle if a term in term_sum and/or Random_average_sum is zero (this was only a case in the example run)
Term_sum = np.where(Term_sum==0, 1, Term_sum)
Random_average_sum = np.where(Random_average_sum==0, 1, Random_average_sum)

#calculate fold increase and average fold increase
Fold_increase = np.divide(Term_sum,Random_average_sum)

Fold_increase = np.round(Fold_increase, decimals=2)

Average_fold_increase = np.mean(Fold_increase)

chisq_test = chisquare(Term_sum,f_exp=Random_average_sum)

#write table to file
with open(os.path.join(Sub_out_3,Evaluation_table),'w+') as out_file:
    out_file.write("{}\n".format("\t".join(Feature_header)))
    out_file.write("{}\n".format("\t".join(map(str,Term_sum))))
    out_file.write("{}\n".format("\t".join(map(str,Random_average_sum))))
    out_file.write("{}\n".format("\t".join(map(str,Fold_increase))))
    out_file.write("Average fold Increase: {}\n".format(Average_fold_increase))
    out_file.write("chisq_test (p-value): {}\n".format(chisq_test[1]))
out_file.close
