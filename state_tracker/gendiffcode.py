# Copyright (c) 2001, Stanford University
# All rights reserved.
#
# See the file LICENSE.txt for information on redistributing this software

import sys

def main():
	name = sys.argv[1]
	Name = sys.argv[2]

	print """/* This code is AUTOGENERATED!!! */

#include "state.h"
#include "state_internals.h\""""

	print """
void crState%(Name)sDiff(CR%(Name)sBits *b, CRbitvalue *bitID,
		CRContext *fromCtx, CRContext *toCtx)
{
	CR%(Name)sState *from = &(fromCtx->%(name)s);
	CR%(Name)sState *to = &(toCtx->%(name)s);"""%vars()
	gendiffcode("state_%s.txt"%(name.lower()), name, docopy=1, doinvalid=0)
	print """}

void crState%(Name)sSwitch(CR%(Name)sBits *b, CRbitvalue *bitID,
		CRContext *fromCtx, CRContext *toCtx)
{
	CR%(Name)sState *from = &(fromCtx->%(name)s);
	CR%(Name)sState *to = &(toCtx->%(name)s);"""%vars()
	gendiffcode("state_%s.txt"%(Name.lower()), Name, docopy=0, doinvalid=1)
	print "}\n"

def gendiffcode(fname, state_name, docopy, doinvalid):
	target = "to"
	current = "from"
	bit = "b"
	extrabit = ""
	tab = "\t"
	current_guard = ""
	current_dependency = ""

	v_types = {
		'l': 'GLboolean',
		'b': 'GLbyte',
		'ub': 'GLubyte',
		's': 'GLshort',
		'us': 'GLushort',
		'i': 'GLint',
		'ui': 'GLuint',
		'f': 'GLfloat',
		'd': 'GLdouble'
	}

	FILE = open(fname, "r")

	print """	unsigned int j, i;
	CRbitvalue nbitID[CR_MAX_BITARRAY];
	for (j=0;j<CR_MAX_BITARRAY;j++)
		nbitID[j] = ~bitID[j];
	i = 0; /* silence compiler */"""

	import re
	for line in FILE.xreadlines():
		line = line.rstrip()

		if re.match("#", line):
			continue

## Handle text dump
		m = re.match("\+(.*)", line)
		if m:
			if doinvalid:
				continue
			line = m.group(1)

		else:
			m = re.match("-(.*)", line)
			if m:
				if docopy:
					continue
				line = m.group(1)

		m = re.match(">(.*)", line)
		if m:
			text = m.group(1)
			if re.search("}", line):
				tab = tab[:-1]
			print tab+text
			if re.search("{", line):
				tab = tab+"\t"
			continue
	
## Handle commands

		m = re.search("%target=(\w*)", line)
		if m:
			target = m.group(1)
		m = re.search("%current=(\w*)", line)
		if m:
			current = m.group(1)
		m = re.search("%bit=(\w*)", line)
		if m:
			bit = m.group(1)
		m = re.search("%extrabit=(\w*)", line)
		if m:
			extrabit = m.group(1)

		if re.search("%flush", line):
			if current_guard != "":
				print tab+"CLEARDIRTY(%(bit)s->%(current_guard)s, nbitID);"%vars()
				tab = tab[:-1]
				print tab+"}"
			if docopy and current_dependency != "":
				tab = tab[:-1]
				print tab+"}"
			current_guard = ""
			current_dependency = ""
		if re.search("%", line):
			continue

## Load the line
		(dependency, guardbit, members, func) = \
			(re.split(":", line) + ["", ""])[0:4]
		func = func.rstrip()

## Close the guardbit and dependency
		if current_guard != "" and current_guard != guardbit:
			print tab+"CLEARDIRTY(%(bit)s->%(current_guard)s, nbitID);"%vars()
			tab = tab[:-1]
			print tab+"}"
		if docopy and current_dependency != "" and current_dependency != dependency:
			tab = tab[:-1]
			print tab+"}"

## Open the dependency if
		if docopy and current_dependency != dependency and dependency != "":
			print tab+"if (%(target)s->%(dependency)s)\n%(tab)s{"%vars()
			tab = tab+"\t"
			current_dependency = dependency
		
