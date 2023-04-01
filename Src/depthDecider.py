import playDecider
import board as bd
import boardValidator
import copy
import board
import time
from collections import deque
inf=9999999999
class depthDecider(playDecider.playDecider):
    def __init__(self, player, Board: board.Board, boardValidator: boardValidator.boardValidator,heuristic,maxDepth):
        super().__init__(player, Board, boardValidator,heuristic)
        self.maxDepth=maxDepth
        self.maxMoves = deque()
        self.minMoves = deque()
        self.timeTook=0
        self.turns=0
        self.playsDone=[]
        self.pruningsPerTurn=[]
        self.boardsPerTurn=[]
    def superSaiyayin(self, moves, movementArray:deque):
        print(id(movementArray))
        movementArray.append(moves)
        if(len(movementArray)> 8):
            movementArray.popleft()
            if(self.maxDepth>2 and all(movementArray[index] == movementArray[0] for index in range(0,len(movementArray), 2))):
                print("Lowered Max depth")
                self.maxDepth -= 1
    def getReport(self):
        report={}
        report['turns']=self.turns
        report['timeTook']=self.timeTook
        report['playsDone']=self.playsDone
        report["pruningsPerTurn"]=self.pruningsPerTurn
        report["boardsPerTurn"]=self.boardsPerTurn
        return report
    def getBestPlay(self):
        self.prunings=0
        self.VisitedBoards=0
        self.visitedBoards=set()
        maxPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MaxPiece)
        minPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MinPiece)
        timerStart = time.perf_counter()
        utility=self.depth(self.board,-inf,inf,maxPiecesCoords,minPiecesCoords,0,self.player)
        timerEnd = time.perf_counter()

        self.turns+=1
        self.timeTook+=timerEnd-timerStart
        self.pruningsPerTurn.append(self.prunings)
        self.boardsPerTurn.append(self.VisitedBoards)

        print("Utility: ", utility)
        if self.player==bd.MaxPiece:
            self.superSaiyayin(self.bestMaxMovement,self.maxMoves)  
            self.playsDone.append(self.bestMaxMovement)
            return self.bestMaxMovement
        else:
            self.superSaiyayin(self.bestMinMovement,self.minMoves)  
            self.playsDone.append(self.bestMinMovement)  
            return self.bestMinMovement

            
    def depth(self,currentBoard:bd.Board,alpha,beta,maxPiecesCoords,minPiecesCoords,depth,player):
        self.VisitedBoards+=1
        terminalState,utility=self.checkIfSomeoneWonForSpecificBoard(currentBoard)
        newMovement=0
        if terminalState or depth==self.maxDepth:
            if utility>0:
                utility+=(self.maxDepth-depth)*100
            else:
                utility-=(self.maxDepth-depth)*100
            utility=int(utility)
            return utility
        
        if player==bd.MaxPiece: 
            bestVal = -inf
            subBoards=self.getSubBoards(currentBoard,maxPiecesCoords,bd.MaxPiece)
            for subBoard,subCoords,newMovement in subBoards:
                value=self.depth(subBoard,alpha,beta,subCoords,minPiecesCoords,depth+1,bd.MinPiece)
                if depth==0 and bestVal<=value:
                    self.bestMaxMovement=newMovement
                bestVal=max(bestVal,value)
                alpha=max(alpha,bestVal)
                if bestVal >= beta and bestVal!=-inf:
                    self.prunings+=1
                    break
            return bestVal
        else:
            bestVal = inf
            subBoards=self.getSubBoards(currentBoard,minPiecesCoords,bd.MinPiece)
            for subBoard,subCoords,newMovement in subBoards:
                value=self.depth(subBoard,alpha,beta,maxPiecesCoords,subCoords,depth+1,bd.MaxPiece)
                if depth==0 and bestVal>=value:
                    self.bestMinMovement=newMovement
                bestVal=min(bestVal,value)
                beta=min(beta,bestVal)
                if bestVal<=alpha and bestVal!=inf :
                    self.prunings+=1
                    break
            return bestVal
    
    def getSubBoards(self,board,coords,player):
        tablesAndCoords=[]
        for indexPiece in range(len(coords)):
            currentCoord=coords[indexPiece]
            for movementDirection in self.availableMovements:  
                for lengthMovement in range(3,0,-1):
                    try:
                        nextCoord=(currentCoord[0]+(movementDirection[0]*lengthMovement),currentCoord[1]+(movementDirection[1]*lengthMovement))
                        self.boardValidator.validatePlayForSpecificBoard(player,coords[indexPiece],nextCoord,board)
                        newBoard:bd.Board=copy.deepcopy(board)
                        newBoard.movePiece(currentCoord,nextCoord)
                        """hashBoard=newBoard.getHash()
                        if hashBoard not in self.visitedBoards:
                            self.visitedBoards.add(hashBoard)
                        else:
                            raise Exception("Already added board")"""
                        newCoords=copy.deepcopy(coords)
                        newCoords[indexPiece]=nextCoord
                        movement=(currentCoord,nextCoord)
                        tablesAndCoords.append((newBoard,newCoords,movement))
                        lengthMovement=0
                    except Exception as e:
                        pass
        return tablesAndCoords
