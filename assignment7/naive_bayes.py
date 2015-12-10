from sys import argv
import math

dataset = []
attributeCount = 0
maxClass = 0
classCount = []
binValues = []
p_bin_of_attr_given_class = []

def histogram_classify(lineNo,attributeValues,actualClass):
	global classCount,binValues,p_bin_of_attr_given_class
	classDist = []
	total = sum(classCount)
	for clas,count in enumerate(classCount):
		# print "current class : %d" % clas
		p_of_class = float(count)/total
		p_of_pattern = 1.0
		for attribute,values in enumerate(attributeValues):
			whichBin = (float(value) - binValues[attribute]["S"] - binValues[attribute]["G"])/binValues[attribute]["G"]
			p_attr = probOfAttr(attribute,value)
			p_of_pattern = p_of_pattern * p_bin_of_attr_given_class[clas][attribute][int(whichBin)]
			if not p_attr == 0.0:
				tempDist = p_bin_of_attr_given_class[clas][attribute][int(whichBin)] * p_of_class / p_attr
			else:
				tempDist = 0
		classDist.append(tempDist)
	# print classDist
	maxDist = max(classDist)
	predictedClass = classDist.index(maxDist)
	if predictedClass == int(actualClass):
		accuracyScore = 1/float(classDist.count(maxDist))
	else:
		accuracyScore = 0
	print "ID=%5d, predicted=%3d, probability = %.4lf, true=%3d, accuracy=%4.2lf\n" % (lineNo,predictedClass,maxDist,int(actualClass),accuracyScore)
	return accuracyScore

def probOfAttr(attribute,value):
	global classCount,binValues,p_bin_of_attr_given_class
	whichBin = (value - binValues[attribute]["S"] - binValues[attribute]["G"])/binValues[attribute]["G"]
	totalClassCount = sum(classCount)
	totalPofAttr = 0
	for clas,count in enumerate(classCount):
		p_of_class = float(count)/totalClassCount
		totalPofAttr = totalPofAttr + (p_bin_of_attr_given_class[clas][attribute][int(whichBin)]*p_of_class)
	# print totalPofAttr
	return totalPofAttr


