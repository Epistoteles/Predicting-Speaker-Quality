#!/bin/bash

file=$1
destination=$2

extra=`./pitchstats.pl -1 < "$destination".pitch.esps | grep "stddev " | sed 's/^stddev *= //'`
lower=`./pitchstats.pl -1 < "$destination".pitch.esps | grep "5/95quant:" | sed -r 's"5/95quant: (.*)\t.*"\1"'`
upper=`./pitchstats.pl -1 < "$destination".pitch.esps | grep "5/95quant:" | sed 's/.*\t//'`
lower=`echo $lower-$extra`
upper=`echo $upper+$extra`
./harmonicstonoise.praat "$file" $lower > "$destination".hnr
./jitter.praat "$file" $lower $upper > "$destination".jitter
./shimmer.praat "$file" $lower $upper > "$destination".shimmer