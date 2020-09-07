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

#include <assert.h>
#include "mutils.h"
#include "dcorrxform.h"

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

static void dcorrxformDATA
	(
		const double *  x,
		const int       Nx,
		double *        y,
		const int       Ny
	)
{
	/*
	 * This requires the implementation of reading a matrix (plus optional vector offset).
	 */

	assert( 0 );

	return; 
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

static void dcorrxformCOS1
	(
		const double *  x,
		const int       Nx,
		double *        y,
		const int       Ny
	)
{
	/*
	 * Not implemented at this time.
	 */

	assert( 0 );

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

static void dcorrxformCOS2
	(
		const double *  x,
		const int       Nx,
		double *        y,
		const int       Ny
	)
{
	/*
	 * Not implemented at this time.
	 */

	assert( 0 );

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

static void dcorrxformSIN
	(
		const double *  x,
		const int       Nx,
		double *        y,
		const int       Ny
	)
{
	/*
	 * Not implemented at this time.
	 */

	assert( 0 );

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

static void dcorrxformNONE
	(
		const double *  x,
		const int       Nx,
		double *        y,
		const int       Ny
	)
{
	int  i;

	for ( i = 0; i < Ny; i ++ )
	{
		y[ i ] = x[ i ];
	}

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

void dcorrxformCOMPUTE
	(
		const double *        x,
		const int             Nx,
		const DCorrXFormType  dCorrXFormType,
		double *              y,
		const int             Ny
	)
{
	switch ( dCorrXFormType )
	{
	case DCorrXFormTypeDATA:
		dcorrxformDATA( x, Nx, y, Ny );
		break;

	case DCorrXFormTypeCOS1:
		assert( 0 );
		dcorrxformCOS1( x, Nx, y, Ny );
		break;

	case DCorrXFormTypeCOS2:
		dcorrxformCOS2( x, Nx, y, Ny );
		break;

	case DCorrXFormTypeSIN:
		assert( 0 );
		dcorrxformSIN( x, Nx, y, Ny );
		break;

	case DCorrXFormTypeNONE:
		dcorrxformNONE( x, Nx, y, Ny );
		break;

	default:
		assert( 0 );
		break;
	}

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

