/* Copyright (c) 2001, Stanford University
	All rights reserved.

	See the file LICENSE.txt for information on redistributing this software. */
	
/* DO NOT EDIT - THIS FILE GENERATED BY THE opcodes.py SCRIPT */



#define GL_GLEXT_PROTOTYPES
#include <GL/gl.h>
#include <GL/glext.h>
#include <GL/glut.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "chromium.h"
#include "cr_error.h"
#include "packertest.h"

extern int errChk;
extern int verbose;
void printError(char *name);

void crPackTestPopAttrib(void)
{
    int i;

    for (i = GL_CURRENT_BIT; i <= GL_SCISSOR_BIT; i = i + 1000 ) {
	glPushAttrib(i);
	glPopAttrib();
	if (errChk)
	    printError("gl(PopAttrib)");
	if (verbose)
	    crDebug("glPopAttrib( )");
    }
}
void crPackTestPushAttrib(void)
{
    int i;

    for (i = GL_CURRENT_BIT; i <= GL_SCISSOR_BIT; i = i + 1000 ) {
	glPushAttrib(i);
	if (errChk)
	    printError("glPushAttrib((int) 16777215)");
	if (verbose)
	    crDebug("glPushAttrib( (int) 16777215 )");
	glPopAttrib();
    }
}
