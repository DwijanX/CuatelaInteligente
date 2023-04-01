import playDecider
import board as bd
import boardValidator
import copy
import board
import queue
import sys
import time
import pickle
import random as rd
sys. setrecursionlimit(3000)
inf=9999999999
class alphaBetaDecider(playDecider.playDecider):
    def __init__(self, player, Board: bd.Board, boardValidator: boardValidator.boardValidator,heuristic):
        super().__init__(player, Board, boardValidator,heuristic)
        self.randomMovements=True

    def getBestPlay(self):
        self.timerStart = time.perf_counter()
        self.terminalStatesFound=0
        self.visitedBoards=set()
        maxPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MaxPiece)
        minPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MinPiece)
        copiedBoard=copy.deepcopy(self.board) 
        print("Utility: ", self.alphaBetaPrunning(self.board,-inf,inf,maxPiecesCoords,minPiecesCoords,0,self.player))
        if self.player==bd.MaxPiece:
            return self.bestMaxMovement
        else:
            return self.bestMinMovement

    
    def alphaBetaPrunning(self,currentBoard:bd.Board,alpha,beta,maxPiecesCoords,minPiecesCoords,depth,player):
        terminalState,utility=self.checkIfSomeoneWonForSpecificBoard(currentBoard)
        if terminalState:
            self.terminalStatesFound+=1
            return utility
        if depth>2500:
            self.generateReport(depth)
        if player==bd.MaxPiece: 
            bestVal = -inf
            subBoards=self.getSubBoards(currentBoard,maxPiecesCoords,bd.MaxPiece,self.randomMovements)
            for subBoard,subCoords,newMovement in subBoards:
                value=self.alphaBetaPrunning(subBoard,alpha,beta,subCoords,minPiecesCoords,depth+1,bd.MinPiece)
                if depth==0 and bestVal<=value:
                    self.bestMaxMovement=newMovement
                bestVal=max(bestVal,value)
                alpha=max(alpha,bestVal)
                if alpha>=beta:
                    self.prunings+=1
                    break
            if (bestVal == -inf):
                return inf
            return bestVal
        else:
            bestVal = inf
            subBoards=self.getSubBoards(currentBoard,minPiecesCoords,bd.MinPiece,self.randomMovements)
            for subBoard,subCoords,newMovement in subBoards:
                value=self.alphaBetaPrunning(subBoard,alpha,beta,maxPiecesCoords,subCoords,depth+1,bd.MaxPiece)
                if depth==0 and bestVal>=value:
                    self.bestMinMovement=newMovement
                bestVal=min(bestVal,value)
                beta=min(beta,bestVal)
                if alpha>=beta:
                    self.prunings+=1
                    break
            if (bestVal == inf):
                return -inf
            return bestVal

    def generateReport(self,depth):
        
        self.timerEnd = time.perf_counter()
        timeTook=self.timerEnd-self.timerStart
        AnswerObject={}
        AnswerObject["orderOfActions"]=self.availableMovements
        AnswerObject["terminalStatesFound"]=self.terminalStatesFound
        AnswerObject["prunings"]=self.prunings
        AnswerObject["depthReached"]=depth
        AnswerObject["time"]=timeTook
        print(AnswerObject)
        file_name = 'Run8AlphaBeta.pickle'
        with open(file_name, 'wb') as file:
            pickle.dump(AnswerObject, file)
            print(f'Object successfully saved to "{file_name}"')
        pass
    def getSubBoards(self,board,coords,player,random=False):
        movements=copy.deepcopy(self.availableMovements)
        if random: 
            rd.shuffle(movements)
        tablesAndCoords=[]
        for indexPiece in range(len(coords)):
            currentCoord=coords[indexPiece]
            for movementDirection in movements:  
                for lengthMovement in range(3,0,-1):
                    try:
                        nextCoord=(currentCoord[0]+(movementDirection[0]*lengthMovement),currentCoord[1]+(movementDirection[1]*lengthMovement))
                        self.boardValidator.validatePlayForSpecificBoard(player,coords[indexPiece],nextCoord,board)
                        
                        newBoard:bd.Board=copy.deepcopy(board)
                        newBoard.movePiece(currentCoord,nextCoord)
                        hashBoard=newBoard.getHash()
                        if hashBoard not in self.visitedBoards:
                            self.visitedBoards.add(hashBoard)
                        else:
                            raise Exception("Already added board")
                        newCoords=copy.deepcopy(coords)
                        newCoords[indexPiece]=nextCoord
                        movement=(currentCoord,nextCoord)
                        tablesAndCoords.append((newBoard,newCoords,movement))
                        lengthMovement=0
                    except Exception as e:
                        continue
        
        return tablesAndCoords
    