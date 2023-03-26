import board
import copy
invalidPlayer="Invalid Player"
cellIsUnavailable="Cell Is Unavailable"
selectedCellIsTooFar="selected Cell Is Too Far"
OutOfBoundaries="Out of Boundaries"
noOneWon="NoWon"
MaxWon="MaxWon"
MinWon="MinWon"

class boardValidator:
    def __init__(self,board:board.Board) -> None:
        self.board=board
        self.availableMovements=[(0,-1),(0,1),(1,0),(-1,0),(1,-1),(-1,-1),(-1,1),(1,1)]

    def validatePlay(self,typeOfPlayer,startCoords,nextCoords):
        dim=self.board.getDim()
        if(nextCoords[0]<0 or nextCoords[0]>=dim or nextCoords[1]<0 or nextCoords[1]>=dim):
            raise Exception(OutOfBoundaries)
        typeOfPiece=self.board.getPieceInCoords(startCoords)
        nextCell=self.board.getPieceInCoords(nextCoords)
        if typeOfPlayer!=typeOfPiece:
            raise Exception(invalidPlayer)
        if nextCell!=board.EmptyCell:
            raise Exception(cellIsUnavailable)
        xDir,yDir=nextCoords[0]-startCoords[0],nextCoords[1]-startCoords[1]
        
        for i in range(1,max(abs(xDir),abs(yDir))+1):
            mediumCoords=[startCoords[0],startCoords[1]]
            if abs(xDir)>0:
                mediumCoords[0]=int(mediumCoords[0]+(xDir/abs(xDir))*i)
            if abs(yDir)>0:
                mediumCoords[1]=int(mediumCoords[1]+(yDir/abs(yDir))*i)
            if self.board.getPieceInCoords(mediumCoords)!=board.EmptyCell:
                raise Exception("UnavailablePath")
        return True
    def validatePlayForSpecificBoard(self,typeOfPlayer,startCoords,nextCoords,SpecificBoard:board.Board):
        dim=SpecificBoard.getDim()
        if(nextCoords[0]<0 or nextCoords[0]>=dim or nextCoords[1]<0 or nextCoords[1]>=dim):
            raise Exception(OutOfBoundaries)
        typeOfPiece=SpecificBoard.getPieceInCoords(startCoords)
        nextCell=SpecificBoard.getPieceInCoords(nextCoords)
        if typeOfPlayer!=typeOfPiece:
            raise Exception(invalidPlayer)
        if nextCell!=board.EmptyCell:
            raise Exception(cellIsUnavailable)
        xDir,yDir=nextCoords[0]-startCoords[0],nextCoords[1]-startCoords[1]
        for i in range(1,max(abs(xDir),abs(yDir))+1):
            mediumCoords=[startCoords[0],startCoords[1]]
            if abs(xDir)>0:
                mediumCoords[0]=int(mediumCoords[0]+(xDir/abs(xDir))*i)
            if abs(yDir)>0:
                mediumCoords[1]=int(mediumCoords[1]+(yDir/abs(yDir))*i)
            if SpecificBoard.getPieceInCoords(mediumCoords)!=board.EmptyCell:
                raise Exception("UnavailablePath")
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