import board as bd
import copy
invalidPlayer="Invalid Player"
cellIsUnavailable="Cell Is Unavailable"
selectedCellIsTooFar="selected Cell Is Too Far"
OutOfBoundaries="Out of Boundaries"
UnavailablePath="Unavailable Path"
PathSelectedIsNotTheMax="Path Selected Is Not The Max"
noOneWon="NoWon"
MaxWon="MaxWon"
MinWon="MinWon"

class boardValidator:
    def __init__(self,board:bd.Board) -> None:
        self.board=board
        self.availableMovements=[(0,-1),(0,1),(1,0),(-1,0),(1,-1),(-1,-1),(-1,1),(1,1)]

    def validatePlay(self,typeOfPlayer,startCoords,nextCoords):
        return self.validatePlayForSpecificBoard(typeOfPlayer,startCoords,nextCoords,self.board)
    def __validateIfCoordIsOutOfBoundaries(self,nextCoords,dim):
        return nextCoords[0]<0 or nextCoords[0]>=dim or nextCoords[1]<0 or nextCoords[1]>=dim
    
    def __verifyIfPathIsValid(self,board,startCoords,nextCoords,dim):
        xDir,yDir=nextCoords[0]-startCoords[0],nextCoords[1]-startCoords[1]
        CellsToMove=max(abs(xDir),abs(yDir))
        mediumCoords=[startCoords[0],startCoords[1]]
        for i in range(1,4):
            if abs(xDir)>0:
                mediumCoords[0]=int(mediumCoords[0]+(xDir/abs(xDir)))
            if abs(yDir)>0:
                mediumCoords[1]=int(mediumCoords[1]+(yDir/abs(yDir)))
            if i< CellsToMove:
                if board.getPieceInCoords(mediumCoords)!=bd.EmptyCell:
                    raise Exception(UnavailablePath)
            elif i>CellsToMove:
                if self.__validateIfCoordIsOutOfBoundaries(mediumCoords,dim):
                    break
                if board.getPieceInCoords(mediumCoords)==bd.EmptyCell:
                    raise Exception(PathSelectedIsNotTheMax)

    def validatePlayForSpecificBoard(self,typeOfPlayer,startCoords,nextCoords,SpecificBoard:bd.Board):
        dim=SpecificBoard.getDim()
        if(self.__validateIfCoordIsOutOfBoundaries(startCoords,dim)):
            raise Exception(OutOfBoundaries)
        if(self.__validateIfCoordIsOutOfBoundaries(nextCoords,dim)):
            raise Exception(OutOfBoundaries)
        typeOfPiece=SpecificBoard.getPieceInCoords(startCoords)
        nextCell=SpecificBoard.getPieceInCoords(nextCoords)
        if typeOfPlayer!=typeOfPiece:
            raise Exception(invalidPlayer)
        if nextCell!=bd.EmptyCell:
            raise Exception(cellIsUnavailable)
        self.__verifyIfPathIsValid(SpecificBoard,startCoords,nextCoords,dim)
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
        if self.checkProcesss(bd.MaxPiece,dim):
            return MaxWon
        if self.checkProcesss(bd.MinPiece,dim):
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