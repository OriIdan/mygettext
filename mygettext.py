#!/usr/python
# -*- coding: utf-8 -*-
#
# mygettext module in Python
# Written by: Ori Idan <ori@heliconbooks.com>
#
# Rational:
# There is a gettext module in Python but it simply does not work and after spending about a day trying to make it work
# I have decided it would be easier to rewrite it.
#
# I don't really know Python and think this is one of the most complicated languages exist but I will try my best.
# License is LGPL so I will be happy to get code contribution from people who really know Python.
#
# This module uses directly the PO file as I have no idea of the internal format of MO files and have no time to study it.
import os, re

# Initialize the translation dictionary
# Note this is a global variable filled out by the init function
translate = {}

# getpofilename:
# Get the name of the PO file to use.
# domain - domain name (usually 'messages')
# lang - language string (such as he_IL)
# base - base directory to search
def getpofilename(domain, lang, base):
	fname = base + '/' + lang + '/LC_MESSAGES/' + domain + '.po'
	if os.path.isfile(fname):
		return fname
	return None

# init:
# Initialize the module, open the file and read it's contents into a Python dictionary
def init(domain, lang, base):
	global translate

	fname = getpofilename(domain, lang, base)
	if fname == None:
		return None;
	
	
	# Analysing the PO file works as a stage machine.
	# There are three states:
	# 0 wait for msgid
	# 1 msgid state, grab the line and add it to the message id
	# 2 msgstr state, grab the line and add it to the message string
	state = 0;
	msgid = ''
	msgstr = ''
	i = 0;
	f = open(fname, 'r')
	for l in f:
		i += 1
		if re.match('^#.*', l):
			continue
#		print "state: " + str(state) + " l: " + l
		if state == 0:
			if l == '\n':
				continue
			if (msgid != '') and (msgstr != ''):
				translate[msgid] = msgstr
				print "1 Add message id: '" + msgid + "' String: '" + msgstr + "'"
				msgid = ''
				msgstr = ''
			r = re.match('msgid "(.*)"', l)
			if r is not None:
				msgid = r.group(1)
				state = 1
		elif state == 1:
			r = re.match('"(.*)"', l)
			if r is not None:
				msgid += r.group(1)
			r = re.match('msgstr "(.*)"', l)
			if r is not None:
				msgstr = r.group(1)
				state = 2
		elif state == 2:
			if l == '\n':
				translate[msgid] = msgstr
				print "2 Add message id: '" + msgid + "' String: '" + msgstr + "'"
				msgid = ''
				msgstr = ''
				state = 0
			r = re.match('"(.*)"', l)
			if r is not None:
				msgstr += r.group(1)
			r = re.match('msgid "(.*)"', l)
			if r is not None:
				# New msgid
				translate[msgid] = msgstr
				print "3 Add message id: '" + msgid + "' String: '" + msgstr + "'"
				msgid = r.group(1)
				msgstr = ''
				state = 1

init('messages', 'he_IL', 'locales')

def gettext(str):
	global translate
	
	if translate[str] is not None:
		return translate[str]
	return str

			
