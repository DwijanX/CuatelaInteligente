import time

class playerWaitingForAnswer:
    def __init__(self) -> None:
        self.waiting = False
        self.move = None

    def playerIsWaiting(self, player):
        self.waiting = True
        self.player = player
        while self.waiting:
            time.sleep(0.1)
        return self.move
