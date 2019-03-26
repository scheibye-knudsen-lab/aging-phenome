# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 16:19:15 2019

@author: soren
"""

### percentage matrix ###

import os
import numpy as np

## directories and files ##

sub_dir1 = "Hallmarks of Aging analysis/Hallmark matrices"
sub_dir2 = "Term lists"

file1 = "9Hallmarks_Sum_matrix.txt"
file2 = "Hallmark_Percentage_matrix.csv"
file3 = "Hallmarks_with_synonyms.txt"

Sub_out = "Hallmarks of Aging analysis/Hallmark matrices"

#rounding error correction function
def round_to_100_percent(number_set, digit_after_decimal=2):
    """
        This function take a list of number and return a list of percentage, which represents the portion of each number in sum of all numbers
        Moreover, those percentages are adding up to 100%!!!
        Notice: the algorithm we are using here is 'Largest Remainder'
    """
    unround_numbers = [x / float(sum(number_set)) * 100 * 10 ** digit_after_decimal for x in number_set]
    decimal_part_with_index = sorted([(index, unround_numbers[index] % 1) for index in range(len(unround_numbers))], key=lambda y: y[1], reverse=True)
    remainder = 100 * 10 ** digit_after_decimal - sum([int(x) for x in unround_numbers])
    index = 0
    while remainder > 0:
        unround_numbers[decimal_part_with_index[index][0]] += 1
        remainder -= 1
        index = (index + 1) % len(number_set)
    return [int(x) / float(10 ** digit_after_decimal) for x in unround_numbers]

#Variables

flag = 0

sum_matrix = {}
Hallmarks = []
Header = []

#import files

with open(os.path.join(sub_dir1,file1), 'r') as read:
    for line in read:
        if flag == 0:
            line = line.strip().split(';')
            for key in line[1:]:
                Header.append(key.capitalize())
            flag = 1
        else:
            line = line.strip().split(';')
            if np.sum(np.array(line[1:],dtype=int)) == 0:
                pass
            else:
                sum_matrix[line[0]] = np.array(line[1:],dtype=int)
read.close

with open(os.path.join(sub_dir2,file3), 'r') as read2:
    for line in read2:
        line = line.strip().split(";")
        Hallmarks.append(line[0].capitalize())
read.close


Sum_vector = np.zeros(9,dtype=int)

for key in sum_matrix:
    Sum_vector = np.sum([Sum_vector,sum_matrix[key]],axis=0)

#Normalizing Matrix based on occurrence frequency

Normalized_matrix = {}
for key in sum_matrix:
    Normalized_matrix[key] = {}
    for item in range(0,len(sum_matrix[key]),1):
        if sum_matrix[key][item] == 0:
            Normalized_matrix[key][Hallmarks[item]] = int(0)
        else:
            Nomalized_value = sum_matrix[key][item]/Sum_vector[item]
            Normalized_matrix[key][Hallmarks[item]] = Nomalized_value

#Percentage matrix
percentage_matrix = {}
rounded_Matrix = {}
for key in Normalized_matrix:
    temp_sum = 0
    percentage_matrix[key] = {}
    percentage_sum = 0
    for item in Normalized_matrix[key]:
        if Normalized_matrix[key][item] == 0:
            pass
        else:
            temp_sum = temp_sum+Normalized_matrix[key][item]
    for item in Normalized_matrix[key]:
        if Normalized_matrix[key][item] == 0:
            percentage_matrix[key][item] = 0
        else:
            percentage_matrix[key][item] = Normalized_matrix[key][item]/temp_sum*100
            percentage_sum = percentage_sum+percentage_matrix[key][item]    

    #Rounding percentage to get 100 %
    Rounded_Percentage_Matrix = {}
    for key in percentage_matrix:
        rounded_Matrix[key] = []
        Rounded_Percentage_Matrix[key] = {}
        for item in percentage_matrix[key]:
            rounded_Matrix[key].append(percentage_matrix[key][item])
        rounded = round_to_100_percent(rounded_Matrix[key])
        n = 0
        for item in percentage_matrix[key]:
            Rounded_Percentage_Matrix[key][item] = rounded[n]
            n += 1

printing_string = []
for n in range(1,len(Header)+1,1):
    printing_string.append("Hallmark {}".format(n))
with open(os.path.join(sub_dir1,file2),'w+') as outfile:
    outfile.write("Terms;{}\n".format(";Percentage;".join(printing_string)))
    for key in Rounded_Percentage_Matrix:
        outfile.write("{}".format(key))
        for item in sorted(Rounded_Percentage_Matrix[key].items(), key=lambda kv: kv[1], reverse=True):
            outfile.write(";{};{}".format(item[0],item[1]))
        outfile.write("\n")
outfile.close
