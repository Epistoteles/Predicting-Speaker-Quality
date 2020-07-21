for file in ../wavs/anonymized/random000.wav
do
  ./compute-mfcc/compute-mfcc --input "$file" --output "${file%%.wav}".mfc
done
