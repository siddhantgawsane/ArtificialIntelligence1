import math
import random

dataset = []
attributeCount = 0
maxClass = 0

class Node(object):
	def __init__(self,treeId,nodeId,attribute,threshold,gain):
		self.treeId = treeId
		self.nodeId = nodeId
		self.featureId = attribute
		self.threshold = threshold
		self.gain = gain
		self.leftChild = None
		self.rightChild = None
	
	def eval(self,sample):
		if sample[self.featureId] < self.threshold:
			if isinstance(self.leftChild,Node):
				return self.leftChild.eval(sample)
			else:
				return self.leftChild
		else:
			if isinstance(self.rightChild,Node):
				return self.rightChild.eval(sample)
			else:
				return self.rightChild

	def printTree(self):
		queue = []
		queue.append(self)
		while queue:
			currentNode = queue.pop(0)
			print "tree=%2d, node=%3d, feature=%2d, thr=%6.2f, gain=%f\n" % (currentNode.treeId, currentNode.nodeId, currentNode.featureId, currentNode.threshold, currentNode.gain)
			if isinstance(currentNode.leftChild,Node):
				queue.append(currentNode.leftChild)
			# else:
			# 	print self.leftChild
			if isinstance(currentNode.rightChild,Node):
				queue.append(currentNode.rightChild)
			# else:
			# 	print self.rightChild

def choose_attribute(examples,attributes):
	max_gain = -1
	best_attribute = -1
	best_threshold = -1

	for attribute in attributes:
		# print "attribute : %d" % attribute
		L,M = getMinMax(examples,attribute)
		for K in range(1,51):
			threshold = L + (K * (M-L)/51)
			gain = information_gain(examples,attribute,threshold)
			if gain > max_gain:
				max_gain = gain
				best_attribute = attribute
				best_threshold = threshold
		# print "max_gain : %f" % max_gain

	return best_attribute,best_threshold,max_gain

def choose_random_attribute(examples,attributes):

	max_gain = -1
	best_attribute = -1
	best_threshold = -1

	attribute = random.choice(attributes)
	L,M = getMinMax(examples,attribute)
	for K in range(1,51):
		threshold = L + (K * (M-L)/51)
		gain = information_gain(examples,attribute,threshold)
		if gain > max_gain:
			max_gain = gain
			best_attribute = attribute
			best_threshold = threshold
	return best_attribute,best_threshold,max_gain


def information_gain(examples,attribute,threshold):
	initial_dist = getClassCountOf(examples)
	left,right = splitBy(examples,attribute,threshold)
	left_dist = getClassCountOf(left)
	right_dist = getClassCountOf(right)

	left_weight = float(sum(left_dist))/sum(initial_dist)
	right_weight = float(sum(right_dist))/sum(initial_dist)

	info_gain = entropy(initial_dist) - (left_weight * entropy(left_dist)) - (right_weight * entropy(right_dist))

	return info_gain


def entropy(distribution):

	ent = 0
	total = sum(distribution)
	for dist in distribution:
		if total:
			temp = float(dist)/total
			if not temp == 0.0000:
				ent = ent - (temp * math.log(temp,2))
	return ent

def splitBy(examples,attribute,threshold):
	left = []
	right = []

	for example in examples:
		if example["attr"][attribute] < threshold:
			left.append(example)
		else:
			right.append(example)
	return left,right

def getClassCountOf(examples):
	global maxClass
	classCount = [0] * (maxClass + 1)
	for ex in examples:
		classCount[ex['class']] = classCount[ex["class"]] + 1
	return classCount

def distribution(examples):
	classCount = getClassCountOf(examples)
	distribution = []
	length = len(classCount)
	for clas in classCount:
		distribution.append(float(clas)/length)
	return distribution

def getMinMax(examples,attribute):
	Min = 99999.99
	Max = 0.0
	for example in examples:
		if example["attr"][attribute] < Min:
			Min = example["attr"][attribute]
		if example["attr"][attribute] > Max:
			Max = example["attr"][attribute]
	return Min,Max

