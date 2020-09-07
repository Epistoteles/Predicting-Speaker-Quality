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

	Move (most) default_ variables to ffv.h.
	Correct default RIFF WAVE header size from 42 to 44 bytes.

 ===+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <getopt.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <math.h>
#include "windowpair.h"
#include "filterbank.h"
#include "dcorrxform.h"
#include "mutils.h"
#include "sutils.h"
#include "ffv.h"

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

extern char *  optarg;
extern int     optind;
extern int     opterr;
extern int     optopt;

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

static const char *          default_fbFileName      =  (char *) NULL;

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

static char *  progName;
 
/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void PRINTUSAGE()
{
	fprintf( stderr, "%s: badly formatted argument list\n", progName );
	fprintf( stderr, "%s [-tint <tint>] [-text <text>] [-tsep <tsep>] [-tfra <tfra>] [-fs <fs>] [-winShape <shape>] [-fbFileName <name>] [-dcorrxformType <type>] [-nOutput <n>] <audioFileName> <outDirName>\n", progName );

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

int main( int argc, char * argv[] )
{
	double              tint;
	double              text;
	double              tsep;
	double              tfra;
	double              fs;
	WinShape            winShape;
	char *              fbFileName;
	struct stat         statBuf;
	int                 statRetVal;
	DCorrXFormType      dCorrXFormType;
	int                 nOutput;

	char *              audioFileName;
	char *              outDirName;
	Filter *            fb;
	int                 Nf;
	int                 Ng;
	double              tsepRef;
	FfvComputer *       ffvComputerPtr;
	FILE *              fPtr;
	long                begSample;
	long                endSample;
	int                 nAudio;
	signed short int *  audio;
	int                 begIdx;
	int                 frameIdx;
	int                 Tstep;
	int                 Tsize;
	char *              outFileName;

	double *            output;

	progName = argv[ 0 ];

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Initialize command-line-modifiable parameters with default values.
	 */

	tint = default_tint;
	text = default_text;
	tsep = default_tsep;
	tfra = default_tfra;
	fs = default_fs;
	winShape = default_winShape;
	fbFileName = (char *) default_fbFileName;
	dCorrXFormType = default_dCorrXFormType;
	nOutput = default_nOutput;

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Parse command line to modify parameters, if applicable.
	 */

	while ( 1 )
	{
		int                   optChar;
		int                   option_index;
		static struct option  long_options[] =
			{
				{ "tint",            1, 0, 1 },
				{ "text",            1, 0, 2 },
				{ "tsep",            1, 0, 3 },
				{ "tfra",            1, 0, 4 },
				{ "fs",              1, 0, 5 },
				{ "winShape",        1, 0, 6 },
				{ "fbFileName",      1, 0, 7 },
				{ "dcorrxformType",  1, 0, 8 },
				{ "nOutput",         1, 0, 9 },
				{ 0, 0, 0, 0 }
			};

		optChar = getopt_long_only( argc, argv, "", long_options, &option_index );
		if ( optChar == -1 )
		{
			break;
		}

		switch( optChar )
		{
		case 1: /* tint */
			tint = str2dbl( optarg );
			break;

		case 2: /* text */
			text = str2dbl( optarg );
			break;

		case 3: /* tsep */
			tsep = str2dbl( optarg );
			break;

		case 4: /* tfra */
			tfra = str2dbl( optarg );
			break;

		case 5: /* fs */
			fs = str2dbl( optarg );
			break;

		case 6: /* winShape */
			if ( strcmp( optarg, "hamming_hamming" ) == 0 )
			{
				winShape = WinShape_HAMMING_HAMMING;
			}
			else if ( strcmp( optarg, "hann_hann" ) == 0 )
			{
				winShape = WinShape_HANN_HANN;
			}
			else if ( strcmp( optarg, "hamming_hann" ) == 0 )
			{
				winShape = WinShape_HAMMING_HANN;
			}
			else
			{
				PRINTUSAGE();
				fprintf( stderr, "%s: winShape must be on of { hamming_hamming, hann_hann, hamming_hann }\n", progName );
				exit( -1 );
			}
			break;

		case 7: /* fbFileName */
			fbFileName = optarg;
			statRetVal = stat( fbFileName, &statBuf );
			if ( statRetVal == 0 )
			{
				if ( S_ISREG( statBuf.st_mode ) )
				{
					/* ok */
				}
				else
				{
					PRINTUSAGE();
					fprintf( stderr, "%s: fbFileName %s must exist\n", progName, fbFileName );
					exit( -1 );
				}
			}
			else
			{
				PRINTUSAGE();
				fprintf( stderr, "%s: fbFileName %s must be a regular file\n", progName, fbFileName );
				exit( -1 );
			}
			break;

		case 8: /* dCorrXFormType */
			if ( strcmp( optarg, "data" ) == 0 )
			{
				dCorrXFormType = DCorrXFormTypeDATA;
			}
			else if ( strcmp( optarg, "cos1" ) == 0 )
			{
				dCorrXFormType = DCorrXFormTypeCOS1;
			}
			else if ( strcmp( optarg, "cos2" ) == 0 )
			{
				dCorrXFormType = DCorrXFormTypeCOS2;
			}
			else if ( strcmp( optarg, "sin" ) == 0 )
			{
				dCorrXFormType = DCorrXFormTypeSIN;
			}
			else if ( strcmp( optarg, "none" ) == 0 )
			{
				dCorrXFormType = DCorrXFormTypeNONE;
			}
			else
			{
				PRINTUSAGE();
				fprintf( stderr, "%s: dcorrxformType must be one of { data, cos1, cos2, sin, none }\n", progName );
				exit( -1 );
			}
			break;

		case 9: /* nOutput */
			nOutput = str2int( optarg );
			assert( nOutput >= 0 );
			break;

		case '?':
		default:
			PRINTUSAGE();
			exit( -1 );
		}
	}

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Parse input and output locations.
	 */

	audioFileName = (char *) NULL;
	outDirName = (char *) NULL;

	if ( ( argc - optind ) == 2 )
	{
		char *  outName;

		audioFileName = argv[ optind ++ ];
		outName = argv[ optind ++ ];

		statRetVal = stat( outName, &statBuf );
		if ( statRetVal == 0 )
		{
			if ( S_ISDIR( statBuf.st_mode ) )
			{
				/*
				 * outName exists and is a directory. Create a file name in it.
				 */

				int  length;

				length = strlen( outName ) + 1 + strlen( audioFileName ) + 4 + 1;
				outFileName = (char *) malloc( length * sizeof( char ) );
				assert( outFileName != (char *) NULL );
				sprintf( outFileName, "%s/%s.txt", outName, audioFileName );
			}
			else
			{
				/*
				 * outName exists but is not a directory. Creating a file with name
				 * outName would overwrite it. Abort.
				 */

				PRINTUSAGE();
				fprintf( stderr, "%s: a file with name %s already exists\n", progName, outName );
				exit( -1 );
			}
		}
		else
		{
			/*
			 * outName does not exist. Create a file name with name outName.
			 */

			int  length;

			length = strlen( outName ) + 1;
			outFileName = (char *) malloc( length * sizeof( char ) );
			assert( outFileName != (char *) NULL );
			sprintf( outFileName, "%s", outName );
		}
	}
	else if ( ( argc - optind ) == 1 )
	{
		int  length;

		audioFileName = argv[ optind ++ ];

		/*
		 * No outName. Create a file name from audioFileName.
		 */

		length = strlen( audioFileName ) + 4 + 1;
		outFileName = (char *) malloc( length * sizeof( char ) );
		assert( outFileName != (char *) NULL );
		sprintf( outFileName, "%s.txt", audioFileName );
	}
	else
	{
		PRINTUSAGE();
		exit( -1 );
	}

	/*
	 * Check that if the outFileName was automatically built, a file with that name does not
	 * already exist.
	 */

	statRetVal = stat( outFileName, &statBuf );
	if ( statRetVal == 0 )
	{
		PRINTUSAGE();
		fprintf( stderr, "%s: a file with (automatically constructed) name %s already exists\n", progName, outFileName );
		exit( -1 );
	}

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Initialize/Load filterbank, create the trappings for subsequent FFV computation, and
	 * allocate space to store the output (per frame).
	 */

	if ( fbFileName != (char *) NULL )
	{
		filterbankLOADFROMFILE( fbFileName, &Ng, &Nf, &tsepRef, &fb );
	}
	else
	{
		filterbankCREATEDEFAULT( &Ng, &Nf, &tsepRef, &fb );
	}

	ffvCREATE
		(
			tint,
			text,
			tsep,
			fs,
			winShape,
			fb,
			Nf,
			Ng,
			tsepRef,
			dCorrXFormType,
			&Tsize,
			&nOutput,
			&ffvComputerPtr
		);

	ffvPRINT( ffvComputerPtr );
		
	output = (double *) malloc( nOutput * sizeof( double ) );
	assert( output != (double *) NULL );

/* -+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+-- */

	/*
	 * Compute number of samples in audioFileName.
	 */

	fPtr = fopen( audioFileName, "r" );
	assert( fPtr != (FILE *) NULL );
	assert( fseek( fPtr, 44, SEEK_SET ) == 0 );
	begSample = ftell( fPtr );
	assert( fseek( fPtr, 0, SEEK_END ) == 0 );
	endSample = ftell( fPtr );

	/*
	 * Allocate space for audio, and load from audioFileName.
	 */

	nAudio = (int) ( endSample - begSample ) / sizeof( signed short int );
	audio = (signed short *) malloc( nAudio * sizeof( signed short int ) );
	assert( audio != (signed short *) NULL );

	assert( fseek( fPtr, 44, SEEK_SET ) == 0 );
	assert( fread( (void *) audio, sizeof( signed short int ), nAudio, fPtr ) == nAudio ); 
	fclose( fPtr );

	printf( "%s   %6.2f%%", audioFileName, 0.0 );
	fflush( stdout );

	/*
	 * Loop over frames for the audio.
	 */

	Tstep = (int) ( tfra * fs );
	if ( ( ( tfra * fs ) - (double) Tstep ) > 0.5 )
	{
		Tstep ++;
	}
	assert( Tstep > 0 );

	fPtr = fopen( outFileName, "w" );
	assert( fPtr != (FILE *) NULL );

	begIdx = 0;
	frameIdx = 0;
	while ( begIdx < nAudio )
	{
		int   endIdx;
		int   nFrameAudio;

		/*
		 * Compute number of samples in the current frame.
		 */

		endIdx = begIdx + Tsize;
		if ( endIdx > nAudio )
		{
			nFrameAudio = nAudio - begIdx;
		}
		else
		{
			nFrameAudio = endIdx - begIdx;
		}

		ffvCOMPUTE
			(
				ffvComputerPtr,
				audio,
				begIdx,
				nFrameAudio,
				output
			);

		if ( nOutput > 0 )
		{
			int  i;

			fprintf( fPtr, "%g", (float)(output[ 0 ]) );
			for  ( i = 1; i < nOutput; i ++ )
			{
				fprintf( fPtr, " %g", (float)(output[ i ]) );
			}
			fprintf( fPtr, "\n" );
		} 

		printf( "\b\b\b\b\b\b\b%6.2f%%", 100.0 * begIdx / nAudio );
		fflush( stdout );

		begIdx += Tstep;
		frameIdx ++;
	}
	printf( "\b\b\b\b\b\b\b100.00%%\n" );

	fclose( fPtr );

	free( (void *) audio );
	free( (void *) output );

	ffvDESTROY( &ffvComputerPtr );

	return 0;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

