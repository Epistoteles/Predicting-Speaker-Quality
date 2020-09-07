#!/bin/bash

file=$1
destination=$2

./lfbank.py $file > "$destination".lfbank

