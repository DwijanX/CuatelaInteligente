import playDecider
import board as bd
import boardValidator
import copy

inf=9999999999
class alphaBetaDecider(playDecider.playDecider):
    def __init__(self, player, Board: bd.Board, boardValidator: boardValidator.boardValidator):
        super().__init__(player, Board, boardValidator)

    def getBestPlay(self):
        self.visitedBoards=set()
        maxPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MaxPiece)
        minPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MinPiece)
        print("Utility: ", self.alphaBetaPrunning(self.board,-inf,inf,maxPiecesCoords,minPiecesCoords,0,self.player))
        if self.player==bd.MaxPiece:
            return self.bestMaxMovement
        else:
            return self.bestMinMovement

    
    def alphaBetaPrunning(self,currentBoard:bd.Board,alpha,beta,maxPiecesCoords,minPiecesCoords,depth,player):
        #if depth>900:
           # print(depth)
        terminalState,utility=self.checkIfSomeoneWonForSpecificBoard(currentBoard)
        if terminalState:
            return utility
        
        if player==bd.MaxPiece: 
            bestVal = -inf
            subBoards=self.getSubBoards(currentBoard,maxPiecesCoords,bd.MaxPiece)
            #if len(subBoards)==0:
             #   print("none")
            for subBoard,subCoords,newMovement in subBoards:
                value=self.alphaBetaPrunning(subBoard,alpha,beta,subCoords,minPiecesCoords,depth+1,bd.MinPiece)
                if depth==0 and bestVal<=value:
                    self.bestMaxMovement=newMovement
                bestVal=max(bestVal,value)
                alpha=max(alpha,bestVal)
                if alpha>=beta:
                    #print("hizo prunning")
                    break
            if (bestVal == -inf):
                return inf
            return bestVal
        else:
            bestVal = inf
            subBoards=self.getSubBoards(currentBoard,minPiecesCoords,bd.MinPiece)
            #if len(subBoards)==0:
              #  print("none")
            for subBoard,subCoords,newMovement in subBoards:
                value=self.alphaBetaPrunning(subBoard,alpha,beta,maxPiecesCoords,subCoords,depth+1,bd.MaxPiece)
                if depth==0 and bestVal>=value:
                    self.bestMinMovement=newMovement
                bestVal=min(bestVal,value)
                beta=min(beta,bestVal)
                if alpha>=beta:
                    print("hizo prunning")
                    break
            if (bestVal == inf):
                return -inf
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
                        pass
        
        return tablesAndCoords
