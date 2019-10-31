#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import re

def findHoles(asc):
	holes = []
	prev = asc[0]
	for val in asc:
		diff = val - prev
		if diff > 1:
			holes.extend(range(prev+1, val))
		prev = val
	return holes

def readIFace(path):
	ifaceDoc = open(path).read()
	# remove comment
	ifaceDoc = re.sub('\s+#.+', '', ifaceDoc)
	return ifaceDoc

def findAPIHoles():
	ifaceDoc = readIFace('../include/Scintilla.iface')

	# find unused or duplicate API message number
	valList = {} # {value: [name]}
	result = re.findall(r'(fun|get|set)\s+(?P<type>\w+)\s+(?P<name>\w+)\s*=\s*(?P<value>\d+)', ifaceDoc)
	for item in result:
		name = item[2]
		value = int(item[3])
		if value in valList:
			print(f'duplicate value: {value} {name} {valList[value]}')
			valList[value].append(name)
		else:
			valList[value] = [name]

	allVals = sorted(valList.keys())
	print('all values:', allVals)
	allVals = [item for item in allVals if item < 3000]
	print('min, max and holes:', allVals[0], allVals[-1], findHoles(allVals))

def CheckLexerDefinition():
	ifaceDoc = readIFace('../include/SciLexer.iface')

	# 1. ensure SCLEX_ is unique
	valList = {} # {value: [name]}
	result = re.findall(r'val\s+(?P<name>SCLEX_\w+)\s*=\s*(?P<value>\d+)', ifaceDoc)
	for name, value in result:
		value = int(value)
		if value in valList:
			print(f'duplicate value: {value} {name} {valList[value]}')
			valList[value].append(name)
		else:
			valList[value] = [name]

	# StylesCommon in Scintilla.iface
	STYLE_DEFAULT = 32
	STYLE_LASTPREDEFINED = 39
	# 2. ensure style number is unique within same lexer and not used by StylesCommon
	prefixMap = {} # {prefix: lexer}
	result = re.findall(r'lex\s+(?P<name>\w+)\s*=(.+)+', ifaceDoc)
	for name, value in result:
		if name == 'XML':
			name = 'HTML'
		for item in value.split():
			prefixMap[item] = name

	lexrList = {} # {lexer: {value: [name]}}
	result = re.findall(r'val\s+(?P<name>SCE_\w+)\s*=\s*(?P<value>\d+)', ifaceDoc)
	for name, value in result:
		prefix = name[:name.index('_', 4) + 1] # underscore after SCE_
		lexer = prefixMap[prefix]
		valList = lexrList.setdefault(lexer, {})
		value = int(value)
		if value >= STYLE_DEFAULT and value <= STYLE_LASTPREDEFINED:
			print(f'error value: {value} {name}')
		if value in valList:
			print(f'duplicate value: {value} {name} {valList[value]}')
			valList[value].append(name)
		else:
			valList[value] = [name]

findAPIHoles()
CheckLexerDefinition()