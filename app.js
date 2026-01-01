const board = document.getElementById("board");
const statusText = document.getElementById("status");
const resetButton = document.getElementById("reset");
const swapButton = document.getElementById("swap");
const modeButton = document.getElementById("mode");

const API_BASE = window.TTT_API_BASE || "";
const cells = Array.from(board.querySelectorAll(".cell"));

let locked = false;
let state = Array(9).fill("");
let gameMode = "two-player";

function updateStatus(message) {
  statusText.textContent = message;
}

function updateModeButton() {
  modeButton.textContent = gameMode === "two-player" ? "Mode: 2 Player" : "Mode: vs AI";
}

function requestAiMoveStub() {
  throw new Error("AI mode is not wired yet.");
}

function applyBoard(boardState) {
  const flat = boardState.flat();
  state = flat.map((cell) => cell || "");
  cells.forEach((cell, index) => {
    cell.textContent = state[index];
    cell.classList.toggle("filled", Boolean(state[index]));
    cell.classList.remove("win");
    if (state[index]) {
      cell.setAttribute("aria-label", `Cell ${index + 1}, ${state[index]}`);
    } else {
      cell.setAttribute("aria-label", "Empty cell");
    }
  });
}

function applyWinningLine(line) {
  if (!line) {
    return;
  }
  line.forEach((index) => {
    if (cells[index]) {
      cells[index].classList.add("win");
    }
  });
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    let detail = "Request failed";
    try {
      const data = await response.json();
      if (data && data.detail) {
        detail = data.detail;
      }
    } catch (error) {
      // Keep default message when JSON parse fails.
    }
    throw new Error(detail);
  }

  return response.json();
}

function render(stateData) {
  locked = stateData.locked;
  applyBoard(stateData.board);
  applyWinningLine(stateData.winning_line);
  updateStatus(stateData.status_message);
}

async function loadState() {
  try {
    const data = await apiRequest("/state");
    render(data);
  } catch (error) {
    updateStatus(error.message);
  }
}

async function handleMove(index) {
  if (locked || state[index]) {
    return;
  }
  try {
    const data = await apiRequest("/move", {
      method: "POST",
      body: JSON.stringify({ index }),
    });
    render(data);
    if (gameMode === "ai" && !data.locked) {
      requestAiMoveStub();
    }
  } catch (error) {
    updateStatus(error.message);
  }
}

cells.forEach((cell) => {
  cell.addEventListener("click", () => {
    const index = Number(cell.dataset.index);
    handleMove(index);
  });
});

resetButton.addEventListener("click", async () => {
  try {
    const data = await apiRequest("/reset", { method: "POST", body: "{}" });
    render(data);
  } catch (error) {
    updateStatus(error.message);
  }
});

swapButton.addEventListener("click", async () => {
  try {
    const data = await apiRequest("/swap-first", { method: "POST" });
    render(data);
  } catch (error) {
    updateStatus(error.message);
  }
});

modeButton.addEventListener("click", () => {
  gameMode = gameMode === "two-player" ? "ai" : "two-player";
  updateModeButton();
});

updateModeButton();
loadState();
