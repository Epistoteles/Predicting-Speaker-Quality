for file in ../wavs/anonymized/random000.wav
do
  ./ffv-1.0.1/ffv --fs 16000 --tfra 0.01 $file ${file%.wav}.ffv
done
