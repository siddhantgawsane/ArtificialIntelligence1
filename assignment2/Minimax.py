from MaxConnect4Game import *
import copy

def possibleMoves(board):
	possibleMoves = []
	for col, colVal in enumerate(board[0]):
		if colVal == 0:
			possibleMoves.append(col)
	return possibleMoves
		
def result(oldGame, column):
	newGame = maxConnect4Game()

	try:
		newGame.nodeDepth = oldGame.nodeDepth + 1
	except AttributeError:
		newGame.nodeDepth = 1

	newGame.pieceCount = oldGame.pieceCount
	newGame.gameBoard = copy.deepcopy(oldGame.gameBoard)
	if not newGame.gameBoard[0][column]:
		for i in range(5, -1, -1):
			if not newGame.gameBoard[i][column]:
				newGame.gameBoard[i][column] = oldGame.currentTurn
				newGame.pieceCount += 1
				break
	if oldGame.currentTurn == 1:
		newGame.currentTurn = 2
	elif oldGame.currentTurn == 2:
		newGame.currentTurn = 1

	newGame.checkPieceCount()
	newGame.countScore()

	return newGame

class Minimax:
	def __init__(self, game, depth):
		self.currentTurn = game.currentTurn
		self.game = game
		self.maxDepth = int(depth)
		
	def makeDecision(self):

		minValues = []
		possMoves = possibleMoves(self.game.gameBoard)
		#self.game.nodeDepth = 0
		#v = self.maxVal(self.game,99999,-99999)
		#chosen = 0

		for move in possMoves:

			rslt = result(self.game,move)
			minValues.append( self.minVal(rslt,99999,-99999) )
			# if v == self.utility(rslt):
			# 	chosen = move
			# 	break

		chosen = possMoves[minValues.index( max( minValues ) )]
		return chosen

	def minVal(self, state, alpha, beta):
		if state.pieceCount == 42 or state.nodeDepth == self.maxDepth:
			return self.utility(state)
		v = 99999

		for move in possibleMoves(state.gameBoard):
			newState = result(state,move)

			v = min(v,self.maxVal( newState,alpha,beta ))
			if v <= alpha:
				return v
			beta = min(beta, v)
		return v
		
	def maxVal(self, state, alpha, beta):
		if state.pieceCount == 42 or state.nodeDepth == self.maxDepth:
			return self.utility(state)
		v = -99999

		for move in possibleMoves(state.gameBoard):
			newState = result(state,move)

			v = max(v,self.minVal( newState,alpha,beta ))
			if v >= beta:
				return v
			alpha = max(alpha, v)
		return v

	def utility(self,state):
		if self.currentTurn == 1:
			utility = state.player1Score * 2 - state.player2Score
		elif self.currentTurn == 2:
			utility = state.player2Score * 2 - state.player1Score

		return utility

