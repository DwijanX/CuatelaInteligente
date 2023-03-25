import player
import mediator 

class PersonPlayer(player.Player):

    def makePlay(self):
        move = self.mediator.playerIsWaiting(self)
        return move

    def __init__(self, type, mediator:mediator.playerWaitingForAnswer) -> None:
        super().__init__(type)
        self.mediator = mediator
        