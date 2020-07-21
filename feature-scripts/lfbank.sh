for file in ../wavs/anonymized/random000.wav
do
	./lfbank.py $file > "${file%%.wav}".lfbank
done