def onlyOneClassIn(examples):
	count = getClassCountOf(examples)
	numOfZeros = 0
	for c in count:
		if c == 0:
			numOfZeros = numOfZeros + 1
	return numOfZeros == len(count) - 1

def DTL(treeId,examples,attributes,default,nodeId,options):
	# print len(examples)
	if not examples:
		return default
	elif onlyOneClassIn(examples):
		return distribution(examples)
	else:
		if options == "optimized":
			best_attribute,best_threshold,max_gain = choose_attribute(examples,attributes)
		else:
			best_attribute,best_threshold,max_gain = choose_random_attribute(examples,attributes)
		tree = Node(treeId,nodeId,best_attribute,best_threshold,max_gain)
		# tree.printNode()

		examples_left,examples_right = splitBy(examples,best_attribute,best_threshold)

		if len(examples_left) > 50:	#pruning
			leftsubtree = DTL(treeId,examples_left,attributes,distribution(examples),2*nodeId,options)
		else:
			leftsubtree = distribution(examples_left)

		if len(examples_right) > 50:
			rightsubtree = DTL(treeId,examples_right,attributes,distribution(examples),(2*nodeId)+1,options)
		else:
			rightsubtree = distribution(examples_right)

		tree.leftChild = leftsubtree
		tree.rightChild = rightsubtree
		return tree

def getExamplesWithAttribute(examples,attribute,isLess,threshold):
	new_examples = []
	for example in examples:
		if isLess and example[attribute] < threshold:
			new_examples.append(example)
		elif not isLess and example[attribute] >= threshold:
			new_examples.append(example)
	return new_examples

def evaluate(forest,sample):
	results = []
	for tree in forest:
		results.append(tree.eval(sample))

	avg = results[0]
	iterResults = iter(results)
	iterResults.next()
	for result in iterResults:
		for i,dist in enumerate(result):
			avg[i] = avg[i] + dist

	for val in avg:
		val = val/len(results)
	return avg

from sys import argv

if __name__ == "__main__":
	if len(argv) > 3 and (argv[3] == 'optimized' or argv[3] == 'randomized' or argv[3][:6] == 'forest'):
		script, training_file_name, test_file_name, options = argv
	else:
		print "usage dtree <training_file> <test_file> <optimized/randomized/forestN>"
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
	
	# kill = raw_input("Read complete. Continue building forest? (hit 'n' to exit) :")
	# if kill and kill.lower() == "n":
	# 	raise SystemExit

	forest_length = 1
	if options[:6] == 'forest':
		forest_length = int(options[6:])

	forest = []
	for i in range(0,forest_length):
		forest.append(DTL(i,dataset,range(0,attributeCount),distribution(dataset),1,options))
	
	for tree in forest:
		tree.printTree()

	kill = raw_input("Forest built. Continue testing samples? (hit 'n' to exit) :")
	if kill and kill.lower() == "n":
		raise SystemExit

	test_file = open(test_file_name)

	accuracies = []
	for i,sample in enumerate(test_file):
		split = sample.split()
		row = []
		for attribute in split[:-1]:
			row.append(float(attribute))

		prob_dist = evaluate(forest,row)
		prob_dist_unique = list(set(prob_dist))
		predicted_class = prob_dist.index(max(prob_dist_unique))
		if predicted_class == int(split[-1]):
			ties = len(prob_dist) - len(prob_dist_unique)
			if ties:
				accuracy = 1/float(ties)
			else:
				accuracy = 1
		else:
			accuracy = 0
		accuracies.append(accuracy)
		print "ID=%5d, predicted=%3d, true=%3d, accuracy=%4.2lf\n" % (i, predicted_class, int(split[-1]), accuracy)

	print "classification accuracy=%6.4lf\n" % (sum(accuracies)/len(accuracies))

