import board
import boardValidator
class playDecider():
    def __init__(self,player,Board:board.Board,boardValidator:boardValidator.boardValidator):
        self.board=Board
        self.player=player
        self.boardValidator=boardValidator
        self.visitedBoards=set()
        self.prunings=0
        #self.availableMovements=[(0,-1),(0,1),(1,0),(-1,0),(1,-1),(-1,-1),(-1,1),(1,1)]
        #self.availableMovements=[(1,-1),(-1,-1),(-1,1),(1,1),(0,-1),(0,1),(1,0),(-1,0)]
        #self.availableMovements=[(-1,-1),(-1,1),(1,-1),(1,1),(0,1),(-1,0),(0,-1),(1,0)]
        #NW,SW,NE,SE,S,W,N,E
        #self.availableMovements=[(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        self.availableMovements= [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    def getBestPlay(self):
        pass
    def checkIfSomeoneWonForSpecificBoard(self,Board:board.Board):
        dim=self.board.getDim()
        MaxWinned,UtilityMax=self.__checkProcesss(board.MaxPiece,dim,Board)
        MinWinned,UtilityMin=self.__checkProcesss(board.MinPiece,dim,Board)
        Utility=UtilityMax-UtilityMin
        if MaxWinned or MinWinned:
            return True,Utility
        return False,Utility
    def __checkProcesss(self,player,dim,board:board.Board):
        Coords=board.getCoordsOfPiecesOfPlayer(player)
        winCond1,utilityAns1=self.__checkFirstWinCond(Coords,dim)
        winCond2,utilityAns2=self.__checkSecondWinCond(Coords,dim)
        winCond3,utilityAns3=self.__checkThirdWinCond(Coords,dim)
        winCond4,utilityAns4=self.__checkFourthWinCond(Coords,dim)
        won=winCond1 or winCond2 or winCond3 or winCond4
        Utility=utilityAns1+utilityAns2+utilityAns3+utilityAns4
        #Utility=max(utilityAns1,utilityAns2,utilityAns3,utilityAns4)
        if won:
            Utility=Utility*20
        return won,Utility
    def __getDistance(self,coord1,coord2):
        return max(abs(coord1[0]-coord2[0]),abs(coord1[1]-coord2[1]))
    def __checkFirstWinCond(self,playerCoords, dim):
        utility=0
        won=True
        coincidences=0
        for playerCoord in playerCoords:
            if playerCoord[0]==0 and (playerCoord[1]==0 or playerCoord[1]==dim-1) or playerCoord[0]==dim-1 and (playerCoord[1]==0 or playerCoord[1]==dim-1):
                utility+=1*coincidences
                coincidences+=1
            else:
                won=False
        return won,utility
    def __checkSecondWinCond(self,playerCoords, dim):
        utility=0
        won=True
        arrayOrder=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        counter=0
        for first,second in arrayOrder:
            if self.__getDistance(playerCoords[first],playerCoords[second])!=1:
                won=False
            else:
                utility+=1+counter
                counter+=10
        return won,utility
    def __checkThirdWinCond(self,playerCoords, dim): ##aligned in rows
        utility=0
        won=True
        counter=0
        for i in range(dim):
            if i+1==dim:
                break
            if playerCoords[i][0]!=playerCoords[i+1][0] or playerCoords[i][1]+1!=playerCoords[i+1][1]:
                won=False
            else:
                utility+=i+counter
                counter+=10
        return won,utility
    def __checkFourthWinCond(self,playerCoords, dim): ##aligned in columns
        utility=0
        won=True
        counter=0
        for i in range(dim):
            if i+1==dim:
                break
            if playerCoords[i][0]+1!=playerCoords[i+1][0] or playerCoords[i][1]!=playerCoords[i+1][1]:
                won=False
            else:
                utility+=1+counter
                counter+=10
        return won,utility