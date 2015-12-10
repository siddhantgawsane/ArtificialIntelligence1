
ASSIGNMENT 1 : Uninformed Search
NAME: Siddhant Gawsane
UTA ID: 1001231597
LANGUAGE: Python
CODE STRUCTURE:
	The program uses uniform cost search to find the shortest path between 2 nodes. Since UCS is being used, the first path to reach the destination is naturally the shortest path
	
	There are 5 classes:
1. Path: Class of a bidirectional path
2. Graph: Class of the graph like structure in the problem. Though this is not actually a graph, since there are some nodes which are not connected, the structure is closest to a graph. Has search() method which searches for a path containing a certain city name
3. TreeNode: Class of a node in the tree. Has equals() method to ease equality check
4. Tree: Class for the list of interconnected nodes that are traversed to reach the destination. Takes a graph object on instantiation and converts it to a tree using UCS.
5. Fringe: The fringe helps to convert the graph to a tree. Has add(), remove() and isEmpty() methods
A tree contains many treeNodes, a graph contains many paths

COMPILATION AND EXECUTION:
	To run the code, open a terminal at the path of the folder, and compile find_route.py using the default python compiler (tested on omega's default compiler)
	The program takes 3 command line arguments:
	1. the name of the file containing the path information. Should be in the format:
			City_A City_B cost1
			City_B City_C cost2
			END OF INPUT
		This file must be at the same location as find_route.py
	2. the name of the source city
	3. the name of the destination city
	
	Ex: python find_route.py input1.txt Munich Berlin
