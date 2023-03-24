import board
import player
import personPlayer as pp
import botPlayer as bp
import boardValidator as bv
Max=1
Min=2
class Game():
    def __init__(self) -> None:
        self.board = board.Board()
        self.boardValidator=bv.boardValidator(self.board)
    def createPlayers(self,Ai1=True,Ai2=True):
        if Ai1:
            self.player1=bp.BotPlayer()
        else:
            self.player1=pp.PersonPlayer(Max)
        if Ai2:
            self.player2=bp.BotPlayer()
        else:
            self.player2=pp.PersonPlayer(Min)
    def __askForPlay(self,player:player.Player):
        while(1):
            try:
                startCoords,nextCoords=player.makePlay()
                self.boardValidator.validatePlay(player.getPlayerType(),startCoords,nextCoords)
                self.board.movePiece(startCoords,nextCoords)
                break
            except Exception as Error:
                print(Error,"try again")
            
    def startGame(self):
        tourn=Max
        while(1):
            self.board.printBoardConsole()
            if tourn==Max:
                self.__askForPlay(self.player1)
                tourn=Min
            else:
                self.__askForPlay(self.player2)
                tourn=Max
            winCheckVar=self.boardValidator.checkIfSomeoneWon()
            if bv.noOneWon!=winCheckVar:
                break
        if(winCheckVar==bv.MaxWon):
            print("Player 1 won")
        else:
            print("Player 2 won")

game=Game()
game.createPlayers(False,False)
game.startGame()