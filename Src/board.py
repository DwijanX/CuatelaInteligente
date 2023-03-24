EmptyCell=0
BlackPieceCell=1
WhitePieceCell=2
class Board:
    def __init__(self,dim=4) -> None:
        self.dim=dim
        self.__initializeBoard()
        pass
    def __fillPieces(self):
        for i in range(self.dim):
            self.board[i][i]=BlackPieceCell
            self.board[i][self.dim-1-i]=WhitePieceCell

    def __initializeBoard(self):
        self.board=[[0 for i in range(self.dim)] for j in range(self.dim)]
        self.__fillPieces()
    def printBoard(self):
        print(self.board)

test=Board()
test.printBoard()