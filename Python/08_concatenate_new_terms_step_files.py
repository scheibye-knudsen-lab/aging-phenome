# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 19:15:39 2019

@author: soren
"""

### concatenate step files from new found terms ###

## import packages ##

import os

## Directories ##

Sub_in = "New terms mining/Found SNOMED terms/Test"

File_out = "concatenated_PMID_terms_found.txt"

#Variables

file_counter = 0
file_list = []

## Load list files ##

for file in os.listdir(Sub_in):
    if file.endswith(".txt"):
        file_list.append(file)

## concatenate the files ##

with open(os.path.join(Sub_in,File_out), 'w+') as output:
    for file in file_list:
        file_counter += 1
        print("File Nummer: {} / {}".format(file_counter,len(file_list)))
        if os.path.isfile(os.path.join(Sub_in,file)):
            with open(os.path.join(Sub_in,"{}".format(file)),'r',encoding="utf-8") as read:
                for line in read:
                    output.write(line)
            read.close
output.close