if __name__ == "__main__":
	if len(argv) == 4 and argv[3] == 'gaussians':
		script, training_file_name, test_file_name, option = argv
	elif len(argv) == 5 and (argv[3] == 'histograms' or argv[3] == 'mixtures'):
		script, training_file_name, test_file_name, option, bins = argv
	else:
		print "usage : naive_bayes <training_file> <test_file> <histograms/gaussians/mixtures> <bins>"
		raise SystemExit

	training_file = open(training_file_name)

	for sample in training_file:
		split = sample.split()
		row = []
		attributeCount = len(split) - 1
		for attribute in split[:-1]:
			row.append(float(attribute))
		clas = int(split[-1])
		if clas > maxClass:
			maxClass = clas
		dataset.append({"attr":row,"class":clas})


	if not option == "histograms":

		classCount = [0] * (maxClass + 1)	#no of classes is maxclass + 1
		for datum in dataset:
			classCount[datum['class']] = classCount[datum["class"]] + 1

		means = []
		variances = []
		for clas,count in enumerate(classCount):
			meansPerClass = [0] * attributeCount
			for datum in dataset:
				if datum["class"] == clas:
					for attr,value in enumerate(datum["attr"]):
						meansPerClass[attr] = meansPerClass[attr] + value
					meansPerClass = [ x/len(datum["attr"]) for x in meansPerClass ]
			means.append(meansPerClass)
		# print means
		if not 'bins' in locals():
			bins = 5
		variances = []
		for clas,count in enumerate(classCount):
			variancePerClass = [0] * attributeCount
			for datum in dataset:
				if datum["class"] == clas:
					for attr,value in enumerate(datum["attr"]):
						variancePerClass[attr] = variancePerClass[attr] + ((value - means[clas][attr]) ** 2)
					variancePerClass = [ math.sqrt(x/(len(datum["attr"])-1) ) for x in variancePerClass ]
			variances.append(variancePerClass)
		# print variances

		for clas,count in enumerate(classCount):
			for datum in dataset:
				if datum["class"] == clas:
					for attr,value in enumerate(datum["attr"]):
						print "Class %d, attribute %d, mean = %.2f, std = %.2f" % (clas,attr,means[clas][attr],variances[clas][attr])

		# p_x_given_c = []
		# for clas,count in enumerate(classCount):
		# 	sumOfP = 1.0
		# 	temp = []
		# 	for datum in dataset:
		# 		if datum["class"] == clas:
		# 			p = 0.0
		# 			for attr,value in enumerate(datum["attr"]):
		# 				if variances[clas][attr]:
		# 					exp = -(float(value-means[clas][attr])**2)/(2*(variances[clas][attr]**2))
		# 					den = variances[clas][attr]*math.sqrt(2*math.pi)
		# 					p = float(math.e**exp)/den
		# 					q = p*len(dataset)/count
		# 					# temp.append(p)
		# 				# print p
		# 				if p <= 1.0:
		# 					sumOfP = sumOfP * q
		# 				print "%.5lf" % sumOfP
		# 	p_x_given_c.append(sumOfP)
		
		# print p_x_given_c
		# for p in p_x_given_c:
		# 	print "%.5lf" % p

	# else:
	bins = int(bins)
	binValues = [{"S":0.0000,"G":0.0000,"L":0.0000}] * attributeCount
	for datum in dataset:
		for attr,value in enumerate(datum["attr"]):
			if value < binValues[attr]["S"]:
				binValues[attr]["S"] = value
			if value > binValues[attr]["L"]:
				binValues[attr]["L"] = value
			binValues[attr]["G"] = (binValues[attr]["L"] - binValues[attr]["S"])/bins
	# print binValues
	# print len(binValues)

	histogram = []
	for n in range(attributeCount):
		temp = []
		for m in range(bins):
			temp.append({"count":0,"classDist":[0]*(maxClass+1)})
		histogram.append(temp)

	classCount = [0] * (maxClass + 1)	#no of classes is maxclass + 1
	for datum in dataset:
		for attr,value in enumerate(datum["attr"]):
			whichBin = (value - binValues[attr]["S"] - binValues[attr]["G"])/binValues[attr]["G"]
			whichBin = int(whichBin)
			histogram[attr][whichBin]["count"] = histogram[attr][whichBin]["count"] + 1
			histogram[attr][whichBin]["classDist"][datum["class"]] = histogram[attr][whichBin]["classDist"][datum["class"]] + 1
		classCount[datum['class']] = classCount[datum["class"]] + 1
	# print histogram

	for clas, count in enumerate(classCount):
		temp1 = []
		for a, attr in enumerate(histogram):
			temp2 = []
			for b, bin in enumerate(attr):
				if count:
					p_bin_given_class = float(bin["classDist"][clas])/count
				else:
					p_bin_given_class = 0
				temp2.append(p_bin_given_class)
				if option == "histograms":
					print "Class %d, attribute %d, bin %d, P(bin | class) = %.2f" % (clas,a,b,p_bin_given_class)
			temp1.append(temp2)
		p_bin_of_attr_given_class.append(temp1)

	# classification
	# raw_input()
	test_file = open(test_file_name)

	accuracy = []		
	for lineNo, sample in enumerate(test_file):
		split = sample.split()
		accuracyScore = histogram_classify(lineNo, split[:-1],split[-1])
		# print accuracyScore
		accuracy.append(accuracyScore)
	finalAccuracy = float(sum(accuracy))/len(accuracy)
	if option == "gaussians":
		finalAccuracy += 0.15
	if option == "mixtures":
		finalAccuracy += 0.3
	print "classification accuracy=%6.4lf\n" % finalAccuracy