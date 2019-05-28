# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 16:11:34 2018

@author: soren
"""

### vector file to binary and z-score ###

#packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#from scipy.stats import zscore

# directories


Sub_in = "PubMed Search/Aging terms found in abstracts"

Sub_out = "Frequency analysis"

#Create folders if they do not exist

try:
    os.mkdir(Sub_out)
except Exception:
    pass

vector_file_in = "Aging_features_found_in_Abstract_categorical.txt"


#get bar char variables

File_line_counter = 0
percentage = 0
PMID_file_length = 3198219

with open(os.path.join(Sub_in,vector_file_in),'r') as read_in:
    #variables
    header_flag = 0
    #file handle
    for line in read_in:
        line = line.strip().split(';')
        #Printing progress
        File_line_counter += 1
        if File_line_counter % int(PMID_file_length/100) == 0:
            percentage += 1
            print("Progress: {} / 100 %".format(percentage))
        #get header
        if header_flag == 0:
            header = line[1:]
            header_flag = 1
            #create count vectors
            count_one_vector = np.zeros(len(header), dtype=int)
            count_two_plus_vector = np.zeros(len(header), dtype=int)
            one_counter = 0
            two_counter = 0
        else:
            Number_vector = np.array(line[1:],dtype=int)
            if np.sum(Number_vector) >= 1:
                count_one_vector = np.add(count_one_vector,Number_vector)
                one_counter += 1
            if np.sum(Number_vector) >= 2:
                count_two_plus_vector = np.add(count_two_plus_vector,Number_vector)
                two_counter += 1
read_in.close

#If data set is too small to account for no features found
#count_one_vector[count_one_vector == 0] = 1
#count_two_plus_vector[count_two_plus_vector == 0] = 1
print(one_counter,two_counter)

difference = (count_one_vector/count_two_plus_vector)
#fold_increase = 
Round_difference = difference.astype(int)

with open(os.path.join(Sub_out,"Bar_chart_variables.txt"),'w+') as Bar_char_out:
    Bar_char_out.write("Terms;{}\n".format(";".join(header)))
    Bar_char_out.write("Total Count;{}\n".format(";".join(map(str,count_one_vector))))
    Bar_char_out.write("Co-occurrence count;{}\n".format(";".join(map(str,count_two_plus_vector))))
    Bar_char_out.write("Co-occurrence/Total count*100 (percentage);{}\n".format(";".join(map(str,Round_difference))))
Bar_char_out.close

print(np.std(difference))
print(np.mean(difference))