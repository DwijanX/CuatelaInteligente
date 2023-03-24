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
    def movePiece(self,startCoords,nextCoords):
        self.board[nextCoords[0]][nextCoords[1]]=self.board[startCoords[0]][startCoords[1]]
        self.board[startCoords[0]][startCoords[1]]=EmptyCell
    def getPieceInCoords(self,coords):
        return self.board[coords[0]][coords[1]]
