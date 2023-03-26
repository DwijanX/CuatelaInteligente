const columnLetters = ['A', 'B', 'C', 'D'];

let previousSquare = null;
let selectedSquare = null;
let squareToMove = null;

let movement = 'actual';

let serverOriginCoords
let serverNextCoords
let turn = 1

const squares = document.querySelectorAll('.square');
const startButton = document.querySelector('#startButton');

function startGame(){
    console.log("inicializando");
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/start_game');
    xhr.send();
}


function squareToMoveInString(fileIndex,rowIndex) {
    if (selectedSquare === null) {
      selectedSquare = fileIndex.toString() + rowIndex.toString();
    } else {
      squareToMove = fileIndex.toString() + rowIndex.toString();
    }
  }

function updateBoard(Coords)
{
  console.log("coordenadas recibidas:")
  console.log(Coords)
  serverOriginCoords=Coords[0]
  serverNextCoords=Coords[1]
}
  async function receiveMoves()
  {
    await fetch('http://127.0.0.1:5000/askForNewMoves', {
      method: 'POST'
    })
    .then((response) => response.json()) 
    .then((data) => {
      updateBoard(data)
    });
  }

function sendMoves(){
    if (selectedSquare != null && squareToMove != null) {
        var moves = {
            'startCoords': selectedSquare,
            'nextCoords': squareToMove
        };

        return new Promise((resolve, reject) => {
          var xhr = new XMLHttpRequest();
          xhr.open('POST', '/move');
          xhr.setRequestHeader('Content-Type', 'application/json');
          xhr.onload = function() {
            if (xhr.status === 200) {
              var response = JSON.parse(xhr.responseText);
              if (response.success) {
                console.log('Moves sent successfully');
                resolve();
              } else {
                reject();
              }
            }
          };
          xhr.send(JSON.stringify(moves));
          
        });
    }
}

function movePiece() {
  var originCoords = [serverOriginCoords[1], serverOriginCoords[0]]; //server gives YX values
  var nextCoords = [serverNextCoords[1], serverNextCoords[0]]; //server gives YX values
  var piece1 = document.querySelector('[data-position="' + originCoords[0] + '-' + originCoords[1] + '"]');
  var piece2 = document.querySelector('[data-position="' + nextCoords[0] + '-' + nextCoords[1] + '"]');
  console.log(piece1)
  console.log(piece2)
  piece1.setAttribute('data-position', nextCoords[0] + '-' + nextCoords[1]);
  piece2.setAttribute('data-position', originCoords[0] + '-' + originCoords[1]);
  var temp = piece1.innerHTML;
  piece1.innerHTML = piece2.innerHTML;
  piece2.innerHTML = temp;
  console.log(piece1)
  console.log(piece2)
}

function updateTurn() {
  var turnText = document.getElementById("turn");
  if(turn == 1){
    turnText.innerHTML = "Black Turn";
    turn = 2;
  }
  else{
    turnText.innerHTML = "White Turn";
    turn = 1;
  }
}

async function getMovesFromServer() {
  await sendMoves();
  selectedSquare = null;
  squareToMove = null;
  await receiveMoves();
  console.log("moving piece:")
  console.log(serverOriginCoords)
  console.log(serverNextCoords)
  movePiece();
  updateTurn();
}




startButton.addEventListener("click", function() {
  startGame();
});

squares.forEach(square => {
    square.addEventListener('click', function() {
      if (previousSquare !== null) {
        previousSquare.style.backgroundColor = '';
      }
      square.style.backgroundColor = 'blue';
  
      const file = square.parentElement;
      const row = file.parentElement;
      const fileIndex = Array.prototype.indexOf.call(row.children, file) + 1; 
      const rowIndex = Array.prototype.indexOf.call(file.children, square) + 1;
  
    console.log(movement)
    if (movement === 'actual'){
        const selected = document.getElementById('selected');
        selected.innerHTML = `Selected square: ${columnLetters[fileIndex - 1]}${rowIndex}`;
        movement = 'next'
        squareToMoveInString(fileIndex, rowIndex);
    }
    else{
        const moveTo = document.getElementById('moveTo');
        moveTo.innerHTML = `wishes square: ${columnLetters[fileIndex - 1]}${rowIndex}`;
        movement = 'actual'
        squareToMoveInString(fileIndex, rowIndex);
        getMovesFromServer();
    }
    previousSquare = square;
    console.log(square)
    });
  });


