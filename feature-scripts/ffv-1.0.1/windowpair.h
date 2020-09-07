/*
 * =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+====0
 
Copyright (c) 2007-2009, Kornel Laskowski
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of
      conditions and the following disclaimer in the documentation and/or other materials provided
      with the distribution.
    * Neither the name of Carnegie Mellon University nor the names of its contributors may be used
      to endorse or promote products derived from this software without specific prior written
      permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 ===+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

#ifndef __WINDOWPAIR_H__
#define __WINDOWPAIR_H__

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

typedef enum
{
	WinShape_HAMMING_HAMMING = 0,
	WinShape_HANN_HANN,
	WinShape_HAMMING_HANN,
	nWinShape
}
WinShape;

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void windowpairCREATE
	(
		const double    tint,
		const double    text,
		const double    tsep,
		const double    fs, 
		const WinShape  winShape,
		int *           TintPtr,
		int *           TextPtr,
		int *           TsepPtr,
		int *           TsizePtr,
		double **       hLPtr,
		double **       hRPtr,
		int *           NhPtr,
		int *           NhPow2Ptr,
		double **       fftLPtr,
		double **       fftRPtr,
		int *           NfftPtr
	);  

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void windowpairDESTROY
	(
		double **  hLPtr,
		double **  hRPtr,
		double **  fftLPtr,
		double **  fftRPtr
	);

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void windowpairTWOFFT
	(
		const signed short int *  audio,
		const int                 nData,
		const double *            hL,    /* length Nh */
		const double *            hR,    /* length Nh */
		const int                 Nh,
		const int                 NhPow2,
		double *                  fftL,  /* length Nfft */
		double *                  fftR,  /* length Nfft */
		const int                 Nfft
	);

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

#endif /* __WINDOWPAIR_H__ */

