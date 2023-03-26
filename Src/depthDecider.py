import playDecider
import board as bd
import boardValidator
import copy
inf=9999999999
class depthDecider(playDecider.playDecider):
    
    def getBestPlay(self):
        self.visitedBoards=set()
        maxPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MaxPiece)
        minPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MinPiece)
        print(self.player)
        print("Utility: ", self.depth(self.board,-inf,inf,maxPiecesCoords,minPiecesCoords,0,self.player))
        if self.player==bd.MaxPiece:
            return self.bestMaxMovement
        else:
            return self.bestMinMovement

    
    def depth(self,currentBoard:bd.Board,alpha,beta,maxPiecesCoords,minPiecesCoords,depth,player):
        terminalState,utility=self.checkIfSomeoneWonForSpecificBoard(currentBoard)
        newMovement=0
        if terminalState and depth==1:
            print("terminal1")
        if terminalState or depth==4:
            utility=int(utility)
            return utility
        
        if player==bd.MaxPiece: 
            bestVal = -inf
            subBoards=self.getSubBoards(currentBoard,maxPiecesCoords,bd.MaxPiece)
            for subBoard,subCoords,newMovement in subBoards:
                value=self.depth(subBoard,alpha,beta,subCoords,minPiecesCoords,depth+1,bd.MinPiece)
                if depth==0 and bestVal<=value:
                    self.bestMinMovement=newMovement
                bestVal=max(bestVal,value)
                alpha=max(alpha,bestVal)
                if bestVal >= beta and bestVal!=-inf:
                    break
            if bestVal==-inf:
                return inf
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
                    break
            if bestVal==inf :
                return -inf
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
                        #hashBoard=newBoard.getHash()
                        #if hashBoard not in self.visitedBoards:
                        #    self.visitedBoards.add(hashBoard)
                        #else:
                        #    raise Exception("Already added board")
                        newCoords=copy.deepcopy(coords)
                        newCoords[indexPiece]=nextCoord
                        movement=(currentCoord,nextCoord)
                        tablesAndCoords.append((newBoard,newCoords,movement))
                    except Exception as e:
                        pass
        return tablesAndCoords
