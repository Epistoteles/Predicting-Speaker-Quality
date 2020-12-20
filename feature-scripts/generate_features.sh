#!/bin/bash

rsync -a --include '*/' --exclude '*' "./wavs/" "./feature-streams/"  # update shallow directory structure

files_total=$(find ../wavs/ -type f | wc -l)

function generate_features () {  # generate feature files given a wav path as argument
  file=$1
  destination_stump=$2

  bash pitch.sh "$file" "$destination_stump" > /dev/null 2>&1
  mv "${file%%.wav}".pitch.esps "$destination_stump".pitch.esps > /dev/null 2>&1
  bash ffv.sh "$file" "$destination_stump" > /dev/null 2>&1
  bash mfcc.sh "$file" "$destination_stump" > /dev/null 2>&1
  bash lfbank.sh "$file" "$destination_stump" > /dev/null 2>&1
  bash praat.sh "$file" "$destination_stump" > /dev/null 2>&1
}

existing=0
created=0
deleted=0
counter=0

for file in $(find ../wavs/ -type f)
do
  counter=$((counter+1))
  destination=$(echo $file | sed "s/wavs/feature-streams/g")
  destination_stump=${destination%%.wav}
  if [ ! -f "$destination_stump.shimmer" ] # if (last) feature file has not yet been generated
  then
    echo "($counter/$files_total) Generating features for $file"
    created=$((created+1))
    generate_features $file $destination_stump
  else
    existing=$((existing+1))
    echo "($counter/$files_total) Already generated features for $file"
  fi
done

echo "Did not change $existing existing feature streams, created $created new feature streams, deleted $deleted old feature streams."