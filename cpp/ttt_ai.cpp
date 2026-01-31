#include <pybind11/pybind11.h>
#include <utility>

namespace py = pybind11;

enum player{
    X,
    O,
    None,
};

/**
 * Gets the player at a specific location of the board
 * IN BOARD 9 least significatn digits are x positoin, then o positon
  */
player get_space(uint32_t board, int row, int col){
    int loc = row*3 + col;
    if(board>>loc & 1){
        return X;
    }
    if(board>>(loc+9) & 1){
        return O;
    }
    return None;
}

const int winning_strips[] = {0b111, 0b111000, 0b111000000, 0b100100100, 0b010010010, 0b001001001, 0b100010001, 0b001010100}; 

/*
 * Gets the winner of the game if current board state has a winner
*/
player get_winner(uint32_t board){
    for(const int strip: winning_strips){
        if((strip & board) == strip)
            return X;
        if((strip<<9 & board) == strip<<9){
            return O;
        }
    }
    return None;
}

std::pair<int, int> get_minimax_move(uint32_t value) {
    return {value, value * 2};
}

PYBIND11_MODULE(ttt_cpp, m) {
    m.doc() = "Tic-tac-toe C++ helpers";
    m.def("get_minimax_move", &get_minimax_move, "Return a tuple (row, col) from C++");
}
