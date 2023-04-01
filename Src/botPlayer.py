import player 
import playDecider
class BotPlayer(player.Player):
    def __init__(self, type,playDecider:playDecider.playDecider) -> None:
        super().__init__(type)
        self.playDecider=playDecider
    def makePlay(self):
        return self.playDecider.getBestPlay()
        pass
    def getReport(self):
        return self.playDecider.getReport()