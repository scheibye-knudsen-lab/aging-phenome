# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 11:55:05 2018

@author: soren
"""

### Pubmed Parser - Create list of pmid and abstracts ###

## Import packages ##

import pubmed_parser as pp
import os
import io

## Subdirectories ##

Sub_in = "Baseline"
Sub_out = "PMID with Abstracts"

try:
    os.mkdir(Sub_out)
except Exception:
    pass	
	
## Variables and lists ##

file_list = []
xml_dict = {}
Not_found_list = []
file_counter = 0

## Load list files ##

file_list = []
for file in os.listdir(Sub_in):
    if file.endswith(".gz"):
        file_list.append(file)

## Run through files and find the ones with abstracts ###
for file in file_list:
    file_counter += 1
    print("File Nummer: {} / {}".format(file_counter,len(file_list)))
    #parse xml file as dict
    if os.path.isfile(os.path.join(Sub_in,file)):
        xml_dict = pp.parse_medline_xml(os.path.join(Sub_in,file), year_info_only=False, nlm_category=False) # return list of dictionary
        #reset parameters
        pmid_abstract = {}
        #only get pmid with abstracts
        for entry in xml_dict:
            if entry['abstract'] and entry['pmid']:
                pmid_abstract[entry['pmid']] = entry['abstract'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        #write list to file
        with io.open(os.path.join(Sub_out,"{}.pmid_abstract.list.txt".format(file)),'w+',encoding="utf-8") as w:
            for pmid in pmid_abstract:
                w.write("{};{}\n".format(pmid,pmid_abstract[pmid]))
        w.close
    else:
        print("Could not find file: {}".format(file))
        Not_found_list.append(file)

## concatenate files ###

All_abstracts = "pmid_abstract.txt"

Abstract_file_list = []
for file in os.listdir(Sub_out):
    Abstract_file_list.append(file)

file_counter = 0

with open(os.path.join(Sub_out,All_abstracts), 'w+',encoding="utf-8") as outfile:
    for fname in Abstract_file_list:
        file_counter += 1
        print("Concatenated files: {} / {}".format(file_counter,len(Abstract_file_list)))
        with open(os.path.join(Sub_out,fname),'r',encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line)