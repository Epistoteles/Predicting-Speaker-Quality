# This script will split the .wav audio files of the Spoken Wikipedia Corpus 2.0
# into sub-samples of a user-defined length and organize them by reader and title.
# The corpus is avaliable under https://nats.gitlab.io/swc/
# Execute this script in the same directory as the main SWC '<language>' directory with 'bash split.sh [-d 30] [-v] [-s]'

function log () {
    if [[ "$verbosity" -eq 1 ]]; then
        echo "$@"
    fi
}

function split_audio () {
	if [[ $(ls "$1"*.ogg | grep -v "audio.ogg" | wc -l) -gt 0 ]] && [ ! -f "$1"audio.ogg ]; then # Some recordings are split up into audio1.ogg, audio2.ogg, ...
    echo "   🔗 Concatenating recordings"
    for f in $1*.ogg; do
      sox $f $f channels 1
    done
    sox $(ls "$1"*.ogg) "$1"audio.ogg
  else
    if [[ $(ls "$1"*.ogg | wc -l) -eq 0 ]]; then # Some dirs are empty :(
      echo "   ❌ Empty directory $1 found"
      emptydirs+="   $1\n"
      return
    fi
	fi
	reader=$(grep -Po '(?<="reader":")([^",]*)(?=")' "$1"info.json | head -1 | tr -dc "[:alnum:]" | tr '[:upper:]' '[:lower:]')
  if [ -z "$reader" ]; then # Some recordings don't have a reader specified
    echo "   🗣️ No reader specified in info.json. Skipping article."
    noreaders+="   $1\n"
    return
  fi
	log "Reader: $reader"
  title=$(grep -Po '(?<="title":")([^",]*)(?=")' "$1"info.json | head -1 | tr -dc "[:alnum:]" | tr '[:upper:]' '[:lower:]')
	log "Title: $title"
  if [ -d wavs/split-"$split_duration"/"$reader"/"$title" ]; then # Don't generate already split audio again
    echo "   ✅ Already generated $title"
    return
  fi
	duration=$(sox --i -D "$1"audio.ogg)
	log "Duration: $duration s"
	num_files=$((${duration%.*} / $split_duration))
  num_files=$([[ $num_files -lt $maxgen ]] && echo "$num_files" || echo "$maxgen")
	log "Splitting audio into $num_files files"
	mkdir -p wavs/split-$split_duration/"$reader"/"$title"
	for i in $(seq 1 $num_files); do
    start=$((($i - 1) * $split_duration))
    end=$(($i * $split_duration))
		log "    Generating $i.wav from second $start to $end"
		sox -v 0.95 "$1"audio.ogg wavs/split-"$split_duration"/"$reader"/"$title"/"$i".wav trim $start "$split_duration" channels 1 rate 16000
	done
  echo "   ✔️ Split up $title by $reader"
}

: ${split_duration:=30}
: ${verbosity:=0}
: ${progress:=0}
: ${maxgen:=1000}
emptydirs=""
noreaders=""

while getopts "hvpd:m:" opt; do
  case ${opt} in
    h )
      echo "Usage:"
      echo "    -h            Display this help message."
      echo "    -v            Execute script with verbose output."
      echo "    -p            Display progress during execution."
      echo "    -m 3          Maximum amount of generated .wav files per article."
      echo "    -d 30         Split audio into files of specified duration in seconds. Default: 30s."
      exit 0
      ;;
    v )
	verbosity+=1
      ;;
    p )
	progress+=1
      ;;
    d )
  split_duration=$OPTARG
      ;;
      m )
  maxgen=$OPTARG
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      ;;
  esac
done

echo "Target audio file length is $split_duration seconds."
echo "Maximum amount of generated .wav files per article is $maxgen."
echo -e "Clipping warnings may occur.\n"
sleep 2
articles=$(ls german/ | wc -l)
counter=0
for d in german/*/; do
    ((counter++))
    if [[ "$progress" -eq 1 ]]; then
      echo -e "Processing dir $counter/$articles ($d)"
    fi
    split_audio $d
done
echo ""
echo -e "❌ Found the following empty directories:\n$emptydirs"
echo -e "🗣️ Found the following articles without readers:\n$noreaders"
echo -e "🦄 Done :)\n"
