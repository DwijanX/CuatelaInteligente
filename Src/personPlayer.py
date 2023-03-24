import player 
class PersonPlayer(player.Player):

    def makePlay(self):
        print("Playing as ",self.type)
        print("Selecting Piece")
        x1=int(input("which X coord u wanna move"))
        y1=int(input("which Y coord u wanna move"))
        print("Selecting Objective")
        x2=int(input("which x coord is the objective"))
        y2=int(input("which Y coord is the objective"))
        return (x1,y1),(x2,y2)

        