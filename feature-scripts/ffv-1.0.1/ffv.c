/*
 * =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+====0
 
Copyright (c) 2009, Kornel Laskowski
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

	ffvCREATEDEFAULT() implementation.

 ===+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "windowpair.h"
#include "filterbank.h"
#include "dcorrxform.h"
#include "ffv.h"

static void ffvSPECTRUM
	(
		const double *  FL,
		const double *  FR,
		const int       Nfft,
		const int       NhPow2,
		const double    tsep,
		const double    tsepRef,
		double *        g,
		const int       Ng,
		const int *     mask
	);
 
/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * CONSTRUCTOR
 */

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
	)
{
	int            Tint;
	int            Text;
	int            Tsep;
	double *       hL;
	double *       hR;
	int            Nh;
	int            NhPow2;
	double *       fftL;
	double *       fftR;
	int            Nfft;
	FfvComputer *  ffvComputerPtr;
	double *       g;
	int *          gMask;
	double *       fbOutput;

	windowpairCREATE
		(
			tint,
			text,
			tsep,
			fs,
			winShape,
			&Tint,
			&Text,
			&Tsep,
			TsizePtr,
			&hL,
			&hR,
			&Nh,
			&NhPow2,
			&fftL,
			&fftR,
			&Nfft
		);

	ffvComputerPtr = (FfvComputer *) malloc( sizeof( FfvComputer ) );
	assert( ffvComputerPtr != (FfvComputer *) NULL );

	g = (double *)  malloc( Ng * sizeof( double ) );
	assert( g != (double *) NULL );

	gMask = (int *) malloc( Ng * sizeof( int ) );
	assert( gMask != (int *) NULL );

	filterbankGETMASK( fb, Nf, Ng, gMask );

	fbOutput = (double *) malloc( Nf * sizeof( double ) );
	assert( fbOutput != (double *) NULL );

	if ( *nOutputPtr == 0 )
	{
		*nOutputPtr = Nf;
	}
	else
	{
		assert( *nOutputPtr > 0 );
		assert( *nOutputPtr <= Nf );
	}

	ffvComputerPtr->tint = tint;
	ffvComputerPtr->text = text;
	ffvComputerPtr->tsep = tsep;
	ffvComputerPtr->fs = fs;
	ffvComputerPtr->winShape = winShape;
	ffvComputerPtr->Tint = Tint;
	ffvComputerPtr->Text = Text;
	ffvComputerPtr->Tsep = Tsep;
	ffvComputerPtr->hL = hL;
	ffvComputerPtr->hR = hR;
	ffvComputerPtr->Nh = Nh;
	ffvComputerPtr->NhPow2 = NhPow2;
	ffvComputerPtr->fftL = fftL;
	ffvComputerPtr->fftR = fftR;
	ffvComputerPtr->Nfft = Nfft;
	ffvComputerPtr->g = g;
	ffvComputerPtr->Ng = Ng;
	ffvComputerPtr->gMask = gMask;
	ffvComputerPtr->fb = fb;
	ffvComputerPtr->Nf = Nf;
	ffvComputerPtr->tsepRef = tsepRef;
	ffvComputerPtr->fbOutput = fbOutput;
	ffvComputerPtr->dCorrXFormType = dCorrXFormType;
	ffvComputerPtr->nOutput = *nOutputPtr;

	*ffvComputerPtrPtr = ffvComputerPtr;

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * CONSTRUCTOR using the ffv_main defaults
 *
 * the user must still look at nOutput and create its own output-array
 */

void ffvCREATEDEFAULT
	(
		int *                 TsizePtr,
		int *                 nOutputPtr,
		FfvComputer **        ffvComputerPtrPtr
	)
{
	Filter *            fb;
	int                 Nf;
	int                 Ng;
	double              tsepRef;
	filterbankCREATEDEFAULT( &Ng, &Nf, &tsepRef, &fb );
	*nOutputPtr = default_nOutput;
	ffvCREATE
		(
			default_tint,
			default_text,
			default_tsep,
			default_fs,
			default_winShape,
			fb,
			Nf,
			Ng,
			tsepRef,
			default_dCorrXFormType,
			TsizePtr,
			nOutputPtr,
			ffvComputerPtrPtr
		);
}


/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * DESTRUCTOR
 */

void ffvDESTROY
	(
		FfvComputer **  ffvComputerPtrPtr
	)
{
	windowpairDESTROY
		( 
			&((*ffvComputerPtrPtr)->hL),
			&((*ffvComputerPtrPtr)->hR),
			&((*ffvComputerPtrPtr)->fftL),
			&((*ffvComputerPtrPtr)->fftR)
		);

	free( (void *) (*ffvComputerPtrPtr)->g );
	free( (void *) (*ffvComputerPtrPtr)->gMask );

	filterbankDESTROY
		(
			(Filter **) (&((*ffvComputerPtrPtr)->fb)), 
			(*ffvComputerPtrPtr)->Nf
		);

	free( (void *) (*ffvComputerPtrPtr)->fbOutput );

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * COMPUTE THE FINAL PER-FRAME REPRESENTATION
 */

void ffvCOMPUTE
	(
		FfvComputer *             ffvComputerPtr,
		const signed short int *  audio,
		const int                 begIdx,
		const int                 nAudio,
		double *                  z
	)
{
	int       allZero;
	int       i;
	double *  g;
	int       Ng;
	int       Nf;
	double *  fbOutput;

	g = ffvComputerPtr->g;
	Ng = ffvComputerPtr->Ng;
	Nf = ffvComputerPtr->Nf;
	fbOutput = ffvComputerPtr->fbOutput;

	/*
	 * Check if all samples are zero (degenerate case).
	 */

	allZero = 1; 
	for ( i = 0; i < nAudio; i ++ )
	{
		if ( *(audio + begIdx + i) != 0 )
		{
			allZero *= 0;
			break;
		}
	}

	if ( allZero == 1 )
	{
		for ( i = 0; i < Ng; i ++ )
		{
			g[ i ] = 0.0;
		}
	}
	else
	{ 
		int       NhPow2;
		double *  fftL;
		double *  fftR;
		int       Nfft;

		NhPow2 = ffvComputerPtr->NhPow2;
		fftL = ffvComputerPtr->fftL;
		fftR = ffvComputerPtr->fftR;
		Nfft = ffvComputerPtr->Nfft;

		/*
		 * Window the frame (into two windows), and compute complex FFV.
		 */

		windowpairTWOFFT
			(
				audio + begIdx,
				nAudio,
				ffvComputerPtr->hL,
				ffvComputerPtr->hR,
				ffvComputerPtr->Nh,
				NhPow2,
				fftL,
				fftR,
				Nfft
			);
		ffvSPECTRUM
			(
				fftL,
				fftR,
				Nfft,
				NhPow2,
				ffvComputerPtr->tsep,
				ffvComputerPtr->tsepRef,
				g,
				Ng,
				ffvComputerPtr->gMask
			);
	}

	filterbankCOMPUTE
		(
			g,
			ffvComputerPtr->fb,
			Nf,
			fbOutput
		);
	dcorrxformCOMPUTE
		(
			fbOutput,
			Nf,
			ffvComputerPtr->dCorrXFormType,
			z,
			ffvComputerPtr->nOutput
		);

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * COMPUTE THE FFV SPECTRUM
 *
 * Recall that in the formulas, the range for discrete indices is [-N/2 + 1, +N/2]. That is
 * 1-offset notation. In 0-offset notation, that would be [-N/2, +N/2 - 1], or [-N/2, +N/2).
 *
 * NOTE: there is further scope for performance improvement (by a factor of approximately 2), by
 * limiting the computation to only the positive frequency half.
 */

static void ffvSPECTRUM
	(
		const double *  FL,         /* in NR/C FFT packed format */
		const double *  FR,         /* in NR/C FFT packed format */
		const int       Nfft,       /* number of doubles in each of FL and FR */
		const int       NhPow2,
		const double    tsep,
		const double    tsepRef,
		double *        g,
		const int       Ng,         /* number of doubles in g[] */
		const int *     mask	    /* which g[r] to compute, based on filterbank */
	)
{
	double  tsepRatio;  /* = tsep / tsepRef */
	int     r;          /* index over doubles in g[], i.e. the log of the dilation factor  */

	assert( tsepRef > 0.0 );
	tsepRatio = tsep / tsepRef;

	/*
	 * Zero g[].
	 */

	for ( r = 0; r < Ng; r ++ )
	{
		g[ r ] = 0.0;
	}

	/*
	 * Populate g[], iterating over index r.
	 */

	for ( r = -Ng/2; r < +Ng/2; r ++ )
	{
		int     r_plus_r;
		double  rho;
		int     k;
		double  product;
		double  normL;
		double  normR;

		/*
		 * Do not bother computing for g[r] values which are not used by
		 *  the filterbank.
		 */

		if ( mask[ r + Ng/2 ] == 0 )
		{
			continue;
		}

		/*
		 * Mapping of logarith of the dilation factor to the dilation factor
		 *  rho, in octaves.
		 */

		if ( r < 0  )
		{
			rho = pow( 2.0, ( 4.0*((double)(+r))/Ng ) * tsepRatio );
		}
		else
		{
			rho = pow( 2.0, ( 4.0*((double)(-r))/Ng ) * tsepRatio );
		}

		r_plus_r = r + r;

		/*
		 * Accumulate the (sum of) product and the quantities necessary for
		 *  cosine normalization.
		 */

		product = 0.0;
		normL = 0.0;
		normR = 0.0;

		for ( k = -NhPow2/2; k < NhPow2/2; k ++ )
		{
			double  sclK;      /* continuous frequency index for the dilated F */
			int     distSclK;  /* closest index for the dilated F, away from zero */
			int     proxSclK;  /* closest index for the dilated F, towards zero */
			double  proxCoeff; /* interpolation weight for the zero-proximate F magnitude */  
			double  distCoeff; /* interpolation weight for the zero-distant F magnitude */

			int     k_plus_k;
			int     proxSclK_plus_proxSclK;
			int     distSclK_plus_distSclK;

			double  myFLMag;
			double  myFRMag;

			sclK = rho * k;

			if ( sclK < 0 )
			{
				distSclK = (int) floor(sclK);
				proxSclK = (int) ceil(sclK);
			}
			else
			{
				distSclK = (int) ceil(sclK);
				proxSclK = (int) floor(sclK);
			}

			assert( fabs(distSclK) >= fabs(sclK) );
			assert( fabs(proxSclK) <= fabs(sclK) );

			proxCoeff = fabs(((double)distSclK) - sclK);
			distCoeff = 1.0 - proxCoeff;

			k_plus_k = k + k;
			proxSclK_plus_proxSclK = proxSclK + proxSclK;
			distSclK_plus_distSclK = distSclK + distSclK;

			if ( r < 0 )
			{
				double  myFLRe;
				double  myFLIm;
				double  myFRProxRe;
				double  myFRProxIm;
				double  myFRDistRe;
				double  myFRDistIm;

				if ( k < 0 )
				{
					myFLRe = FL[ k_plus_k     + Nfft ];
					myFLIm = FL[ k_plus_k + 1 + Nfft ];

					/*
					 * Must check also proxSclK_plus_proxSclK, because it is possible
					 *  for k to be (e.g.) -0.5, in which case proxSclK is 0.
					 */

					if ( proxSclK_plus_proxSclK < 0 )
					{
						myFRProxRe = FR[ proxSclK_plus_proxSclK     + Nfft ];
						myFRProxIm = FR[ proxSclK_plus_proxSclK + 1 + Nfft ];
					}
					else if ( proxSclK_plus_proxSclK == 0 )
					{
						myFRProxRe = FR[ 0 ];
						myFRProxIm = FR[ 1 ];
					}
					else
					{
						assert( 0 );
					}

					myFRDistRe = FR[ distSclK_plus_distSclK     + Nfft ];
					myFRDistIm = FR[ distSclK_plus_distSclK + 1 + Nfft ];
				}
				else
				{
					myFLRe = FL[ k_plus_k     ]; 
					myFLIm = FL[ k_plus_k + 1 ];

					myFRProxRe = FR[ proxSclK_plus_proxSclK     ];
					myFRProxIm = FR[ proxSclK_plus_proxSclK + 1 ];
					myFRDistRe = FR[ distSclK_plus_distSclK     ];
					myFRDistIm = FR[ distSclK_plus_distSclK + 1 ];
				}

				myFLMag = sqrt( myFLRe * myFLRe + myFLIm * myFLIm );
				myFRMag = proxCoeff * sqrt( myFRProxRe * myFRProxRe + myFRProxIm * myFRProxIm )
					+ distCoeff * sqrt( myFRDistRe * myFRDistRe + myFRDistIm * myFRDistIm );
			}
			else
			{
				double  myFLProxRe;
				double  myFLProxIm;
				double  myFLDistRe;
				double  myFLDistIm;
				double  myFRRe;
				double  myFRIm;

				if ( k < 0 )
				{
					/*
					 * Must check also proxSclK_plus_proxSclK, because it is possible
					 *  for k to be (e.g.) -0.5, in which case proxSclK is 0.
					 */

					if ( proxSclK_plus_proxSclK < 0 )
					{
						myFLProxRe = FL[ proxSclK_plus_proxSclK     + Nfft ];
						myFLProxIm = FL[ proxSclK_plus_proxSclK + 1 + Nfft ];
					}
					else if ( proxSclK_plus_proxSclK == 0 )
					{
						myFLProxRe = FL[ 0 ];
						myFLProxIm = FL[ 1 ];
					}
					else
					{
						assert( 0 );
					}

					myFLDistRe = FL[ distSclK_plus_distSclK     + Nfft ];
					myFLDistIm = FL[ distSclK_plus_distSclK + 1 + Nfft ];

					myFRRe = FR[ k_plus_k     + Nfft ];
					myFRIm = FR[ k_plus_k + 1 + Nfft ];
				}
				else
				{
					myFLProxRe = FL[ proxSclK_plus_proxSclK     ];
					myFLProxIm = FL[ proxSclK_plus_proxSclK + 1 ];
					myFLDistRe = FL[ distSclK_plus_distSclK     ];
					myFLDistIm = FL[ distSclK_plus_distSclK + 1 ];

					myFRRe = FR[ k_plus_k     ];
					myFRIm = FR[ k_plus_k + 1 ];
				}

				myFLMag = proxCoeff * sqrt( myFLProxRe * myFLProxRe + myFLProxIm * myFLProxIm )
					+ distCoeff * sqrt( myFLDistRe * myFLDistRe + myFLDistIm * myFLDistIm );
				myFRMag = sqrt( myFRRe * myFRRe + myFRIm * myFRIm );
			}

			product += (+myFLMag) * (+myFRMag);

			normL += myFLMag * myFLMag;
			normR += myFRMag * myFRMag;
		}

		g[ r + Ng/2 ] = product / sqrt( normL * normR );
	}

	return; 
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void ffvPRINT
	(
		const FfvComputer *  ffvComputerPtr
	)
{
	printf( "tint           : %.3g\n", ffvComputerPtr->tint );
	printf( "text           : %.3g\n", ffvComputerPtr->text );
	printf( "tsep           : %.3g\n", ffvComputerPtr->tsep );
	printf( "fs             : %g\n", ffvComputerPtr->fs );
	printf( "Tint           : %d\n", ffvComputerPtr->Tint );
	printf( "Text           : %d\n", ffvComputerPtr->Text );
	printf( "Tsep           : %d\n", ffvComputerPtr->Tsep );
	printf( "winShape       : %d\n", ffvComputerPtr->winShape );
	printf( "Nh             : %d\n", ffvComputerPtr->Nh );
	printf( "NhPow2         : %d\n", ffvComputerPtr->NhPow2 );
	printf( "Nfft           : %d\n", ffvComputerPtr->Nfft );
	printf( "Ng             : %d\n", ffvComputerPtr->Ng );
	printf( "Nf             : %d\n", ffvComputerPtr->Nf );
	printf( "tsepRef        : %.3g\n", ffvComputerPtr->tsepRef );
	printf( "dCorrXFormType : %d\n", ffvComputerPtr->dCorrXFormType );
	printf( "nOutput        : %d\n", ffvComputerPtr->nOutput );

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */


