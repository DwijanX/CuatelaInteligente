import board
invalidPlayer="Invalid Player"
cellIsUnavailable="Cell Is Unavailable"
selectedCellIsTooFar="selected Cell Is Too Far"
noOneWon="NoWon"
MaxWon="MaxWon"
MinWon="MinWon"

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
        if abs(startCoords[0]-nextCoords[0])>1 or abs(startCoords[1]-nextCoords[1])>1:
            raise Exception(selectedCellIsTooFar)
        return True
    
        
    def checkProcesss(self,player,dim):
        Coords=self.board.getCoordsOfPiecesOfPlayer(player)
        if self.__checkFirstWinCond(Coords,dim):
            return True
        if self.__checkSecondWinCond(Coords,dim):
            return True
        if self.__checkThirdWinCond(Coords,dim):
            return True
        if self.__checkFourthWinCond(Coords,dim):
            return True
        return False
    def checkIfSomeoneWon(self):
        dim=self.board.getDim()
        if self.checkProcesss(board.MaxPiece,dim):
            return MaxWon
        if self.checkProcesss(board.MinPiece,dim):
            return MinWon
        return noOneWon
        

    def __getDistance(self,coord1,coord2):
        return max(abs(coord1[0]-coord2[0]),abs(coord1[1]-coord2[1]))
    def __checkFirstWinCond(self,playerCoords, dim):
        if playerCoords[0][0]!=0 or playerCoords[0][1]!=0:
            return False
        if playerCoords[1][0]!=0 or playerCoords[1][1]!=dim-1:
            return False
        if playerCoords[2][0]!=dim-1 or playerCoords[2][1]!=0:
            return False
        if playerCoords[3][0]!=dim-1 or playerCoords[3][1]!=dim-1:
            return False
        return True
    def __checkSecondWinCond(self,playerCoords, dim):
        arrayOrder=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        for first,second in arrayOrder:
            if self.__getDistance(playerCoords[first],playerCoords[second])!=1:
                return False
        return True
    def __checkThirdWinCond(self,playerCoords, dim): ##aligned in rows
        for i in range(dim):
            if i+1==dim:
                break
            if playerCoords[i][0]!=playerCoords[i+1][0] or playerCoords[i][1]+1!=playerCoords[i+1][1]:
                return False
        return True
    def __checkFourthWinCond(self,playerCoords, dim): ##aligned in columns
        for i in range(dim):
            if i+1==dim:
                break
            if playerCoords[i][0]+1!=playerCoords[i+1][0] or playerCoords[i][1]!=playerCoords[i+1][1]:
                return False
        return True