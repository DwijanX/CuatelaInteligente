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
    def __init__(self, player, Board: bd.Board, boardValidator: boardValidator.boardValidator):
        super().__init__(player, Board, boardValidator)
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
    
    """
    def checkIfSomeoneWonForSpecificBoard(self,Board:board.Board):
        dim=self.board.getDim()
        MaxWinned,UtilityMax=self.__checkProcesss(board.MaxPiece,dim,Board)
        MinWinned,UtilityMin=self.__checkProcesss(board.MinPiece,dim,Board)
        Utility=UtilityMax-UtilityMin
        if MaxWinned or MinWinned:
            return True,Utility
        return False,Utility
    def __checkProcesss(self,player,dim,board:board.Board):
        Coords=board.getCoordsOfPiecesOfPlayer(player)
        winCond1,utilityAns1=self.__checkFirstWinCond(Coords,dim)
        winCond2,utilityAns2=self.__checkSecondWinCond(Coords,dim)
        winCond3,utilityAns3=self.__checkThirdWinCond(Coords,dim)
        winCond4,utilityAns4=self.__checkFourthWinCond(Coords,dim)
        won=winCond1 or winCond2 or winCond3 or winCond4
        #Utility=utilityAns1+utilityAns2+utilityAns3+utilityAns4
        Utility=max(utilityAns1,utilityAns2,utilityAns3,utilityAns4)
        return won,Utility
    def __getDistance(self,coord1,coord2):
        return max(abs(coord1[0]-coord2[0]),abs(coord1[1]-coord2[1]))
    def __checkFirstWinCond(self,playerCoords, dim):
        utility=0
        won=True
        coincidences=0
        for playerCoord in playerCoords:
            if playerCoord[0]==0 and (playerCoord[1]==0 or playerCoord[1]==dim-1) or playerCoord[0]==dim-1 and (playerCoord[1]==0 or playerCoord[1]==dim-1):
                utility+=1
                coincidences+=1
            else:
                won=False
        return won,utility
    def __checkSecondWinCond(self,playerCoords, dim):
        utility=0
        won=True
        arrayOrder=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        counter=0
        for first,second in arrayOrder:
            if self.__getDistance(playerCoords[first],playerCoords[second])!=1:
                won=False
            else:
                if utility<4:
                    utility+=1
                counter+=10
        return won,utility
    def __checkThirdWinCond(self,playerCoords, dim): ##aligned in rows
        utility=0
        won=True
        counter=0
        for i in range(dim):
            if i+1==dim:
                break
            if playerCoords[i][0]!=playerCoords[i+1][0] or playerCoords[i][1]+1!=playerCoords[i+1][1]:
                won=False
            else:
                utility+=1
                counter+=10
        return won,utility
    def __checkFourthWinCond(self,playerCoords, dim): ##aligned in columns
        utility=0
        won=True
        counter=0
        for i in range(dim):
            if i+1==dim:
                break
            if playerCoords[i][0]+1!=playerCoords[i+1][0] or playerCoords[i][1]!=playerCoords[i+1][1]:
                won=False
            else:
                utility+=1
                counter+=10
        return won,utility
        """