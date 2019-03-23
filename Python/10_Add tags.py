# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 11:24:02 2018

@author: soren
"""

### Update abstract list with systemic tags ###

## Import Packages ##

import os

## Directories ##

Sub_in = "New terms mining/New word list"
Sub_in_2 = "New terms mining/SNOMED"

## files ##
file_in = "Word_list.txt"
file_out = "Word_list_tags_added.txt"

SNOMED_file = "SNOMED_ONLY.RRF"

## Variables ##

Snowmed_word_list = []
line_counter = 0

updated_word_list = {}

Minimum_count = 100 #set mimimum count to wanted mimimum of word occurrence

Semantic_tag = ['disorder', 'procedure', 'substance', 'finding', 'product', 'observable entity', 'situation', 'physical object', 'organism', 'occupation', 'assessment scale', 'event', 'attribute', 'navigational concept', 'body structure', 'physical force', 'qualifier value', 'regime/therapy', 'morphologic abnormality', 'environment', 'medicinal product', 'person', 'disposition', 'record artifact', 'religion/philosophy', 'clinical drug', 'medicinal product form', 'context-dependent category', 'clinical drug', 'specimen', 'combined site', 'cell structure', 'namespace concept', 'function', 'cell', 'geographic location', 'ethnic group', '& level', 'tumor staging', 'foundation metadata concept', 'dose form', 'biological function', 'isbt symbol', 'living organism']

## load files ##

# load the dictionary from snowmed_refs
print("Loads word list with tags.")
with open(os.path.join(Sub_in_2,SNOMED_file),'r',encoding="utf8") as r:
    for line in r:
        line_counter += 1
        if line_counter % 100000 == 0:
            print("{} out of 1392287".format(line_counter))
        line = line.strip().split('|')
        Snowmed_word_list.append(line[-5].lower())
r.close
print("Done loading word list.")

#remove redundant entries and remove Snomed_word_list from memory
Non_redundant_Snowmed_word_list = list(set(Snowmed_word_list))
Snowmed_word_list = 0

# Load feature lists
word_list = {}

with open(os.path.join(Sub_in,file_in), 'r') as R:
    for line in R:
        line = line.strip().split('\t')
        if int(line[1]) >= Minimum_count:
            word_list[line[0].lower()] = int(line[1])

#Just values for printing process
entry_counter = 0
percent_done = 0
number_of_divition = 1000
length_counter = int(len(Non_redundant_Snowmed_word_list)/number_of_divition)
print("Processing: Tag finder")

#Main script that runs through the snowmed_word_list and 
#finds the terms in it and see if a correct tag can be found to added to the feature list.
for entry in Non_redundant_Snowmed_word_list:
    entry_counter += 1
    if entry_counter % length_counter == 0:
        percent_done += 1
        print("Process: {}/{} %".format(percent_done,number_of_divition))
    #To optimize the speed, sorting out entries that ends with one of the 44 tags,
    #then run it through the feature list, and finally see if the correct feature+semetic-tag is found.
    for semantic in Semantic_tag:
        #The Feature should end if a "(semantic-tag)"
        if entry.endswith("({})".format(semantic)):
            for feature in word_list:
                #Feature should be the first word in the feature name.
                if entry.startswith("{}".format(feature)):
                    #if correct feature + tag is found add it to the updated_word_list
                    #so that it can be added to the fil later on.
                    if entry == "{} ({})".format(feature,semantic):
                        if feature in updated_word_list:
                            if "{}".format(semantic) not in updated_word_list[feature]:
                                updated_word_list[feature].append("{}".format(semantic))
                        else:
                            updated_word_list[feature] = ["{}".format(semantic)]
#Printing to file
with open(os.path.join(Sub_in,file_out),'w+') as out_file1:
    #Sorts the list based on the found number entry
    for key,value in sorted(word_list.items(),key=lambda i:i[1],reverse=True):
        #Needed two different approaches to handle no tag found
        if key in updated_word_list:
            out_file1.write("{}\t{}\t({})\n".format(key, value,";".join(map(str,updated_word_list[key]))))
        else:
            out_file1.write("{}\t{}\n".format(key, value))
out_file1.close