#!/usr/bin/env python
import sys

"""
* C:\Program Files (x86)\LTC\LTspiceIV\Draft1.asc
V1 N001 N004 4
R1 N001 N002 100
R2 N002 N003 150
R3 N002 N004 250
R4 N003 N004 80
.backanno
.end
"""

#Open File
f = open('spiceneteg.net', 'r');
nodeNames = []
vsNames = []
isNames = []
rNames = []

vlist = [] #[[from, to, val]] Where from and to are indexes in nodeNames
	   #and index of vlist is index of vsNames
ilist = []
rlist = []


nCount = 0
rCount = 0
for line in f:
	if line[0] == 'R':
		print "RESISTOR:\n\t", line
		temp = line.split();
		if len(temp) != 4:
			print "Length of resistor line too long, aborting\n"
			sys.exit()
		if temp[1] in nodeNames:
			start = nodeNames.index(temp[1])
		else:
			nodeNames.append(temp[1])
			start = nCount; 
			nCount+=1
		if temp[2] in nodeNames:
			end = nodeNames.index(temp[2])
		else:
			nodeNames.append(temp[2])
			end = nCount
			nCount+=1
	
		rNames.append(temp[0]); rCount+=1
		rlist.append([start, end, int(temp[3])])

	elif line[0] == 'V':
		print "VOLTAGE:\n\t", line
	elif line[0] == 'I':
		print "CURRENT:\n\t", line
	else:
		print "IGNORED:\n\t", line

print "\n\n--------------\n\n"
print rNames
print nodeNames
print rlist

#Read file and create list of nodes
#Create list of components and their nodes

#Reject invalid files naturally

#Define current directions
#e.g. IR1 from node A -> B
#Store this in new mem

#Form KCL equations based on this

#KCL -> Nodal equations

#Align Nodal equations into linear matrix

#Solve for Nodes simultaneously

#Use Nodes to solve for Currents

#Use Currents to solve for powers
#Check sum = 0
