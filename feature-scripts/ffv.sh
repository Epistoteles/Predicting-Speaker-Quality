#!/bin/bash

file=$1
destination=$2

./ffv-1.0.1/ffv --fs 16000 --tfra 0.01 $file "$destination".ffv