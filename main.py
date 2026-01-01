from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

Player = str  # "X" or "O"
Cell = Optional[Player]


def check_winner(grid: List[List[Cell]]) -> Optional[Player]:
    lines = []
    lines.extend(grid)  # rows
    lines.extend([[grid[r][c] for r in range(3)] for c in range(3)])  # cols
    lines.append([grid[i][i] for i in range(3)])
    lines.append([grid[i][2 - i] for i in range(3)])
    for line in lines:
        if line[0] is not None and line.count(line[0]) == 3:
            return line[0]
    return None


def is_full(grid: List[List[Cell]]) -> bool:
    return all(cell is not None for row in grid for cell in row)


@dataclass
class UltimateTicTacToe:
    boards: List[List[List[List[Cell]]]]
    winners: List[List[Optional[Player]]]
    current: Player = "X"
    active_board: Optional[Tuple[int, int]] = None  # (br, bc) or None for any

    @classmethod
    def new(cls) -> "UltimateTicTacToe":
        boards = [[[ [None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        winners = [[None for _ in range(3)] for _ in range(3)]
        return cls(boards=boards, winners=winners)

    def place(self, br: int, bc: int, r: int, c: int) -> bool:
        if self.winners[br][bc] is not None:
            return False
        if self.boards[br][bc][r][c] is not None:
            return False
        self.boards[br][bc][r][c] = self.current

        winner = check_winner(self.boards[br][bc])
        if winner:
            self.winners[br][bc] = winner
        elif is_full(self.boards[br][bc]):
            self.winners[br][bc] = "T"  # tie

        next_active = (r, c)
        if self.winners[next_active[0]][next_active[1]] is None:
            self.active_board = next_active
        else:
            self.active_board = None

        self.current = "O" if self.current == "X" else "X"
        return True

    def global_winner(self) -> Optional[Player]:
        grid = [[None if w == "T" else w for w in row] for row in self.winners]
        return check_winner(grid)

    def is_over(self) -> bool:
        return self.global_winner() is not None or all(
            w is not None for row in self.winners for w in row
        )

    def render(self) -> str:
        cell_w = 3
        row_sep = " + ".join(["-" * cell_w] * 3)
        between_boards = " || "
        between_big = "===="
        small_w = len(row_sep)

        lines = []
        for br in range(3):
            for r in range(3):
                parts = []
                for bc in range(3):
                    row = self.boards[br][bc][r]
                    cells = [f" {cell if cell is not None else '.'} " for cell in row]
                    parts.append(" | ".join(cells))
                lines.append(between_boards.join(parts))
                if r < 2:
                    lines.append(between_boards.join([row_sep] * 3))
            if br < 2:
                lines.append(between_big.join(["=" * small_w] * 3))
        return "\n".join(lines)


def parse_move(text: str, active: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    tokens = text.strip().split()
    if not tokens:
        return None
    if tokens[0].lower() in {"q", "quit", "exit"}:
        return None

    nums = []
    for t in tokens:
        if not t.isdigit():
            return None
        nums.append(int(t))

    if active is None:
        if len(nums) != 4:
            return None
        br, bc, r, c = nums
    else:
        if len(nums) == 2:
            br, bc = active
            r, c = nums
        elif len(nums) == 4:
            br, bc, r, c = nums
        else:
            return None

    for v in (br, bc, r, c):
        if v < 1 or v > 3:
            return None
    return br - 1, bc - 1, r - 1, c - 1


def run() -> None:
    game = UltimateTicTacToe.new()
    print("Ultimate Tic-Tac-Toe")
    print("Input: board_row board_col cell_row cell_col (1-3).")
    print("If a board is forced, you may enter just cell_row cell_col.")
    print("Type 'q' to quit.\n")

    while True:
        print(game.render())
        if game.global_winner():
            print(f"\nWinner: {game.global_winner()}")
            break
        if game.is_over():
            print("\nGame over: tie.")
            break

        if game.active_board is None:
            prompt = f"\nPlayer {game.current} move (any board): "
        else:
            br, bc = game.active_board
            prompt = f"\nPlayer {game.current} move (board {br+1},{bc+1}): "

        move = parse_move(input(prompt), game.active_board)
        if move is None:
            print("Invalid input. Try again.")
            continue
        br, bc, r, c = move

        if game.active_board is not None and (br, bc) != game.active_board:
            print("That board is not active. Try again.")
            continue

        if not game.place(br, bc, r, c):
            print("Illegal move. Try again.")
            continue


if __name__ == "__main__":
    run()
