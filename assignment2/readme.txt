
ASSIGNMENT 2 : Depth limited minimax with alpha-beta pruning
NAME: Siddhant Gawsane
UTA ID: 1001231597
LANGUAGE: Python
CODE STRUCTURE:
	The class minimax performs the decision making. Contains methods makeDecision() which returns minimax's decision, maxVal() which performs maximizing operations, minVal() which perfoms minimizing operations, and utility() which returns the utility that needs to be maximized or minimized.
	result() calculates the new state after a particular move
	possibleMoves() returns the moves that are possible on a state

COMPILATION AND EXECUTION:
	To run the code, execute maxconnect4.py with standard python compilation commands (works on omega)

	For interactive mode, pass the following arguments:
		python maxconnect4.py interactive [input_file] [computer-next/human-next] [depth]

	For one-move mode, pass the following arguments:
		python maxconnect4.py one-move [input_file] [output_file] [depth]	

TOURNAMENT:
	Yes, the program has depth limted and alpha-beta implemented and can be entered into the tournament