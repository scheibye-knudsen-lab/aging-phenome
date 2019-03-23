#!/bin/bash

## Subdirectory ##

Subdirectory="./Baseline"

## url ##

url="ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/*"

## Get Baseline ##

wget $url -P $Subdirectory