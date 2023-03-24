EmptyCell=0
MaxPiece=1
MinPiece=2
class Board:
    def __init__(self,dim=4) -> None:
        self.dim=dim
        self.__initializeBoard()
        pass
    def __fillPieces(self):
        for i in range(self.dim):
            self.board[i][i]=MaxPiece
            self.board[i][self.dim-1-i]=MinPiece

    def __initializeBoard(self):
        self.board=[[0 for i in range(self.dim)] for j in range(self.dim)]
        self.__fillPieces()
    def getBoard(self):
        return self.board
    def getDim(self):
        return self.dim
    def movePiece(self,startCoords,nextCoords):
        self.board[nextCoords[0]][nextCoords[1]]=self.board[startCoords[0]][startCoords[1]]
        self.board[startCoords[0]][startCoords[1]]=EmptyCell
        print("Moved")
    def getPieceInCoords(self,coords):
        return self.board[coords[0]][coords[1]]
    def printBoardConsole(self):
        for r in self.board:
            print(r)
    def getCoordsOfPiecesOfPlayer(self,player):
        playerCoords=[]
        coordsFound=0
        for r in range(self.dim):
            for c in range(self.dim):
                if self.board[r][c]==player:
                    playerCoords.append((r,c))
                    coordsFound+=1
                    if coordsFound==self.dim:
                        break
        return playerCoords