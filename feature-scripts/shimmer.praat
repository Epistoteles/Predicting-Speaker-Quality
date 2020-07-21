#!/usr/bin/praat

step = 0.01
windowSize = 0.15

form Parameters
  word inFile
  real minPitch 64.0
  real maxPitch 400
endform

Read from file... 'inFile$'
tmax = Get end time

To Pitch (cc)... 'step' 'minPitch' 15 true 0.03 0.45 0.01 0.35 0.14 'maxPitch'
selectObject: 1
plusObject: 2
To PointProcess (cc)
selectObject: 1
plusObject: 3
for i to (tmax-windowSize)/step
  frameStart = i * step
  frameEnd = i * step + windowSize
  shimmer = Get shimmer (apq5)... 'frameStart' 'frameEnd' 0.0001 0.02 1.3 1.6
  if shimmer = undefined
      shimmer = -1
   endif
  printline 'shimmer:4'
endfor
for i to windowSize/step - 1
  printline -1
endfor
