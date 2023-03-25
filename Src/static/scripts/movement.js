const columnLetters = ['A', 'B', 'C', 'D'];

let previousSquare = null;
let selectedSquare = null;
let squareToMove = null;

let movement = 'actual';

const squares = document.querySelectorAll('.square');
const startButton = document.querySelector('#startButton');

function startGame(){
    console.log("inicializando");
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/start_game');
    xhr.send();
}


function moveSquare(fileIndex,rankIndex) {
    if (selectedSquare === null) {
      selectedSquare = fileIndex.toString() + rankIndex.toString();
    } else {
      squareToMove = fileIndex.toString() + rankIndex.toString();
    }
  }
function updateBoard(Coords)
{
  console.log(Coords)
  originCoords=Coords[0]
  nextCoords=Coords[1]
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

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/move');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    console.log('Moves sent successfully.');
                }
            }
        };
        xhr.send(JSON.stringify(moves));
        selectedSquare = null;
        squareToMove = null;
        receiveMoves()
    }
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
      const rank = file.parentElement;
      const fileIndex = Array.prototype.indexOf.call(rank.children, file) + 1;
      const rankIndex = Array.prototype.indexOf.call(file.children, square) + 1;
  
    console.log(movement)
    if (movement === 'actual'){
        const selected = document.getElementById('selected');
        selected.innerHTML = `Selected square: ${columnLetters[fileIndex - 1]}${rankIndex}`;
        movement = 'next'
    }
    else{
        const moveTo = document.getElementById('moveTo');
        moveTo.innerHTML = `wishes square: ${columnLetters[fileIndex - 1]}${rankIndex}`;
        movement = 'actual'
    }

      

      previousSquare = square;
      console.log(square)
      moveSquare(fileIndex, rankIndex);
      sendMoves();
      
    });
  });


