import time
import requests
import json

class gameMediator:
    def __init__(self) -> None:

        self.waiting = False
        self.move = None
        self.urlToGiveInstructions='http://127.0.0.1:5000/giveInstructions'
    def playerIsWaiting(self, player):
        self.waiting = True
        self.player = player
        while self.waiting:
            time.sleep(0.1)
        return self.move
    def sendConfirmedMoves(self,moves):
        print("sent moves",moves)
        data={"ans":"UpdatePiece","coords":moves}
        time.sleep(1)
        requests.post(self.urlToGiveInstructions, json = json.dumps(data))
    def askForPlayerMoves(self):
        data={"ans":"SendMoves"}
        time.sleep(1)
        requests.post(self.urlToGiveInstructions, json = json.dumps(data))
    def notifyGameOver(self):
        data={"ans":"GameOver"}
        time.sleep(1)
        requests.post(self.urlToGiveInstructions, json = json.dumps(data))
    
