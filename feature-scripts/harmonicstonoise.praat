#!/usr/bin/praat

step = 0.01
silenceThreshold = 0.05

form Parameters
	word inFile
	real minPitch 64.0
endform
Read from file... 'inFile$'
To Harmonicity (cc)... step 'minPitch' silenceThreshold 4.5
numberOfFrames = Get number of frames
for iframe to numberOfFrames
  hnr = Get value in frame... iframe
  if hnr = undefined
    hnr = -1
  endif
  printline 'hnr:4'
endfor
exit
