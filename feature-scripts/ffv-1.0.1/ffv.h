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

10.08.2009 Timo Baumann

	Include default_ variables here, and ffvCREATEDEFAULT() signature.

 ===+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

#ifndef __FFV_H__
#define __FFV_H__

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

#include "windowpair.h"
#include "filterbank.h"
#include "dcorrxform.h"

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

static const double          default_tint            =  0.011;
static const double          default_text            =  0.009;
static const double          default_tsep            =  0.014;
static const double          default_fs              =  16000.0;
static const WinShape        default_winShape        =  WinShape_HAMMING_HANN;
static const DCorrXFormType  default_dCorrXFormType  =  DCorrXFormTypeNONE;
static const int             default_nOutput         =  0;
static const double          default_tfra            =  0.008;

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

typedef struct
{
	double          tint;
	double          text;
	double          tsep;
	double          fs;
	WinShape        winShape;
	int             Tint;
	int             Text;
	int             Tsep;
	double *        hL;
	double *        hR;
	int             Nh;
	int             NhPow2;
	double *        fftL;
	double *        fftR;
	int             Nfft;
	double *        g;
	int             Ng;
	int *           gMask;
	const Filter *  fb;
	int             Nf;
	double          tsepRef;
	double *	fbOutput;
	DCorrXFormType  dCorrXFormType;
        int             nOutput;
}
FfvComputer;

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void ffvCREATE
	(
		const double          tint,
		const double          text,
		const double          tsep,
		const double          fs,
		const WinShape        winShape,
		const Filter *        fb,
		const int             Nf,
		const int             Ng,
		const double          tsepRef,
		const DCorrXFormType  dCorrXFormType,
		int *                 TsizePtr,
		int *                 nOutputPtr,
		FfvComputer **        ffvComputerPtrPtr
	);

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void ffvCREATEDEFAULT
	(
		int *                 Tsize,
		int *                 nOutput,
		FfvComputer **        ffvComputerPtrPtr
	);

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void ffvDESTROY
	(
		FfvComputer **  ffvComputerPtrPtr
	);

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void ffvCOMPUTE
	(
		FfvComputer *             ffvComputerPtr,
		const signed short int *  audio,
		const int                 begIdx,
		const int                 nAudio,
		double *                  z
	);

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void ffvPRINT
	(   
		const FfvComputer *  ffvComputerPtr
	);

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

#endif /* __FFV_H__ */

