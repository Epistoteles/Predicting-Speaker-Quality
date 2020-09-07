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
#include <stdio.h>
#include <string.h>
#include "sutils.h"
#include "filterbank.h"

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * CONSTRUCTOR (DEFAULT)
 */

void filterbankCREATEDEFAULT
	(
		int  *        NgPtr,
		int  *        NfPtr,
		double *      tsepRefPtr,
		Filter **     fbPtr
	)
{
	int       Ng;
	int       Nf;
	double    tsepRef;
	Filter *  fb;
	Filter *  filterPtr;
	int       i;
	int       filterIdx;

	Ng = 512;
	Nf = 7;
	tsepRef = 0.008;

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Allocate the required space for the entire filterbank.
	 */

        fb = (Filter *) malloc( Nf * sizeof( Filter ) );
        assert( fb != (Filter *) NULL );

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Left extremity filter (known as F_{-3}).
	 */

        filterPtr = &(fb[ 0 ]);
        filterPtr->n = 23;
	filterPtr->fx = (int *) malloc( filterPtr->n * sizeof( int ) );
	assert( filterPtr->fx != (int *) NULL );
	filterPtr->fy = (double *) malloc( filterPtr->n * sizeof( double ) );
	assert( filterPtr->fy != (double *) NULL );
	i =  0; filterPtr->fx[ i ] = 117; filterPtr->fy[ i ] = 1.0;
	i =  1; filterPtr->fx[ i ] = 118; filterPtr->fy[ i ] = 1.0;
	i =  2; filterPtr->fx[ i ] = 119; filterPtr->fy[ i ] = 1.0;
	i =  3; filterPtr->fx[ i ] = 120; filterPtr->fy[ i ] = 1.0;
	i =  4; filterPtr->fx[ i ] = 121; filterPtr->fy[ i ] = 1.0;
	i =  5; filterPtr->fx[ i ] = 122; filterPtr->fy[ i ] = 1.0;
	i =  6; filterPtr->fx[ i ] = 123; filterPtr->fy[ i ] = 1.0;
	i =  7; filterPtr->fx[ i ] = 124; filterPtr->fy[ i ] = 1.0;
	i =  8; filterPtr->fx[ i ] = 125; filterPtr->fy[ i ] = 1.0;
	i =  9; filterPtr->fx[ i ] = 126; filterPtr->fy[ i ] = 1.0;
	i = 10; filterPtr->fx[ i ] = 127; filterPtr->fy[ i ] = 1.0;
	i = 11; filterPtr->fx[ i ] = 128; filterPtr->fy[ i ] = 1.0;
	i = 12; filterPtr->fx[ i ] = 129; filterPtr->fy[ i ] = 1.0;
	i = 13; filterPtr->fx[ i ] = 130; filterPtr->fy[ i ] = 1.0;
	i = 14; filterPtr->fx[ i ] = 131; filterPtr->fy[ i ] = 1.0;
	i = 15; filterPtr->fx[ i ] = 132; filterPtr->fy[ i ] = 1.0;
	i = 16; filterPtr->fx[ i ] = 133; filterPtr->fy[ i ] = 1.0;
	i = 17; filterPtr->fx[ i ] = 134; filterPtr->fy[ i ] = 1.0;
	i = 18; filterPtr->fx[ i ] = 135; filterPtr->fy[ i ] = 1.0;
	i = 19; filterPtr->fx[ i ] = 136; filterPtr->fy[ i ] = 1.0;
	i = 20; filterPtr->fx[ i ] = 137; filterPtr->fy[ i ] = 1.0;
	i = 21; filterPtr->fx[ i ] = 138; filterPtr->fy[ i ] = 1.0;
	i = 22; filterPtr->fx[ i ] = 139; filterPtr->fy[ i ] = 1.0;
	/* normalize area below */

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Filter corresponding to quickly falling pitch (known as F_{-2}).
	 */

	filterPtr = &(fb[ 1 ]);
	filterPtr->n = 7;
	filterPtr->fx = (int *) malloc( filterPtr->n * sizeof( int ) );
	assert( filterPtr->fx != (int *) NULL );
	filterPtr->fy = (double *) malloc( filterPtr->n * sizeof( double ) );
	assert( filterPtr->fy != (double *) NULL );
	i = 0; filterPtr->fx[ i ] = 245; filterPtr->fy[ i ] = 0.5;
	i = 1; filterPtr->fx[ i ] = 246; filterPtr->fy[ i ] = 1.0;
	i = 2; filterPtr->fx[ i ] = 247; filterPtr->fy[ i ] = 1.0;
	i = 3; filterPtr->fx[ i ] = 248; filterPtr->fy[ i ] = 1.0;
	i = 4; filterPtr->fx[ i ] = 249; filterPtr->fy[ i ] = 1.0;
	i = 5; filterPtr->fx[ i ] = 250; filterPtr->fy[ i ] = 1.0;
	i = 6; filterPtr->fx[ i ] = 251; filterPtr->fy[ i ] = 0.5;
	/* normalize area below */

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Filter corresponding to slowly falling pitch (known as F_{-1}).
	 */

	filterPtr = &(fb[ 2 ]);
	filterPtr->n = 7;
	filterPtr->fx = (int *) malloc( filterPtr->n * sizeof( int ) );
	assert( filterPtr->fx != (int *) NULL );
	filterPtr->fy = (double *) malloc( filterPtr->n * sizeof( double ) );
	assert( filterPtr->fy != (double *) NULL );
	i = 0; filterPtr->fx[ i ] = 249; filterPtr->fy[ i ] = 0.5;
	i = 1; filterPtr->fx[ i ] = 250; filterPtr->fy[ i ] = 1.0;
	i = 2; filterPtr->fx[ i ] = 251; filterPtr->fy[ i ] = 1.0;
	i = 3; filterPtr->fx[ i ] = 252; filterPtr->fy[ i ] = 1.0;
	i = 4; filterPtr->fx[ i ] = 253; filterPtr->fy[ i ] = 1.0;
	i = 5; filterPtr->fx[ i ] = 254; filterPtr->fy[ i ] = 1.0;
	i = 6; filterPtr->fx[ i ] = 255; filterPtr->fy[ i ] = 0.5;
	/* normalize area below */

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Filter corresponding to flat pitch (known as F_{0}).
	 */

	filterPtr = &(fb[ 3 ]);
	filterPtr->n = 5;
	filterPtr->fx = (int *) malloc( filterPtr->n * sizeof( int ) );
	assert( filterPtr->fx != (int *) NULL );
	filterPtr->fy = (double *) malloc( filterPtr->n * sizeof( double ) );
	assert( filterPtr->fy != (double *) NULL );
	i = 0; filterPtr->fx[ i ] = 254; filterPtr->fy[ i ] = 0.5;
	i = 1; filterPtr->fx[ i ] = 255; filterPtr->fy[ i ] = 1.0;
	i = 2; filterPtr->fx[ i ] = 256; filterPtr->fy[ i ] = 1.0;
	i = 3; filterPtr->fx[ i ] = 257; filterPtr->fy[ i ] = 1.0;
	i = 4; filterPtr->fx[ i ] = 258; filterPtr->fy[ i ] = 0.5;
	/* normalize area below */

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Filter corresponding to slowly rising pitch (known as F_{+1}).
	 */

	filterPtr = &(fb[ 4 ]);
	filterPtr->n = 7;
	filterPtr->fx = (int *) malloc( filterPtr->n * sizeof( int ) );
	assert( filterPtr->fx != (int *) NULL );
	filterPtr->fy = (double *) malloc( filterPtr->n * sizeof( double ) );
	assert( filterPtr->fy != (double *) NULL );
	i = 0; filterPtr->fx[ i ] = 257; filterPtr->fy[ i ] = 0.5;
	i = 1; filterPtr->fx[ i ] = 258; filterPtr->fy[ i ] = 1.0;
	i = 2; filterPtr->fx[ i ] = 259; filterPtr->fy[ i ] = 1.0;
	i = 3; filterPtr->fx[ i ] = 260; filterPtr->fy[ i ] = 1.0;
	i = 4; filterPtr->fx[ i ] = 261; filterPtr->fy[ i ] = 1.0;
	i = 5; filterPtr->fx[ i ] = 262; filterPtr->fy[ i ] = 1.0;
	i = 6; filterPtr->fx[ i ] = 263; filterPtr->fy[ i ] = 0.5;
	/* normalize area below */

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Filter corresponding to quickly rising pitch (known as F_{+2}).
	 */

	filterPtr = &(fb[ 5 ]);
	filterPtr->n = 7;
	filterPtr->fx = (int *) malloc( filterPtr->n * sizeof( int ) );
	assert( filterPtr->fx != (int *) NULL );
	filterPtr->fy = (double *) malloc( filterPtr->n * sizeof( double ) );
	assert( filterPtr->fy != (double *) NULL );
	i = 0; filterPtr->fx[ i ] = 261; filterPtr->fy[ i ] = 0.5;
	i = 1; filterPtr->fx[ i ] = 262; filterPtr->fy[ i ] = 1.0;
	i = 2; filterPtr->fx[ i ] = 263; filterPtr->fy[ i ] = 1.0;
	i = 3; filterPtr->fx[ i ] = 264; filterPtr->fy[ i ] = 1.0;
	i = 4; filterPtr->fx[ i ] = 265; filterPtr->fy[ i ] = 1.0;
	i = 5; filterPtr->fx[ i ] = 266; filterPtr->fy[ i ] = 1.0;
	i = 6; filterPtr->fx[ i ] = 267; filterPtr->fy[ i ] = 0.5;
	/* normalize area below */

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Right extremity filter (known as F_{-3}).
	 */

	filterPtr = &(fb[ 6 ]);
	filterPtr->n = 23;
	filterPtr->fx = (int *) malloc( filterPtr->n * sizeof( int ) );
	assert( filterPtr->fx != (int *) NULL );
	filterPtr->fy = (double *) malloc( filterPtr->n * sizeof( double ) );
	assert( filterPtr->fy != (double *) NULL );
	i =  0; filterPtr->fx[ i ] = 373; filterPtr->fy[ i ] = 1.0;
	i =  1; filterPtr->fx[ i ] = 374; filterPtr->fy[ i ] = 1.0;
	i =  2; filterPtr->fx[ i ] = 375; filterPtr->fy[ i ] = 1.0;
	i =  3; filterPtr->fx[ i ] = 376; filterPtr->fy[ i ] = 1.0;
	i =  4; filterPtr->fx[ i ] = 377; filterPtr->fy[ i ] = 1.0;
	i =  5; filterPtr->fx[ i ] = 378; filterPtr->fy[ i ] = 1.0;
	i =  6; filterPtr->fx[ i ] = 379; filterPtr->fy[ i ] = 1.0;
	i =  7; filterPtr->fx[ i ] = 380; filterPtr->fy[ i ] = 1.0;
	i =  8; filterPtr->fx[ i ] = 381; filterPtr->fy[ i ] = 1.0;
	i =  9; filterPtr->fx[ i ] = 382; filterPtr->fy[ i ] = 1.0;
	i = 10; filterPtr->fx[ i ] = 383; filterPtr->fy[ i ] = 1.0;
	i = 11; filterPtr->fx[ i ] = 384; filterPtr->fy[ i ] = 1.0;
	i = 12; filterPtr->fx[ i ] = 385; filterPtr->fy[ i ] = 1.0;
	i = 13; filterPtr->fx[ i ] = 386; filterPtr->fy[ i ] = 1.0;
	i = 14; filterPtr->fx[ i ] = 387; filterPtr->fy[ i ] = 1.0;
	i = 15; filterPtr->fx[ i ] = 388; filterPtr->fy[ i ] = 1.0;
	i = 16; filterPtr->fx[ i ] = 389; filterPtr->fy[ i ] = 1.0;
	i = 17; filterPtr->fx[ i ] = 390; filterPtr->fy[ i ] = 1.0;
	i = 18; filterPtr->fx[ i ] = 391; filterPtr->fy[ i ] = 1.0;
	i = 19; filterPtr->fx[ i ] = 392; filterPtr->fy[ i ] = 1.0;
	i = 20; filterPtr->fx[ i ] = 393; filterPtr->fy[ i ] = 1.0;
	i = 21; filterPtr->fx[ i ] = 394; filterPtr->fy[ i ] = 1.0;
	i = 22; filterPtr->fx[ i ] = 395; filterPtr->fy[ i ] = 1.0;
	/* normalize area below */

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Normalize area for all filters.
	 */

	for ( filterIdx = 0; filterIdx < Nf; filterIdx ++ )
	{
		Filter *  filterPtr;
		double    sum;
		int       i; 

		filterPtr = &(fb[ filterIdx ]);

		sum = 0.0;
		for ( i = 0; i < filterPtr->n; i ++ )
		{ 
			sum += filterPtr->fy[ i ];
		}
		assert( sum > 0.0 );

		for ( i = 0; i < filterPtr->n; i ++ )
		{
			filterPtr->fy[ i ] /= sum;
		}
	}
 
/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	*NgPtr = Ng;
	*NfPtr = Nf;
	*tsepRefPtr = tsepRef;
	*fbPtr = fb;
 
	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * CONSTRUCTOR (ALTERNATE, FROM FILE)
 */

void filterbankLOADFROMFILE
	(
		const char *  fileName,
		int  *        NgPtr,
		int  *        NfPtr,
		double *      tsepRefPtr,
		Filter **     fbPtr
	)
{
	FILE *    filePtr;
	#define   LINEBUFFERLEN 1024
	char      lineBuffer[ LINEBUFFERLEN ];
	int       Ng;
	int       Nf;
	double    tsepRef;
	Filter *  fb;

	filePtr = fopen( fileName, "r" );
	assert( filePtr != (FILE *) NULL );

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Determine the size of the spectrum (Ng) and the number of filters (Nf).
	 */

	Ng = 0;
	Nf = 0;
	tsepRef = 0.0;
	while ( fgets( lineBuffer, LINEBUFFERLEN, filePtr ) != (char *) NULL )
	{
		const char *  tokenSeparator = " \t\n\r";
		char *        tokenPtr;

		/* first token: parameter type */

		tokenPtr = strtok( lineBuffer, tokenSeparator );
		if ( tokenPtr != (char *) NULL )
		{
			if ( strcmp( tokenPtr, "NINPUT" ) == 0 )
			{
				/* second token: value of Ng */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr != (char *) NULL );

				Ng = str2int( tokenPtr );
				assert( Ng > 0 );

				/* no third token */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr == (char *) NULL );
			}
			else if ( strcmp( tokenPtr, "NFILTER" ) == 0 )
			{
				/* second token: value of Nf */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr != (char *) NULL );

				Nf = str2int( tokenPtr );
				assert( Nf > 0 );

				/* no third token */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr == (char *) NULL );
			}
			else if ( strcmp( tokenPtr, "TSEPREF" ) == 0 )
			{
				/* second token: value of tsepRef */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr != (char *) NULL );

				tsepRef = str2dbl( tokenPtr );
				assert( tsepRef > 0 );

				/* no third token */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr == (char *) NULL );
			}
		}
	}

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Allocate the required space for the entire filterbank.
	 */

        fb = (Filter *) malloc( Nf * sizeof( Filter ) );
        assert( fb != (Filter *) NULL );

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Load filterbank structure into allocated space (remember to reseek beginning of file).
	 */

	fseek( filePtr, 0, SEEK_SET );
	while ( fgets( lineBuffer, LINEBUFFERLEN, filePtr ) != (char *) NULL )
	{
		const char *  tokenSeparator = " \t\n\r";
		char *        tokenPtr;

		/* first token: parameter type */

		tokenPtr = strtok( lineBuffer, tokenSeparator );
		if ( tokenPtr != (char *) NULL )
		{
			if ( strcmp( tokenPtr, "NINPUT" ) == 0 )
			{
				int  myNg;

				/* second token: value of Ng */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr != (char *) NULL );

				myNg = str2int( tokenPtr );
				assert( myNg == Ng );

				/* no third token */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr == (char *) NULL );
			}
			else if ( strcmp( tokenPtr, "NFILTER" ) == 0 )
			{
				int  myNf;

				/* second token: value of Nf */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr != (char *) NULL );

				myNf = str2int( tokenPtr );
				assert( myNf == Nf );

				/* no third token */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr == (char *) NULL );
			}
			else if ( strcmp( tokenPtr, "TSEPREF" ) == 0 )
			{
				double  myTsepRef;

				/* second token: value of tsepRef */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr != (char *) NULL );

				myTsepRef = str2dbl( tokenPtr );
				assert( myTsepRef == tsepRef );

				/* no third token */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr == (char *) NULL );
			}
			else if ( strcmp( tokenPtr, "FILTER" ) == 0 )
			{
				int       filterIdx;
				int       n;
				int *     fx;
				double *  fy;
				int       i;
				double    sum;

				/* second token: index of this filter */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr != (char *) NULL );

				filterIdx = str2int( tokenPtr );
				assert( ( filterIdx >= 0 ) && ( filterIdx < Nf ) );

				/* third token: number of this filter's (input) samples */

				tokenPtr = strtok( (char *) NULL, tokenSeparator );
				assert( tokenPtr != (char *) NULL );

				n = str2int( tokenPtr );
				assert( ( n > 0 ) && ( n <= Ng ) );

				/* allocate space for this filter */

					fx = (int *) malloc( n * sizeof( int ) );
				assert( fx != (int *) NULL );

				fy = (double *) malloc( n * sizeof( double ) );
				assert( fy != (double *) NULL );

				i = 0;

				/* (4+i)'th and (4+1+i)'th tokens: sample index and filter sample value */

				while ( ( tokenPtr = strtok( (char *) NULL, tokenSeparator ) ) != (char *) NULL )
				{
					int     x;
					double  y;

					assert( i < n );

					x = str2int( tokenPtr );
					assert( ( x > 0 ) && ( x <= Ng ) );

					tokenPtr = strtok( (char *) NULL, tokenSeparator );
					assert( tokenPtr != (char *) NULL );

					y = str2dbl( tokenPtr );

					fx[ i ] = x;
					fy[ i ] = y;

					i ++;
				}

				sum = 0.0;
				for ( i = 0; i < n; i ++ )
				{
					sum += fy[ i ];
				}
				assert( sum > 0 );

				for ( i = 0; i < n; i ++ )
				{
					fy[ i ] /= sum;
				}

				fb[ filterIdx ].n = n;
				fb[ filterIdx ].fx = fx;
				fb[ filterIdx ].fy = fy;
			}
			else if ( strcmp( tokenPtr, "#" ) == 0 )
			{
				/* skip, comment */
			}
			else
			{
				assert( 0 );
			}
		}
	}

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	fclose( filePtr );

	*NgPtr = Ng;
	*NfPtr = Nf;
	*tsepRefPtr = tsepRef;
	*fbPtr = fb;
 
	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void filterbankDESTROY
	(
		Filter **  fbPtr,
		const int  Nf
	)
{
	int  filterIdx;

	for ( filterIdx = 0; filterIdx < Nf; filterIdx ++ )
	{
		free( (void *) ((*fbPtr)[ filterIdx ].fx) );
		free( (void *) ((*fbPtr)[ filterIdx ].fy) );
	}

	free( (void *) (*fbPtr) );

	*fbPtr = (Filter *) NULL;

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void filterbankGETMASK
	(
		const Filter *  fb,
		const int       Nf,
		const int       Ng,
		int *           gMask
	)
{
	int    r;
	int    filterIdx;

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Exclude all input spectrum points.
	 */

	for ( r = 0; r < Ng; r ++ )
	{
		gMask[ r ] = 0;
	}

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * If any filter filterPtr in filterbank fb requires point filterPtr->fx[ i ], then that
	 * point must be in the mask.
	 */

	for ( filterIdx = 0; filterIdx < Nf; filterIdx ++ )
	{
		const Filter *  filterPtr;
		int       i;

		filterPtr = &(fb[ filterIdx ]);
		for ( i = 0; i < filterPtr->n; i ++ )
		{
			if ( filterPtr->fy[ i ] != 0.0 )
			{
				assert( filterPtr->fx[ i ] >= 0 );
				assert( filterPtr->fx[ i ] < Ng );

				gMask[ filterPtr->fx[ i ] ] = 1;
			}
		}
	}

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void filterbankCOMPUTE
	(
		const double *  input,
		const Filter *  fb,
		const int       Nf,
		double *        output
	)
{
	int  filterIdx;

	for ( filterIdx = 0; filterIdx < Nf; filterIdx ++ )
	{
		const Filter *  filterPtr;
		int             n;
		int *           fx;
		double *        fy;
		double          myOutput;
		int             i;

		filterPtr = &(fb[ filterIdx ]);
		n = filterPtr->n;
		fx = filterPtr->fx;
		fy = filterPtr->fy;

		myOutput = 0.0;
		for ( i = 0; i < n; i ++ )
		{
			myOutput += ( input[ fx[ i ] ] * fy[ i ] );
		}

		output[ filterIdx ] = myOutput;
	}

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

