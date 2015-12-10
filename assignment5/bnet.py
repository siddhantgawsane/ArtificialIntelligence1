class BayesianNetwork(object):
	def computeProbability(self, b, e, a, j, m):
		result = (self.P("B",b,None,None) * self.P("E",e,None,None) * self.P("A|B,E",a,b,e) * self.P("J|A",j,a,None) * self.P("M|A",m,a,None))
		# print b,e,a,j,m
		# print "%.10f" % (result)
		return result

	def P(self,query,value1,value2,value3):
		if query == "B":
			if value1:
				return 0.001
			else:
				return 0.999
		
		if query == "E":
			if value1:
				return 0.002
			else:
				return 0.998
		
		if query == "A|B,E":
			if value2 and value3:
				temp = 0.95
			if value2 and not value3:
				temp = 0.94
			if not value2 and value3:
				temp = 0.29
			if not value2 and not value3:
				temp = 0.001
			if value1:
				return temp
			else:
				return (1-temp)
		
		if query == "J|A":
			if value2:
				temp = 0.9
			else:
				temp = 0.05
			if value1:
				return temp
			else:
				return (1-temp)
		
		if query == "M|A":
			if value2:
				temp = 0.7
			else:
				temp = 0.01
			if value1:
				return temp
			else:
				return (1-temp)

	def enumerate(self,variables):
		# print variables
		if not None in variables:
			return self.computeProbability(variables[0],variables[1],variables[2],variables[3],variables[4])
		else:
			noneIdx = variables.index(None)
			new_variables = list(variables)
			new_variables[noneIdx] = True
			val1 = self.enumerate(new_variables)
			new_variables[noneIdx] = False
			val2 = self.enumerate(new_variables)
			return val1 + val2

	def generateValues(self,variables):
		result = []
		if "Bt"	in variables:
			result.append(True)
		elif "Bf" in variables:
			result.append(False)
		else:
			result.append(None)
		if "Et"	in variables:
			result.append(True)
		elif "Ef" in variables:
			result.append(False)
		else:
			result.append(None)
		if "At"	in variables:
			result.append(True)
		elif "Af" in variables:
			result.append(False)
		else:
			result.append(None)
		if "Jt"	in variables:
			result.append(True)
		elif "Jf" in variables:
			result.append(False)
		else:
			result.append(None)
		if "Mt"	in variables:
			result.append(True)
		elif "Mf" in variables:
			result.append(False)
		else:
			result.append(None)
		#print result
		return result


from sys import argv

given = False
observations = []
query = []
for i in range(1,len(argv)):
	if argv[i] == "given":
		given = True
		continue
	query.append(argv[i])
	if given:
		observations.append(argv[i])

bnet = BayesianNetwork()

# print query
# print observations

if query:
	num = bnet.enumerate(bnet.generateValues(query))
	if observations:
		den = bnet.enumerate(bnet.generateValues(observations))
	else:
		den = 1
	# print num
	# print den
	print "The probability is : %.9f" % (num/den)
else:
	print "Invalid query string"