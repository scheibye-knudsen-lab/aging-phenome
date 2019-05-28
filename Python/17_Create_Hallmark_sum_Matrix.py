# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:04:01 2019

@author: soren
"""

### Create Sum Matrix ###

## import ##

import os
import numpy as np

## directories and files ##

sub_dir1 = "Hallmarks of Aging analysis"

file1 = "Hallmark_features_found_in_Abstracts.txt"
file2 = "105_terms_found_in_Hallmark_Abstracts.txt"
file3 = "9Hallmarks_Sum_matrix.txt"

Sub_out = "Hallmarks of Aging analysis/Hallmark matrices"

try:
    os.mkdir(Sub_out)
except Exception:
    pass

## Variables ##


#header handle
Hallmark_Header = []
Terms_Header = []
Flag_header_hallmark = 1
Flag_header_terms = 1

#matrices
Hallmark_dict = {}
Terms_dict = {}

## load files ##
# Hallmarks #
with open(os.path.join(sub_dir1,file1),'r') as read:
    for line in read:
        line = line.strip().split(';')
        #create header
        if Flag_header_hallmark == 1:
            Hallmark_Header = line[1:]
            Flag_header_hallmark = 0
        #create matrix
        else:
            Hallmark_dict[line[0]] = np.array(line[1:],dtype=int)
read.close
print("loaded hallmarks.")

# 105 aging terms #
with open(os.path.join(sub_dir1,file2),'r') as read:
    for line in read:
        line = line.strip().split(';')
        #create header
        if Flag_header_terms == 1:
            Terms_Header = line[1:]
            Flag_header_terms = 0
        #create matrix
        else:
            Terms_dict[line[0]] = np.array(line[1:],dtype=int)
read.close
print("loaded 105 terms.")

#Initialize sum matrix
Summary_matrix = {}
for key in Terms_Header:
    Summary_matrix[key] = np.zeros(len(Hallmark_Header),dtype=int)

#add to summary_matrix

Terms_dict_length = len(Terms_dict)
pmid_counter = 0
percentage = 0

for pmid in Terms_dict:
    #Printing progress
    pmid_counter += 1
    if pmid_counter % int(Terms_dict_length/100) == 0:
        percentage += 1
        print("Summary_Matrix: {} / 100 %".format(percentage))
    #go through all terms and see if they are present
    for x in range(0,len(Terms_dict[pmid]),1):
        if int(Terms_dict[pmid][x]) > 0:
            #add hallmarks to summary_matrix if present
            Summary_matrix[Terms_Header[x]] = np.add(Summary_matrix[Terms_Header[x]],Hallmark_dict[pmid])
print("Have created the Summary matrix.")

#save summary matrix to file
with open(os.path.join(Sub_out,file3),'w+') as sum_mat:
    sum_mat.write("Terms;{}\n".format(";".join(Hallmark_Header)))
    for term in Summary_matrix:
        sum_mat.write("{};{}\n".format(term,";".join(map(str,Summary_matrix[term]))))
sum_mat.close
print("Saved Summary matrix to file.")
