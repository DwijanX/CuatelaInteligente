import time
import requests
import json

class gameMediator:
    def __init__(self) -> None:
        self.waiting = False
        self.move = None
        self.urlToConfirmMove='http://127.0.0.1:5000/sendBoard'
    def playerIsWaiting(self, player):
        self.waiting = True
        self.player = player
        while self.waiting:
            time.sleep(0.1)
        return self.move
    def sendConfirmedMoves(self,moves):
        requests.post(self.urlToConfirmMove, json = json.dumps({'moves': moves}))
    
