#!/usr/bin/env python
import sys

class CircuitSolver:

	def __init__(self):
		#nodeNames is array of strings of node names read from file
		self.nodeNames = []
		self.nCount = 0

		#vNames, iNames, rNames strings of comp names as in netlist
		self.vNames = []
		self.iNames = []
		self.rNames = []
		
		#vList, iList and rList item index correlates to relevant xNames
		#[fromNodeindex, toNodeindex, value] for each entry
		self.vList = []
		self.iList = []
		self.rList = []

	def __parse_line(self, line, component):

		temp = line.split();
		if len(temp) != 4:
			print "Length of line too long, aborting\n"
			sys.exit()
		if temp[1] in self.nodeNames:
			start = self.nodeNames.index(temp[1])
		else:
			self.nodeNames.append(temp[1])
			start = self.nCount 
			self.nCount += 1
		if temp[2] in self.nodeNames:
			end = self.nodeNames.index(temp[2])
		else:
			self.nodeNames.append(temp[2])
			end = self.nCount
			self.nCount += 1

		if component == 'R':	
			self.rNames.append(temp[0]);
			self.rList.append([start, end, int(temp[3])])
		elif component == 'V':
			self.vNames.append(temp[0]);
			self.vList.append([start, end, int(temp[3])])
		elif component == 'I':
			self.iNames.append(temp[0]);
			self.iList.append([start, end, int(temp[3])])

	def read_file(self, filename):
		f = open(filename, 'r')
		for line in f:
			if line[0] == 'R':
				self.__parse_line(line, 'R');
			elif line[0] == 'V':
				self.__parse_line(line, 'V');	
			elif line[0] == 'I':
				self.__parse_line(line, 'I');
			else:
				print "IGNORED:\n\t", line

new = CircuitSolver()

new.read_file('spiceneteg.net')

print new.nodeNames
print new.vNames
print new.rNames
print new.rList
print new.vList
	
"""
#Globals. Complain about it, see if I care
nodeNames = [] #Text repr of nodes, voltages etc in these vars
vsNames = []
isNames = []
rNames = []

vlist = [] #[[from, to, val]] Where from and to are indexes in nodeNames
	   #and index of vlist is index of vsNames
ilist = []
rlist = []


nCount = 0
rCount = 0

def parse_netfile_part(line, t_part):
	global nodeNames; global vsNames; global isNames; global rNames;
	global vlist; global ilist; global nCount; global rCount

	temp = line.split();
	if len(temp) != 4:
		print "Length of line too long, aborting\n"
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

	if t_part == 'R':	
		rNames.append(temp[0]); rCount+=1
		rlist.append([start, end, int(temp[3])])
	elif t_part == 'V':
		vsNames.append(temp[0]);
		vlist.append([start, end, int(temp[3])])
	elif t_part == 'I':
		isNames.append(temp[0]);
		ilist.append([start, end, int(temp[3])])


#File reader for netfiles. Loads up globals
def parse_netfile(fhandle):
 global nodeNames; global vsNames; global isNames; global rNames;
 global vlist; global ilist; global nCount; global rCount

 for line in fhandle:
	if line[0] == 'R':
		parse_netfile_part(line, 'R');
	elif line[0] == 'V':
		parse_netfile_part(line, 'V');	
	elif line[0] == 'I':
		parse_netfile_part(line, 'I');
	else:
		print "IGNORED:\n\t", line

"""
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
"""
#Open File
f = open('spiceneteg.net', 'r');
parse_netfile(f)

print "\n\n--------------\n\n"
print rNames
print nodeNames
print vsNames
print rlist
print vlist

#Read file and create list of nodes
#Create list of components and their nodes

#Reject invalid files naturally

#Define current directions
#e.g. IR1 from node A -> B
if '0' not in nodeNames:
	print "No Ground, exiting..."
	sys.exit()

print "\nFile read successfully!\n"
print "Defining Current Directions...\n"

for res in rlist:
	print res
	print 'I' + rNames[rlist.index(res)] + \
	" from node " + nodeNames[res[0]] + \
	" to node " + nodeNames[res[1]] 
for v in vlist:
	print v
	print 'I' + vsNames[vlist.index(v)] + \
	" from node " + nodeNames[v[0]] + \
	" to node " + nodeNames[res[1]]

Iin = []
Iout = []
#Form KCL equations based on this
for ind,node in enumerate(nodeNames):
	if node == '0':
		continue
	print "\n\n@ Node: " + node
	#Find currents
	for res in rlist:
		if res[1] == ind:
			#res describes input current
			Iin.append('I' + rNames[rlist.index(res)])
		elif res[0] == ind:
			#res describes output current
			Iout.append('I' + rNames[rlist.index(res)])
	for v in vlist:
		if v[1] == ind:
			#Iv describes input current	
			Iin.append('I' + vsNames[vlist.index(v)])
		elif v[0] == ind:
			Iout.append('I' + vsNames[vlist.index(v)])
	if len(Iin) == 0:
		Iin = '0'
	if len(Iout) == 0:
		Iout = '0'	
	print " + ".join(Iin) + " = " + " + ".join(Iout)
	
	Iin = []
	Iout = []

#KCL -> Nodal equations

#Align Nodal equations into linear matrix

#Solve for Nodes simultaneously

#Use Nodes to solve for Currents

#Use Currents to solve for powers
#Check sum = 0

"""
