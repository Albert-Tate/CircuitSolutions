#!/usr/bin/env python
import sys

"""
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
	Iout = [
"""


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

		#KCL item index correlates to nodeName index
		#[ [(fromNode, toNode, name), (fromNode, toNode)], [(fromNode, toNode)] ]
		#Each index contains two arrays: Iin and Iout
		#Each Iin/Iout entry is described as a tuple (fromNode, toNode)
		self.KCL = []

	def make_kcl(self):
		if '0' not in self.nodeNames:
			print "No ground found, exiting..."
			sys.exit()
		for ind, node in enumerate(self.nodeNames):
			temp = [ [], [] ]
			if node == '0':
				self.KCL.append(temp)
				continue
			for rind, res in enumerate(self.rList):
				if res[1] == ind:
				  #res describes input
				  temp[0].append((res[0],res[1],self.rNames[rind]))
				elif res[0] == ind:
				  temp[1].append((res[0],res[1],self.rNames[rind]))
			for vind, v in enumerate(self.vList):
				if v[1] == ind:
				  temp[0].append((v[0], v[1], self.vNames[vind]))
				elif v[0] == ind:
				  temp[1].append((v[0],v[1],self.vNames[vind]))
			self.KCL.append(temp)
			#TODO: Add support for vsource/Isource

	def print_kcl(self, resBool):
		for ind, eqn in enumerate(self.KCL):
			sTemp = "\t";
			if self.nodeNames[ind] == '0':
				continue
			print "@ " + self.nodeNames[ind]
			if eqn[0] == []:
				sTemp += "0"
			else:
				for i in eqn[0]:
					if not resBool: 
					  sTemp += "I" + i[2] + " + "
					else:
					  sTemp += "(" + \
						self.nodeNames[i[0]] + " - " + \
						self.nodeNames[i[1]] + ")/" + \
						i[2] + " + "

				sTemp = sTemp[0:-3]
			sTemp += " = "	
			if eqn[1] == []:
				sTemp += "0"
			else:
				for i in eqn[1]:
					if not resBool: 
					  sTemp += "I" + i[2] + " + "
					else:
					  sTemp += "(" + \
						self.nodeNames[i[0]] + " - " + \
						self.nodeNames[i[1]] + ")/" + \
						i[2] + " + "
				sTemp = sTemp[0:-3]
			
			if "V1" not in sTemp:
				print sTemp
			else:
				print "Voltage Source Prevents Nodal here"


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


"""print new.nodeNames
print new.vNames
print new.rNames
print new.rList
print new.vList
"""
new.make_kcl()

new.print_kcl(0)
new.print_kcl(1)
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
