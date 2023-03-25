import board
import player
import personPlayer as pp
import botPlayer as bp
import boardValidator as bv
import mediator
import time

Max=1
Min=2
class Game():
    def __init__(self, mediator:mediator.gameMediator) -> None:
        self.board = board.Board()
        self.boardValidator=bv.boardValidator(self.board)
        self.mediator = mediator
        self.turn = Max
    def createPlayers(self,Ai1=True,Ai2=True):
        if Ai1:
            self.player1=bp.BotPlayer()
        else:
            self.player1=pp.PersonPlayer(Max, self.mediator)
        if Ai2:
            self.player2=bp.BotPlayer()
        else:
            self.player2=pp.PersonPlayer(Min, self.mediator)
    def __askForPlay(self,player:player.Player):
        while(1):
            moves = player.makePlay()
            startCoords = moves[0]
            nextCoords = moves[1]
            print(startCoords,nextCoords)
            try:
                self.boardValidator.validatePlay(player.getPlayerType(),startCoords,nextCoords)
                self.board.movePiece(startCoords,nextCoords)
                print("movida hecha")
                break
            except Exception as Error:
                time.sleep(1)
                print(Error,"try again")
        return moves
            
    def startGame(self):
        while(1):
            self.board.printBoardConsole()
            if self.turn==Max:
                moves=self.__askForPlay(self.player1)
                self.turn=Min
            else:
                moves=self.__askForPlay(self.player2)
                self.turn = Max
            print("saliendo del turno")
            self.mediator.sendConfirmedMoves(moves)
            winCheckVar=self.boardValidator.checkIfSomeoneWon()
            if bv.noOneWon!=winCheckVar:
                break
        if(winCheckVar==bv.MaxWon):
            print("Player 1 won")
        else:
            print("Player 2 won")

#si los descomento se inicializa el juego antes del html por lo que no hay respuesta
#game_mediator = mediator.playerWaitingForAnswer()
#game=Game(game_mediator)
#game.createPlayers(False,False)
#game.startGame()