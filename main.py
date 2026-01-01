from __future__ import annotations

from typing import List, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

Player = str  # "X" or "O"


class MoveRequest(BaseModel):
    index: int


class ResetRequest(BaseModel):
    first_player: Optional[Player] = None


def check_winner_line(board: np.ndarray) -> tuple[Optional[Player], Optional[List[int]]]:
    for i in range(3):
        row = board[i, :]
        if row[0] is not None and np.all(row == row[0]):
            return row[0], [i * 3, i * 3 + 1, i * 3 + 2]
        col = board[:, i]
        if col[0] is not None and np.all(col == col[0]):
            return col[0], [i, i + 3, i + 6]

    diag = np.array([board[i, i] for i in range(3)], dtype=object)
    if diag[0] is not None and np.all(diag == diag[0]):
        return diag[0], [0, 4, 8]

    anti = np.array([board[i, 2 - i] for i in range(3)], dtype=object)
    if anti[0] is not None and np.all(anti == anti[0]):
        return anti[0], [2, 4, 6]

    return None, None


def is_full(board: np.ndarray) -> bool:
    return bool(np.all(board != None))


class TicTacToe:
    def __init__(self) -> None:
        self.first_player: Player = "X"
        self.reset(self.first_player)

    def reset(self, first_player: Optional[Player] = None) -> None:
        if first_player in {"X", "O"}:
            self.first_player = first_player
        self.board = np.full((3, 3), None, dtype=object)
        self.current_player = self.first_player
        self.winner: Optional[Player] = None
        self.winning_line: Optional[List[int]] = None
        self.moves = 0
        self.locked = False

    def swap_first(self) -> None:
        self.first_player = "O" if self.first_player == "X" else "X"
        self.reset(self.first_player)

    def move(self, index: int) -> None:
        if self.locked:
            raise HTTPException(status_code=400, detail="Game is over")
        if index < 0 or index > 8:
            raise HTTPException(status_code=400, detail="Invalid cell index")
        row, col = divmod(index, 3)
        if self.board[row, col] is not None:
            raise HTTPException(status_code=400, detail="Cell already taken")

        self.board[row, col] = self.current_player
        self.moves += 1

        winner, line = check_winner_line(self.board)
        if winner:
            self.winner = winner
            self.winning_line = line
            self.locked = True
            return

        if is_full(self.board):
            self.locked = True
            return

        self.current_player = "O" if self.current_player == "X" else "X"

    def status_message(self) -> str:
        if self.winner:
            return f"{self.winner} wins"
        if self.locked:
            return "Tie game"
        return f"{self.current_player} to move"

    def to_dict(self) -> dict:
        return {
            "board": self.board.tolist(),
            "current_player": self.current_player if not self.locked else None,
            "first_player": self.first_player,
            "winner": self.winner,
            "winning_line": self.winning_line,
            "locked": self.locked,
            "moves": self.moves,
            "status": "win" if self.winner else ("tie" if self.locked else "in_progress"),
            "status_message": self.status_message(),
        }


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = TicTacToe()


@app.get("/state")
def get_state() -> dict:
    return game.to_dict()


@app.post("/move")
def post_move(payload: MoveRequest) -> dict:
    game.move(payload.index)
    return game.to_dict()


@app.post("/reset")
def post_reset(payload: ResetRequest) -> dict:
    game.reset(payload.first_player)
    return game.to_dict()


@app.post("/swap-first")
def post_swap_first() -> dict:
    game.swap_first()
    return game.to_dict()
