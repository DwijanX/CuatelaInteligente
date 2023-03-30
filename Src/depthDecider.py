import playDecider
import board as bd
import boardValidator
import copy
import board
inf=9999999999
class depthDecider(playDecider.playDecider):
    def __init__(self, player, Board: board.Board, boardValidator: boardValidator.boardValidator,maxDepth):
        super().__init__(player, Board, boardValidator)
        self.maxDepth=maxDepth
        self.maxMoves = []
        self.minMoves = []
    
    def superSaiyayin(self, moves, movementArray):
        movementArray.append(moves)
        if(len(movementArray)>= 8):
            if(all(movementArray[index] == movementArray[0] for index in range(0,len(movementArray), 2))):
                print("saiyayin mode activated")
                self.maxDepth -= 1
            movementArray = []    

    def getBestPlay(self):
        self.visitedBoards=set()
        maxPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MaxPiece)
        minPiecesCoords=self.board.getCoordsOfPiecesOfPlayer(bd.MinPiece)
        print(self.player)
        print("Utility: ", self.depth(self.board,-inf,inf,maxPiecesCoords,minPiecesCoords,0,self.player))
        if self.player==bd.MaxPiece:
            self.superSaiyayin(self.bestMaxMovement,self.maxMoves)
            return self.bestMaxMovement

        else:
            self.superSaiyayin(self.bestMinMovement,self.minMoves)  
            return self.bestMinMovement

    
    def depth(self,currentBoard:bd.Board,alpha,beta,maxPiecesCoords,minPiecesCoords,depth,player):
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
                        newCoords=copy.deepcopy(coords)
                        newCoords[indexPiece]=nextCoord
                        movement=(currentCoord,nextCoord)
                        tablesAndCoords.append((newBoard,newCoords,movement))
                        lengthMovement=0
                    except Exception as e:
                        pass
        return tablesAndCoords
