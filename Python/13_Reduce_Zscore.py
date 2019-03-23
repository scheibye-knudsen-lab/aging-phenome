# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 11:15:37 2019

@author: soren
"""

### New zsore file ###

# import packages #

import os
import pandas as pd

# Dictionaries #

Sub_in = "Word embeddings matrix"
Sub_in_1 = "Term lists"

# files #

terms_file = 'Final_list_105_terms.txt'
file_out = "Zscore_105_terms.csv"
Zscore_file = "Zscore_matrix.csv"

# Variables #

Terms_list = []
Lower_case_list = []

#read and get feature list
with open(os.path.join(Sub_in_1,terms_file),'r') as read:
    for line in read:
        line = line.strip()
        Terms_list.append(line)
        Lower_case_list.append(line.lower())
read.close

#load data
data = pd.read_csv(os.path.join(Sub_in,Zscore_file),sep=";",encoding = 'cp1252')
print("data loaded")

data.columns = data.columns.str.lower()
print("data is lowercase")

data_reduced = data[data.columns.intersection(Lower_case_list)]
print("Data is reduced")
print("Number of columns: {}".format(len(data_reduced.columns)))

for key in data_reduced.columns:
    data_reduced = data_reduced.rename(index=str, columns={"{}".format(key): "{}".format(Terms_list[Lower_case_list.index(key)])})
    
print("Correctly renamed coloums")

data_reduced_round = data_reduced.round(decimals=6)

data_reduced_round.to_csv(os.path.join(Sub_in,file_out),sep=";",encoding='utf-8', index=False)

print("Data saved")