class Path(object):
	def __init__(self,line):
		for index, word in enumerate(line.split()):
			if (index is 0):
				self.source = word
			elif (index is 1):
				self.destination = word
			elif (index is 2):
				self.cost = int(word)

class Graph(object):
	def __init__(self,filename):
		txt = open(filename)
		self.paths = []
		for line in txt:
			if("END OF INPUT" in line):
				break;
			self.paths.append(Path(line))
		txt.close()
		
	def search(self,key):
		matchedPaths = []
		for path in self.paths:
	#		print(node)
			if key in path.source:
				matchedPaths.append(path)
			if key in path.destination:
				matchedPaths.append(path)
		for path in matchedPaths:
			self.paths.remove(path)
		return matchedPaths


class TreeNode(object):
	def __init__(self,city,parent,children,depth,pathCost):
		self.city = city
		self.parent = parent
		self.children = children
		self.depth = depth
		self.pathCost = pathCost
		
	def equals(self,cityName):
		return self.city == cityName
		
class Fringe(object):
	def __init__(self,graph):
		self.graph = graph
		self.queue = []
		
	def add(self,node):
		self.queue.append(node)
		self.queue.sort(key=lambda node: node.pathCost)		#uniform cost search
		
	def remove(self):
#		for node in self.queue:
#			print node.city
		return self.queue.pop(0)
		
	def isEmpty(self):
		return not self.queue
	

class Tree(object):
	def __init__(self,graph,source,destination):
		fringe = Fringe(graph)
		self.origin = TreeNode(source,None,[],0,0)
		fringe.add(self.origin)
		complete = False
		while not fringe.isEmpty():
			currentNode = fringe.remove()
			if currentNode.equals(destination):
				print "distance: %d kms\nroute:" % (currentNode.pathCost)
				while currentNode.parent is not None:
					currentNode.parent.children.append(currentNode)
					currentNode = currentNode.parent
				complete = True
				break
			traversiblePaths = graph.search(currentNode.city)
			for path in traversiblePaths:
				if currentNode.equals(path.source):
					newNode = TreeNode( path.destination, currentNode, [], path.cost, currentNode.pathCost+path.cost )
		 		else:
					newNode = TreeNode( path.source, currentNode, [], path.cost, currentNode.pathCost+path.cost )
				fringe.add( newNode )
		if not complete:
			print "distance: infinity\nroute:\nnone"
		else:
			currentNode = self.origin
			while currentNode.children:
				print "%s to %s, %d kms" % (currentNode.city,currentNode.children[0].city,currentNode.children[0].depth)
				currentNode = currentNode.children[0]


from sys import argv

script,filename,source,destination = argv

graph = Graph(filename)
tree = Tree(graph,source,destination)
