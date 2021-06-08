/*
 * linspace.c
 *
 *  Created on: 6 Apr 2021
 *      Author: Sabrina
 */
#include "main.h"
#include <../INC/linspace.h>
#include <stdlib.h>

float linspace(int datapoint)
{
	float x;
	float step;
	if(test_type ==0){
		step = (finish1-start1)/(float)length1; //comment explainataion at some point//
		x = (float)start1 + step*(float)datapoint;
	}
	if(test_type == 1){
		float step = 2*(finish1-start1) /(float)length1;
		int midpoint = (length1)/2;
		//more explainations//
		if(datapoint < midpoint){
			x = (float)start1 + step*(float)datapoint;
		}
		if(datapoint == midpoint){
			x = (float)finish1;
		}
		if(datapoint > midpoint){
			x =(float)finish1 - step*(float)(datapoint-midpoint);
		}
	}
	return x;
}

