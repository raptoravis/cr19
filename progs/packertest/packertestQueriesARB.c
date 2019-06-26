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

void crPackTestDeleteQueriesARB(void)
{
	GLubyte ids[100000];/* VECP2 */
	crDebug ( "DeleteQueriesARB is a stub and needs to be special cased  0!");
	return;
	glDeleteQueriesARB((unsigned) 10, 	(const GLuint *)ids /* VEC3 */
);
	if(errChk)
		printError("glDeleteQueriesARB((unsigned) 10, )");
	if (verbose)
		crDebug("glDeleteQueriesARB( (unsigned) 10,  )");
}
void crPackTestGenQueriesARB(void)
{
	GLubyte ids[100000];/* VECP */
	crDebug ( "GenQueriesARB is a stub and needs to be special cased  1!");
	return;
	glGenQueriesARB((unsigned) 10, 	(GLuint *)ids /* VEC3 */
);
	if(errChk)
		printError("glGenQueriesARB((unsigned) 10, )");
	if (verbose)
		crDebug("glGenQueriesARB( (unsigned) 10,  )");
}
