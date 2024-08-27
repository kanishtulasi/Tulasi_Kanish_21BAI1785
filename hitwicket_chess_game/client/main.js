const boardElement = document.getElementById('board');
const turnElement = document.getElementById('turn');

const ws = new WebSocket('ws://localhost:8766');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received data:', data);  // Log received messages to check content
    if (data.type === 'state_update') {
        updateBoard(data.board);
        updateTurn(data.currentTurn);
    } else if (data.type === 'invalid_move') {
        alert('Invalid move, please try again.');
    }
};


function updateBoard(board) {
    boardElement.innerHTML = '';  // Clear the board
    for (let row = 0; row < board.length; row++) {
        for (let col = 0; col < board[row].length; col++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            const piece = board[row][col];
            if (piece) {
                cell.innerText = piece;
                cell.classList.add(piece.startsWith('A') ? 'playerA' : 'playerB');
                // Add event listener for selecting a piece
                cell.addEventListener('click', function() {
                    selectPiece(piece, row, col);  // Handle piece selection
                });
            }
            boardElement.appendChild(cell);
        }
    }
}

function updateTurn(currentTurn) {
    turnElement.innerText = `Current Turn: Player ${currentTurn}`;
}


function selectPiece(piece, row, col) {
    console.log(`Selected piece: ${piece} at (${row}, ${col})`);
    // Implement logic to show possible moves, send move to the server, etc.
}



ws.onopen = function() {
    console.log("WebSocket connection established");
    ws.send(JSON.stringify({type: 'init'}));
};

function makeMove(move) {
    ws.send(JSON.stringify({type: 'move', player: 'A', move}));
}

ws.onerror = function(error) {
    console.error("WebSocket error observed:", error);
};