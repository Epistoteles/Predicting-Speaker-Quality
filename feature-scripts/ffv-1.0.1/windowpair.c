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

#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include "mutils.h"
#include "windowpair.h"

#define PI 3.14159265359
#define DOPREEMPHASIS

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * CONSTRUCTOR
 */

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
	)
{
	int       Tint;
	int       Text;
	int       Tsep;
	int       Nh;
	int       NhPow2;
	double    bint;
	double    mint;
	double    bext;
	double    mext;
	double *  hL;
	double *  hR;
	int       TsepHalf;
	int       i;
	int       Nfft;
	double *  fftL;
	double *  fftR;

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Compute window-size parameters in number of samples.
	 */

	Tint = (int) ( tint * fs );
	if ( ( ( tint * fs ) - (double) Tint ) > 0.5 )
	{
		Tint ++;
	}
	assert( Tint > 0 );

	Text = (int) ( text * fs );
	if ( ( ( text * fs ) - (double) Text ) > 0.5 )
	{
		Text ++;
	}
	assert( Text > 0 );

	Tsep = (int) ( tsep * fs );
	if ( ( ( tsep * fs ) - (double) Tsep ) > 0.5 )
	{
		Tsep ++;
	}
	assert( Tsep > 0 );
	assert( ( Tsep % 2 ) == 0 ); 

	assert( Tint <= (Tsep + Text) ); /* can't remember why */

	Nh = Text + Tsep + Text;

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Assign window-shape curve-parameters based on winShape.
	 */

        switch( winShape )
        {
        case WinShape_HAMMING_HAMMING:
                bint = 0.54;
                mint = 0.46;
                bext = 0.54;
                mext = 0.46;
                break;

        case WinShape_HANN_HANN:
                bint = 0.5;
                mint = 0.5;
                bext = 0.5;
                mext = 0.5;
                break;

        case WinShape_HAMMING_HANN:
                bint = 0.5;
                mint = 0.5;
                bext = 0.54;
                mext = 0.46;
                break;

        default:
                assert( 0 );
                break;
        }

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Allocate space for left and right windows.
	 */

	hL = (double *) malloc( Nh * sizeof( double ) );
	assert( hL != (double *) NULL );

	hR = (double *) malloc( Nh * sizeof( double ) );
	assert( hR != (double *) NULL );

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Construct left and right windows based on window-size and window-shape parameters.
	 */

        TsepHalf = Tsep / 2;

	for ( i = 0; i < Nh; i ++ )
	{
		int  t;

		/*
		 * Windows are defined with t=0 in the center; the window arrays will be 0-offset
		 *  for subsequent ease of use. Hence "i" (the 0-offset index) and "t" (the
		 *  variable in the formulas in the paper).
		 */

		t = i - ( Text + TsepHalf );

		/*
		 * Compute hL[0:Nh-1] and hR[0:Nh-1] separately. Not efficient, but clear.
		 */

		if ( t < - ( Text + TsepHalf ) )
		{
			hL[ i ] = 0.0;
		}
		else if ( t < - TsepHalf )
		{
			hL[ i ] = bext + mext * cos( PI * (t + TsepHalf) / Text );
			
		}
		else if ( t <= ( - TsepHalf + Tint ) )
		{
			hL[ i ] = bint + mint * cos( PI * (t + TsepHalf) / Tint );
		}
		else
		{
			hL[ i ] = 0.0;
		}

		if ( t < ( + TsepHalf - Tint ) )
		{
			hR[ i ] = 0.0;
		}
		else if ( t < +TsepHalf )
		{
			hR[ i ] = bint + mint * cos( PI * (t - TsepHalf) / Tint );
		}
		else if ( t < + ( TsepHalf + Text ) )
		{
			hR[ i ] = bext + mext * cos( PI * (t - TsepHalf) / Text );
		}
		else
		{
			hR[ i ] = 0.0;
		}
	}

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Allocate space for the FFTs of the left and right windows.
	 */

	NhPow2 = (int) pow( 2, ceil( log2( Nh ) ) );

	Nfft = NhPow2 + NhPow2;

	fftL = (double *) malloc( Nfft * sizeof( double ) );
	assert( fftL != (double *) NULL );

	fftR = (double *) malloc( Nfft * sizeof( double ) );
	assert( fftR != (double *) NULL );

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	*TintPtr = Tint;
	*TextPtr = Text;
	*TsepPtr = Tsep;
	*TsizePtr = Nh;
	*hLPtr = hL;
	*hRPtr = hR;
	*NhPtr = Nh;
	*NhPow2Ptr = NhPow2;
	*fftLPtr = fftL;
	*fftRPtr = fftR;
	*NfftPtr = Nfft;

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * DESTRUCTOR
 */

void windowpairDESTROY
	(
		double **  hLPtr,
		double **  hRPtr,
		double **  fftLPtr,
		double **  fftRPtr
	)
{
	free( (void *) (*hLPtr) );
	*hLPtr = (double *) NULL;

	free( (void *) (*hRPtr) );
	*hRPtr = (double *) NULL;

	free( (void *) (*fftLPtr) );
	*fftLPtr = (double *) NULL;

	free( (void *) (*fftRPtr) );
	*fftRPtr = (double *) NULL;

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * SIMULTANEOUS FFT OF BOTH WINDOWED VERSIONS OF THE SAME AUDIO
 */

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
	)
{

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Originally based on:
	 *
	 *    Numerical Recipes in C : the art of scientific computing
	 *     William H. Press [et al] - 2nd ed.
	 *     ISBN 0-521-43108-5
	 *
	 *    Chapter 12.3, p 511.
	 *
	 * "Given two real input arrays data1[1..n] and data2[1..n], this routine calls four1 and
	 * returns two complex output arrays, fftL[1..2n] and fftR[1..2n], each of complex length n
	 * (i.e., real length 2*n), which contain the discrete Fourier transforms of the respective
	 * data arrays. n MUST be an integer power of 2.
	 */

	unsigned long nn3,nn2,jj,j;
	double rep,rem,aip,aim;

	double *  fft1 = fftL - 1; /* NR/C 1-offset arrays. */
	double *  fft2 = fftR - 1;

	for (j=1,jj=2;(j<=nData)&&(j<=Nh);j++,jj+=2) { /* Pack the two real arrays into one */
		                            /*  complex array. */
		double  myAudio;

		#ifdef DOPREEMPHASIS
		{
			if ( j == 1 )
			{
				myAudio = 0.0;
			}
			else
			{
				myAudio = (double)(audio[ j - 1 ]) - 0.97 * (double)(audio[ j - 2 ]);
			}
		}
		#else
		{
			myAudio = audio[ j - 1 ];
		}
		#endif

		fft1[ jj - 1 ] = myAudio * hL[ j - 1 ];
		fft1[ jj ] = myAudio * hR[ j - 1 ];
	}
	if ( nData < Nh )
	{
		for (j=nData+1,jj=2*nData+2;j<=NhPow2;j++,jj+=2) {
			fft1[jj-1]=0.0;
			fft1[jj]=0.0;
		}
	}
	else
	{
		for (j=Nh+1,jj=2*Nh+2;j<=NhPow2;j++,jj+=2) {
			fft1[jj-1]=0.0;
			fft1[jj]=0.0;
		}
	}

	nn3=1+(nn2=2+Nfft);

	four1(fft1,NhPow2,1);                                          /* Transform the complex array. */

	fft2[1]=fft1[2];
	fft1[2]=fft2[2]=0.0;
	for (j=3;j<=NhPow2+1;j+=2) {
		rep=0.5*(fft1[j]+fft1[nn2-j]);                    /* Use symmetries to separate   */
		rem=0.5*(fft1[j]-fft1[nn2-j]);                    /*  the two transforms.         */
		aip=0.5*(fft1[j+1]+fft1[nn3-j]);
		aim=0.5*(fft1[j+1]-fft1[nn3-j]);
		fft1[j]=rep;                                      /* Ship them out in two complex */
		fft1[j+1]=aim;                                    /*  arrays.                     */
		fft1[nn2-j]=rep;
		fft1[nn3-j] = -aim;
		fft2[j]=aip;
		fft2[j+1] = -rem;
		fft2[nn2-j]=aip;
		fft2[nn3-j]=rem;
	}

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * The second bin contains the highest frequency energy, which we zero here for convenience.
	 */

	fft1[ 2 ] = 0.0;
	fft2[ 2 ] = 0.0;

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

