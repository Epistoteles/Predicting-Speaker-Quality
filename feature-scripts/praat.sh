for file in ../wavs/anonymized/random000.wav
do
	extra=`./pitchstats.pl -1 < "${file%%.wav}".pitch.esps | grep "stddev " | sed 's/^stddev *= //'`
	lower=`./pitchstats.pl -1 < "${file%%.wav}".pitch.esps | grep "5/95quant:" | sed -r 's"5/95quant: (.*)\t.*"\1"'`
	upper=`./pitchstats.pl -1 < "${file%%.wav}".pitch.esps | grep "5/95quant:" | sed 's/.*\t//'`
	lower=`echo $lower-$extra`
	upper=`echo $upper+$extra`
	./harmonicstonoise.praat $file $lower > "${file%%.wav}".hnr
	./jitter.praat $file $lower $upper > "${file%%.wav}".jitter
	./shimmer.praat $file $lower $upper > "${file%%.wav}".shimmer
done
