import player
import mediator 

class PersonPlayer(player.Player):
    def __init__(self, type, mediator:mediator.gameMediator,useUI=True) -> None:
        super().__init__(type)
        self.mediator = mediator
        self.useUI = useUI
        
    def __askForUIPlay(self):
        self.mediator.askForPlayerMoves()
        move = self.mediator.playerIsWaiting(self)
        return move
    def __askForConsolePlay(self):
        print("Playing as ",self.type) 
        print("Selecting Piece")
        x1=int(input("which X coord u wanna move"))
        y1=int(input("which Y coord u wanna move"))
        print("Selecting Objective")
        x2=int(input("which x coord is the objective"))
        y2=int(input("which Y coord is the objective"))
        return ((x1,y1),(x2,y2))
    
    def makePlay(self):
        if self.useUI:
            return self.__askForUIPlay()
        return self.__askForConsolePlay()


        