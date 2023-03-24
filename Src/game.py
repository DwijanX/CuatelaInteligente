import board
import player
import personPlayer
import botPlayer
import boardValidator
Max=1
Min=2
class Game():
    def __init__(self) -> None:
        self.board = board.Board()
        self.boardValidator=boardValidator(self.board)
    def createPlayers(self,Ai1=True,Ai2=True):
        if Ai1:
            self.player1=botPlayer()
        else:
            self.player1=personPlayer()
        if Ai2:
            self.player2=botPlayer()
        else:
            self.player2=personPlayer()
    def askForPlay(self,player:player.Player):
        startCoords,nextCoords=player.makePlay()
        try:
            self.boardValidator(player.getPlayerType(),startCoords,nextCoords)
            self.board.movePiece(startCoords,nextCoords)
        except Exception as Error:
            print(Error)
    def startGame(self):
        tourn=Max
        while(1):
            if tourn==Max:
                self.askForPlay(self.player1)
            else:
                self.askForPlay(self.player2)
            winCheckVar=self.boardValidator.checkIfSomeoneWon()
            if boardValidator.noOneWon!=winCheckVar:
                break
        if(winCheckVar==boardValidator.MaxWon):
            print("Player 1 won")
        else:
            print("Player 2 won")