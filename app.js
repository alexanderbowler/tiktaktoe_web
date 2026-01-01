const board = document.getElementById("board");
const statusText = document.getElementById("status");
const turnsText = document.getElementById("turns");
const resetButton = document.getElementById("reset");
const swapButton = document.getElementById("swap");

const winningLines = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

let firstPlayer = "X";
let currentPlayer = firstPlayer;
let moves = 0;
let locked = false;
let cells = Array.from(board.querySelectorAll(".cell"));
let state = Array(9).fill("");

function updateStatus(message) {
  statusText.textContent = message;
}

function updateTurn() {
  turnsText.textContent = `Turn ${moves + 1}`;
}

function setCell(index, player) {
  state[index] = player;
  cells[index].textContent = player;
  cells[index].classList.add("filled");
  cells[index].setAttribute("aria-label", `Cell ${index + 1}, ${player}`);
}

function clearBoard() {
  state = Array(9).fill("");
  moves = 0;
  locked = false;
  cells.forEach((cell) => {
    cell.textContent = "";
    cell.classList.remove("filled", "win");
    cell.setAttribute("aria-label", "Empty cell");
  });
  currentPlayer = firstPlayer;
  updateStatus(`${currentPlayer} to move`);
  updateTurn();
}

function checkWinner() {
  for (const line of winningLines) {
    const [a, b, c] = line;
    if (state[a] && state[a] === state[b] && state[a] === state[c]) {
      return line;
    }
  }
  return null;
}

function handleMove(index) {
  if (locked || state[index]) {
    return;
  }

  setCell(index, currentPlayer);
  moves += 1;

  const winnerLine = checkWinner();
  if (winnerLine) {
    locked = true;
    winnerLine.forEach((idx) => cells[idx].classList.add("win"));
    updateStatus(`${currentPlayer} wins`);
    return;
  }

  if (moves === 9) {
    locked = true;
    updateStatus("Tie game");
    return;
  }

  currentPlayer = currentPlayer === "X" ? "O" : "X";
  updateStatus(`${currentPlayer} to move`);
  updateTurn();
}

cells.forEach((cell) => {
  cell.addEventListener("click", () => {
    const index = Number(cell.dataset.index);
    handleMove(index);
  });
});

resetButton.addEventListener("click", () => {
  clearBoard();
});

swapButton.addEventListener("click", () => {
  firstPlayer = firstPlayer === "X" ? "O" : "X";
  clearBoard();
});

clearBoard();
