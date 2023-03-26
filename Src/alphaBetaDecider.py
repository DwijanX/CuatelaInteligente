import playDecider
import board as bd
import boardValidator
import copy

class alphaBetaDecider(playDecider.playDecider):
    
    def getBestPlay(self):
        self.visitedBoards=set()
        maxPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MaxPiece)
        minPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MinPiece)
        print("Utility: ", self.alphaBetaPrunning(self.board,float('-inf'),float('inf'),maxPiecesCoords,minPiecesCoords,0,self.player))
        if self.player==bd.MaxPiece:
            return self.bestMaxMovement
        else:
            return self.bestMinMovement

    
    def alphaBetaPrunning(self,currentBoard:bd.Board,alpha,beta,maxPiecesCoords,minPiecesCoords,depth,player):
        if depth>900:
            print(depth)
        terminalState,utility=self.boardValidator.checkIfSomeoneWonForSpecificBoard(currentBoard)
        if terminalState:
            return utility
        if player==bd.MaxPiece: 
            bestVal = float("-inf")
            subBoards=self.getSubBoards(currentBoard,maxPiecesCoords,bd.MaxPiece)
            if len(subBoards)==0:
                print("none")
            for subBoard,subCoords,newMovement in subBoards:
                bestVal=max(bestVal,self.alphaBetaPrunning(subBoard,alpha,beta,subCoords,minPiecesCoords,depth+1,bd.MinPiece))
                alpha=max(alpha,bestVal)
                if beta<=bestVal:
                    break
            return bestVal
        else:
            bestVal = float("inf")
            for subBoard,subCoords,newMovement in self.getSubBoards(currentBoard,minPiecesCoords,bd.MinPiece):
                bestVal=min(bestVal,self.alphaBetaPrunning(subBoard,alpha,beta,maxPiecesCoords,subCoords,depth+1,bd.MaxPiece))
                beta=min(beta,bestVal)
                if bestVal<=alpha:
                    break
            return bestVal
    def getSubBoards(self,board,coords,player):
        tablesAndCoords=[]
        for indexPiece in range(len(coords)):
            currentCoord=coords[indexPiece]
            for movementDirection in self.availableMovements:  
                for lengthMovement in range(1,4):
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
                    except Exception as e:
                        pass
        return tablesAndCoords
