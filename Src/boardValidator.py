import board
invalidPlayer="IP"
cellIsUnavailable="CU"
noOneWon=0
MaxWon=1
MinWon=2

class boardValidator:
    def __init__(self,board:board.Board) -> None:
        self.board=board
    def validatePlay(self,typeOfPlayer,startCoords,nextCoords):
        typeOfPiece=self.board.getPieceInCoords(startCoords)
        nextCell=self.board.getPieceInCoords(nextCoords)
        if typeOfPlayer!=typeOfPiece:
            raise Exception(invalidPlayer)
        if nextCell!=board.EmptyCell:
            raise Exception(cellIsUnavailable)
        return True
    def checkIfSomeoneWon(self):
        pass
        