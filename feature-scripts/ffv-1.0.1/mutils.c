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

 ---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+----0

Several functions in this file were inspired by

William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery.
Numerical Recipes in C: The Art of Scientific Computing.
Copyright (c) 1988-1992 by Cambridge University Press.

 ===+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include "mutils.h"

#define PI 3.141592653589793
#define TWOPI (PI+PI)

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * FAST FOURIER TRANSFORM FOR COMPLEX INPUT 
 *
 * Originally based on
 *
 *    Numerical Recipes in C : the art of scientific computing
 *     William H. Press [et al] - 2nd ed.
 *     ISBN 0-521-43108-5
 *
 *    Chapter 12.2, p 507.
 *
 * Modifications:
 *
 *  12.03.2004 kornel
 *
 *    + Changed every instance of float to double.
 *    + Changed the initialization of theta from
 *        theta=isign*(TWOPI/mmax);
 *      to
 *        theta=-isign*(TWOPI/mmax);
 */

#define SWAP(a,b) tempr=(a);(a)=(b);(b)=tempr
 
void four1(double data[], unsigned long nn, int isign)
/*
 * Replaces data[1..2*nn] by its discrete Fourier transform, if isign is input as 1; or replaces
 * data[1..2*nn] by nn times its inverse discrete Fourier transform, if isign is input as -1. data
 * is a complex array of length nn or, equivalently, a real array of length 2*nn. nn MUST be an
 * integer power of 2 (this is not checked for!).
 */
{
	unsigned long n,mmax,m,j,istep,i;
	double wtemp,wr,wpr,wpi,wi,theta;                      /* Double precision for the trigo- */
	double tempr,tempi;                                    /*  nometric recurrences.          */

	n=nn << 1;
	j=1;
	for (i=1;i<n;i+=2) {                                 /* This is the bit-reversal section  */
		if (j > i) {                                 /*  of the routine.                  */
			SWAP(data[j],data[i]);               /* Exchange the two complex numbers. */
			SWAP(data[j+1],data[i+1]);
		}
		m=n >> 1;
		while (m >= 2 && j > m) {
			j -= m;
			m >>= 1;
		}
		j += m;
	}
	                             /* Here begins the Danielson-Lanczos section of the routine. */
	mmax=2;
	while (n > mmax) {                                 /* Outer loop executed log_2 nn times. */
		istep=mmax << 1;
		theta=-isign*(TWOPI/mmax);                    /* Initialize the trigo- */
		wtemp=sin(0.5*theta);                                    /*  nometric recurrence. */
		wpr = -2.0*wtemp*wtemp;
		wpi=sin(theta);
		wr=1.0;
		wi=0.0;
		for (m=1;m<mmax;m+=2) {                                /* Here are the two nested */
			for (i=m;i<=n;i+=istep) {                      /*  inner loops.           */
				j=i+mmax;                              /* This is the Danielson-  */
				tempr=wr*data[j]-wi*data[j+1];         /*  Lanczos formula:       */
				tempi=wr*data[j+1]+wi*data[j];
				data[j]=data[i]-tempr;
				data[j+1]=data[i+1]-tempi;
				data[i] += tempr;
				data[i+1] += tempi;
			}
			wr=(wtemp=wr)*wpr-wi*wpi+wr;                 /* Trigonometric recurrence. */
			wi=wi*wpr+wtemp*wpi+wi;
		}
		mmax=istep;
	}
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * FAST FOURIER TRANSFORM FOR REAL INPUT
 *
 * Originally based on
 *
 *    Numerical Recipes in C : the art of scientific computing
 *     William H. Press [et al] - 2nd ed.
 *     ISBN 0-521-43108-5
 *
 *    Chapter 12.3, p 513.
 *
 * Modifications:
 *
 *  12.03.2004 kornel
 *
 *    + Changed every instance of double to double.
 *    + Changed the initialization of theta from
 *       theta=PI/(double) (n>>1);
 *      to
 *       theta=-PI/(double) (n>>1);
 */

void realft(double data[], unsigned long n, int isign)
/*
 * Calculates the Fourier transform of a set of n real-valued data points. Replaces this data
 * (which is stored in array data[1..n]) by the positive frequency half of its complex Fourier
 * transform. The real-valued first and last components of the complex transform are returned as
 * elements data[1] and data[2], respectively. n must be a power of 2. This routine also calculates
 * the inverse transform of a complex data array if it is the transform of real data. (Result in
 * this case must be multiplied by 2/n.)
 */
{
	void four1(double data[], unsigned long nn, int isign);
	unsigned long i,i1,i2,i3,i4,np3;
	double c1=0.5,c2,h1r,h1i,h2r,h2i;
	double wr,wi,wpr,wpi,wtemp,theta;                      /* Double precision for the trigo- */
	                                                       /*  nometric recurrences.          */
	theta=-PI/(double) (n>>1);                             /* Initialize the recurrence.      */
	if (isign == 1) {
		c2 = -0.5;
		four1(data,n>>1,1);                             /* The forward transform is here. */
	} else {
		c2=0.5;                                        /* Otherwise set up for an inverse */
		theta = -theta;                                /*  transform.                     */
	}
	wtemp=sin(0.5*theta);
	wpr = -2.0*wtemp*wtemp;
	wpi=sin(theta);
	wr=1.0+wpr;
	wi=wpi;
	np3=n+3;
	for (i=2;i<=(n>>2);i++) {                              /* Case i=1 done separately below. */
		i4=1+(i3=np3-(i2=1+(i1=i+i-1)));
		h1r=c1*(data[i1]+data[i3]);                    /* The two separate transforms are */
		h1i=c1*(data[i2]-data[i4]);                    /*  separated out of data.         */
		h2r = -c2*(data[i2]+data[i4]);
		h2i=c2*(data[i1]-data[i3]);
		data[i1]=h1r+wr*h2r-wi*h2i;                   /* Here they are recombined to form */
		data[i2]=h1i+wr*h2i+wi*h2r;                   /*  the true transform of the       */
		data[i3]=h1r-wr*h2r+wi*h2i;                   /*  original real data.             */
		data[i4] = -h1i+wr*h2i+wi*h2r;
		wr=(wtemp=wr)*wpr-wi*wpi+wr;                                   /* The recurrence. */
		wi=wi*wpr+wtemp*wpi+wi;
	}
	if (isign == 1) {
		data[1] = (h1r=data[1])+data[2];               /* Squeeze the first and last      */
		data[2] = h1r-data[2];                         /*  data together to get them      */
	} else {                                               /*  all within the original array. */
		data[1]=c1*(h1r=data[1])+data[2];
		data[2]=c1*(h1r-data[2]);
		four1(data,n>>1,-1);                             /* This is the inverse transform */
	}                                                        /*  for the case isign=-1.       */
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * FAST COS-II TRANSFORM
 *
 * Originally based on
 *
 *    Numerical Recipes in C : the art of scientific computing
 *     William H. Press [et al] - 2nd ed.
 *     ISBN 0-521-43108-5
 *
 *    Chapter 12.3, p 520.
 *
 * Modifications:
 *
 *  28.07.2009 kornel
 *
 *    + Changed every instance of float to double.
 *    + Added return statement.
 */

void cosft2(double y[], int n, int isign)
/* Calculates the "staggered" cosine transform of a set y[1..n] of real-valued data points. The
 * transformed data replace the original data in array y. n must be a power of 2. Set isign to +1
 * for a transform, and to -1 for an inverse transform. For an inverse transform, the output array
 * should be multiplied by 2/n.
 */
{
	void realft(double data[], unsigned long n, int isign);
	int i;
	double sum,sum1,y1,y2,ytemp;
	double theta,wi=0.0,wi1,wpi,wpr,wr=1.0,wr1,wtemp;

	                                   /* Double precision for the trigonometric recurrences. */

	theta=0.5*PI/n;                                            /* Initialize the recurrences. */
	wr1=cos(theta);
	wi1=sin(theta);
	wpr = -2.0*wi1*wi1;
	wpi=sin(2.0*theta);
	if (isign == 1) {                                                   /* Forward transform. */
		 for (i=1;i<=n/2;i++) {
			y1=0.5*(y[i]+y[n-i+1]);             /* Calculate the auxillary transform. */
			y2=wi1*(y[i]-y[n-i+1]);
			y[i]=y1+y2;
			y[n-i+1]=y1-y2;
			wr1=(wtemp=wr1)*wpr-wi1*wpi+wr1;             /* Carry out the recurrence. */
			wi1=wi1*wpr+wtemp*wpi+wi1;
		}
		realft(y,n,1);                               /* Transform the auxillary function. */
		for (i=3;i<=n;i+=2) {                                              /* Even terms. */
			wr=(wtemp=wr)*wpr-wi*wpi+wr;
			wi=wi*wpr+wtemp*wpi+wi;
			y1=y[i]*wr-y[i+1]*wi;
			y2=y[i+1]*wr+y[i]*wi;
			y[i]=y1;
			y[i+1]=y2;
		}
		sum=0.5*y[2];              /* Initialize recurrence for odd terms with 1/2 R_N/2. */
		for (i=n;i>=2;i-=2) {                      /* Carry out recurrence for odd terms. */ 
			sum1=sum;
			sum += y[i];
			y[i]=sum1;
		}
	} else if (isign == -1) {                                           /* Inverse transform. */
		ytemp=y[n];
		for (i=n;i>=4;i-=2) y[i]=y[i-2]-y[i];        /* Form the difference of odd terms. */
		y[2]=2.0*ytemp;
		for (i=3;i<=n;i+=2) {                                   /* Calculate R_k and I_k. */
			wr=(wtemp=wr)*wpr-wi*wpi+wr;
			wi=wi*wpr+wtemp*wpi+wi;
			y1=y[i]*wr+y[i+1]*wi;
			y2=y[i+1]*wr-y[i]*wi;
			y[i]=y1;
			y[i+1]=y2;
		}
		realft(y,n,-1);
		for (i=1;i<=n/2;i++) {                                 /* Invert auxiliary array. */
			y1=y[i]+y[n-i+1];
			y2=(0.5/wi1)*(y[i]-y[n-i+1]);
			y[i]=0.5*(y1+y2);
			y[n-i+1]=0.5*(y1-y2);
			wr1=(wtemp=wr1)*wpr-wi1*wpi+wr1;
			wi1=wi1*wpr+wtemp*wpi+wi1;
		}
	}

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * FAST SINE TRANSFORM
 *
 * Originally based on
 *
 *    Numerical Recipes in C : the art of scientific computing
 *     William H. Press [et al] - 2nd ed.
 *     ISBN 0-521-43108-5
 *
 *    Chapter 12.3, p 517.
 *
 * Modifications:
 *
 *  ??.??.2007 kornel
 *
 *  + Changed all instances of float to double.
 *  + Added return statement at end.
 */

void sinft(double y[], int n)
/* Calculates the sine transform of a set of n real-valued data points stored in array y[1..n]. The
 * number n must be a power of 2. On exit, y is replaced by its transform. This program, without
 * changes, also calculates the inverse sine transform, but in this case the output array should be
 * multiplied by 2/n.
 */
{
	void realft(double data[], unsigned long n, int isign);
	int j,n2=n+2;
	double sum,y1,y2;
	double theta,wi=0.0,wr=1.0,wpi,wpr,wtemp;

                                            /* Double precision in the trigonometric recurrences. */

	theta=3.14159265358979/(double) n;                          /* Initialize the recurrence. */
	wtemp=sin(0.5*theta);
	wpr = -2.0*wtemp*wtemp;
	wpi=sin(theta);
	y[1]=0.0;
	for (j=2;j<=(n>>1)+1;j++) {
		wr=(wtemp=wr)*wpr-wi*wpi+wr;      /* Calculate the sine for the auxilliary array. */
		wi=wi*wpr+wtemp*wpi+wi;       /* The cosine is needed to continue the recurrence. */
		y1=wi*(y[j]+y[n2-j]);                          /* Construct the auxilliary array. */
		y2=0.5*(y[j]-y[n2-j]);
		y[j]=y1+y2;                                       /* Terms j and N-j are related. */
		y[n2-j]=y1-y2;
	}
	realft(y,n,1);                                         /* Transform the auxilliary array. */
	y[1]*=0.5;                                /* Initialize the sum used for odd terms below. */
	sum=y[2]=0.0;
	for (j=1;j<=n-1;j+=2) {
		sum += y[j];
		y[j]=y[j+1];                                   /* Even terms determined directly. */
		y[j+1]=sum;                          /* Odd terms determined by this running sum. */
	}

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

/*
 * WRITE DOUBLE VECTOR TO FILE
 *
 * Created on ??.??.2003.
 */

void dblvecWRITE
	(
		const char *    fileName,
		const double *  vector,
		const int       N
	)
{
	FILE *  fPtr;
	int     i;

	fPtr = fopen( fileName, "w" );
	assert( fPtr != (FILE *) NULL );

	for ( i = 0; i < N; i ++ )
	{
		fprintf( fPtr, "%f\n", vector[ i ] );
	}

	fclose( fPtr );

	return;
}

/* =+====1====+====2====+====3====+====4====+====5====+====6====+====7====+====8====+====9====+== */

