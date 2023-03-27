from flask import Flask, render_template, request, jsonify,redirect,url_for

import json
import mediator
import game
import time

app=Flask(__name__)
gameStart = None
receivedNewInstructions=False
instructionsData=[]
#creates game.py environment after html was created
@app.route('/start_game')
def start_game():
    global gameStart
    print("game started")
    mediatorGame=mediator.gameMediator()
    gameStart=game.Game(mediatorGame)
    gameStart.createPlayers(True,True)
    gameStart.startGame()
    return 'Game started'

#moves every 2 moves, one for the position the other for place to move
@app.route('/move', methods=['POST'])
def move():
    # move sent from javascript
    data = request.data
    moves = json.loads(data)
    
    print("flask is working")
    print(moves)

    if gameStart is None:
        # game hasn't started yet
        print("entrando a juego")
        response = jsonify({'success': False, 'message': 'Game has not started yet'})
        return response
    
    # use those moves in python
    nums = int(moves['startCoords']), int(moves['nextCoords'])
    column = (nums[0] // 10) - 1
    row = (nums[0] % 10) - 1
    startCoords = (row, column)
    column = (nums[1] // 10) - 1
    row = (nums[1] % 10) - 1
    nextCoords = (row, column)
    gameStart.mediator.move = (startCoords,nextCoords)
    gameStart.mediator.waiting = False
    
    # return moves from python
    response = jsonify({'success': True})
    return response
"""
@app.route('/askForNewMoves', methods=['POST'])
def askForNewMoves():
    global receivedNewMoves
    global lastMoves
    print("asked")
    while receivedNewMoves==False:
        time.sleep(0.1)
    receivedNewMoves=False
    print("Ready to send")
    return json.dumps(lastMoves)"""
@app.route('/listenForInstructions', methods=['POST'])
def askForNewMoves():
    global receivedNewInstructions
    global instructionsData
    print("asked")
    while receivedNewInstructions==False:
        time.sleep(0.1)
    receivedNewInstructions=False
    return json.dumps(instructionsData)

@app.route('/giveInstructions', methods=['POST'])
def confirmMove():
    global receivedNewInstructions
    global instructionsData
    instructionsData=json.loads(request.get_json())
    receivedNewInstructions=True
    print("instructions given")
    return "OK"

@app.route('/')
def index():
    return render_template('index.html')

if __name__=='__main__':
    #app.run(debug=True) #add to debug HTML page easier
    app.run() #debugger doesnt work idkw

    