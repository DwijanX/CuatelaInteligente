
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
const modeSelection = document.querySelector('#modeSelection');
const colorSelection = document.querySelector('#colorSelection');
const depthInput = document.querySelector('#depthInput');


async function sendSelection(){
  const selectedColor = colorSelection.value;
  const selectedMode = modeSelection.value;
  const selectedDepth = depthInput.value;
  console.log(selectedColor,selectedMode,selectedDepth)

  settings = JSON.stringify({
    color: selectedColor,
    mode: selectedMode,
    depth: selectedDepth
})
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/settings');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        if (response.success) {
          console.log('settings changed successfully');
          resolve();
        } else {
          reject();
        }
      }
    };
    console.log("ready to send settings");
    xhr.send(settings);
    
  });
}

async function startGame(){
  console.log("inicializando");
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/start_game');
  xhr.send();
  await listener()
}


function squareToMoveInString(fileIndex,rowIndex) {
    if (selectedSquare === null) {
      selectedSquare = fileIndex.toString() + rowIndex.toString();
    } else {
      squareToMove = fileIndex.toString() + rowIndex.toString();
    }
  }

function setReceivedCoords(Coords)
{
  console.log("coordenadas recibidas:")
  console.log(Coords)
  serverOriginCoords=Coords[0]
  serverNextCoords=Coords[1]
}



function sendMoves(){
    if (selectedSquare != null && squareToMove != null) {
        var moves = {
            'startCoords': selectedSquare,
            'nextCoords': squareToMove
        };
        console.log("moves to send",moves)

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
          console.log("ready to send moves");
          xhr.send(JSON.stringify(moves));
          
        });
    }
}

function movePiece() {
  var originCoords = [serverOriginCoords[1], serverOriginCoords[0]]; //server gives YX values
  var nextCoords = [serverNextCoords[1], serverNextCoords[0]]; //server gives YX values
  var originPiece = document.querySelector('[data-position="' + originCoords[0] + '-' + originCoords[1] + '"]');
  var NextPiece = document.querySelector('[data-position="' + nextCoords[0] + '-' + nextCoords[1] + '"]');
  console.log(originPiece)
  console.log(NextPiece)
  var temp = originPiece.innerHTML;
  originPiece.innerHTML = NextPiece.innerHTML;
  NextPiece.innerHTML = temp;
}

function updateTurn() {
  var turnText = document.getElementById("turn");
  if(turn == 1){
    turnText.innerHTML = "White Turn";
    turn = 2;
  }
  else{
    turnText.innerHTML = "Black Turn";
    turn = 2;
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

async function listener()
{
  let data
  let GameOver=false
  while (GameOver) {
    await fetch('http://127.0.0.1:5000/listenForInstructions', {
        method: 'POST'
      })
      .then((response) => response.json()) 
      .then((data) => {
        data=data
      });
    if (data["ans"]=="UpdatePiece"){
      setReceivedCoords(data["coords"]);
      movePiece();
      updateTurn();
    }
    if (data["ans"]=="SendMoves"){
      //should unlock buttons to select piece, otherwise they'd be locked
      //could show a message asking the user to select move
      alert("Select your move")
      await sendMoves()
    }
    if(data["ans"]=="GameOver")
    {
      GameOver=true
      alert("GameOver")
    }
    turn = 1;
  }
}



async function listener()
{
  let receivedData
  let GameOver=false
  console.log("entered Listener")
  while (GameOver==false) {
    await fetch('http://127.0.0.1:5000/listenForInstructions', {
        method: 'POST'
      })
      .then((response) => response.json()) 
      .then((data) => {
        console.log(data)
        receivedData=data
      });
    console.log("passed request")
    if (receivedData["ans"]=="UpdatePiece"){
      selectedSquare = null;
      squareToMove = null;
      setReceivedCoords(receivedData["coords"]);
      movePiece();
      updateTurn();
    }
    if (receivedData["ans"]=="SendMoves"){
      //could show a message asking the user to select move
      alert("Select your move")
      //should unlock buttons to select piece, otherwise they ought to be locked
      
    }
    if(receivedData["ans"]=="GameOver")
    {
      GameOver=true
      alert("GameOver")
    }
    console.log("waiting");
  }
  
}


startButton.addEventListener("click", function() {
  sendSelection();
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
        sendMoves()
    }
    previousSquare = square;
    console.log(square)
    });
  });


