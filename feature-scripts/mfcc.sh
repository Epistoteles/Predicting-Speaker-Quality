#!/bin/bash

file=$1
destination=$2

./compute-mfcc/compute-mfcc --input "$file" --output "$destination".mfc
