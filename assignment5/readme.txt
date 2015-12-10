ASSIGNMENT 3 : Probability
NAME: Siddhant Gawsane
UTA ID: 1001231597
LANGUAGE: Python
CODE STRUCTURE:
	Actions are broken down into methods which are logically grouped into classes

COMPILATION AND EXECUTION:
	Part1:
	python compute_a_posteriori.py [observations]
	for example, python compute_a_posteriori.py CLLCCCLLL
	The output is written to a file called "result.txt"

	Part3:
	python learn_test_data.py [data-file]
	for example, python learn_test_data.py training_data.txt

	Part4:
	python bnet.py [query1] [query2] [query3] ... given [observation1] [observation2] [observation3] ...
	for example python bnet.py Bt Af given Mf
	the 'given' argument is optional, its absence will mark all inputs as queries
	for example python bnet.py Bt Af Mf Jt Et