## Open the guard if
		if docopy and current_dependency != dependency and dependency != "":
			print tab+"if ($(target)s->%(dependency)s)\n%(tab)s{"%vars()
			tab = tab+"\t"
		
		if current_guard != guardbit and guardbit != "":
			print tab+"if (CHECKDIRTY(%(bit)s->%(guardbit)s, bitID))\n%(tab)s{"%vars()
			tab = tab+"\t"
			if members[0] != "*" and guardbit[0:6] == "enable":
				print tab+"glAble able[2];"
				print tab+"able[0] = diff_api.Disable;"
				print tab+"able[1] = diff_api.Enable;"

		current_dependency = dependency
		current_guard = guardbit

## Handle text dump
		if members[0] == "*":
			print tab+members[1:]
		else:
			## Parse the members variable
			mainelem = re.split(",", members)
			elems = re.split("\|", members)
			if len(elems) > 1:
				mainelem = [""]
				mainelem[0] = elems[0]
				elems = re.split(",", elems[1])
				newelems = []
				for elem in elems:
					elem = mainelem[0] + "." + elem
					newelems += [elem]
				elems = newelems
			else:
				elems = re.split(",", members)

			## Check member values
			if guardbit != "extensions":
				sys.stdout.write(tab+"if (")
				first = 1
				for elem in elems:
					if first != 1:
						print " ||\n"+tab+"    ",
					first = 0
					sys.stdout.write("%(current)s->%(elem)s != %(target)s->%(elem)s"%vars())
				print ")\n"+tab+"{"
				tab = tab+"\t"

## Handle text function 
			if func[0] == "*":
				func = func[1:]
				print tab+func
			else:
				if func != "":
## Call the glhw function
					if guardbit[0:6] == "enable":
						print tab+"able["+target+"->"+elems[0]+"]("+func+");"
					elif guardbit == "extensions":
						print tab+"crState$state_name",
						if docopy == 1:
							print "Diff",
						else:
							print "Switch",
						print "Extensions( from, to );"
					else:
						funcargs = re.split(",", func)
						#print "// funcargs:",funcargs
						func = funcargs.pop(0)

						if func[-1] == "v":
							v_type = func[-2:-1]
							num_elems = len(elems)
							print tab+v_types[v_type]+" varg["+str(num_elems)+"];"
							i = 0
							for elem in elems:
								print tab+"varg["+str(i)+"] = "+target+"->"+elem+";"
								i += 1
						elif func[-3:] == "vNV":
							v_type = func[-4:-3]
							num_elems = len(elems)
							print tab+v_types[v_type]+" varg["+str(num_elems)+"];"
							i = 0
							for elem in elems:
								print tab+"varg["+str(i)+"] = "+target+"->"+elem+";"
								i += 1

						sys.stdout.write(tab+"diff_api.%(func)s ("%vars())
						for funcarg in funcargs:
							sys.stdout.write(funcarg+", ")

## Handle vargs
						if func[-1] == "v" or func[-3:] == "vNV":
							sys.stdout.write("varg")
						else:
							first = 1
							for elem in elems:
								if first != 1:
									sys.stdout.write(",\n"+tab+"    ")
								first = 0
								sys.stdout.write(target+"->"+elem)
						print ");"

## Do the sync if nessesary
			if docopy and guardbit != "extensions":
				for elem in  mainelem:
					print tab+current+"->"+elem+" = "+target+"->"+elem+";"

			## Do the clear if nessesary
			if doinvalid:
				if guardbit != "":
					print tab+"FILLDIRTY(%(bit)s->%(guardbit)s);"%vars()
				print tab+"FILLDIRTY(%(bit)s->dirty);"%vars()
				if extrabit != "":
					print tab+"FILLDIRTY(%(extrabit)s->dirty);"%vars()

			## Close the compare
			if guardbit != "extensions":
				tab = tab[:-1]
				print tab+"}"

## Do final closures
	if current_guard != "":
		print tab+"CLEARDIRTY(%(bit)s->%(current_guard)s, nbitID);"%vars()
		tab = tab[:-1]
		print tab+"}"
	if docopy and current_dependency != "":
		tab = tab[:-1]
		print tab+"} /*%(current_dependency)s*/"%vars()

	print tab+"CLEARDIRTY(%(bit)s->dirty, nbitID);"%vars()

main()
