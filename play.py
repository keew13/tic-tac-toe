from game_basics import *

b = TicTacToe()
b.display_board()
for i in range(0, 9):
    if i%2==0:
        print("Player 1's Turn")
        x = int(input("row pos: "))
        y = int(input("col pos: "))
        b.make_move(x, y, "X")
        b.display_board()
        b.is_win("X")
        if b.winner == "X":
            print("Player 1 has won.")
            b.reset_board()
            break
    else:
        print("Player 2's Turn")
        x = int(input("row pos: "))
        y = int(input("col pos: "))
        b.make_move(x, y, "O")
        b.display_board()
        b.is_win("O")
        if b.winner == "O":
            print("Player 2 has won.")
            b.reset_board()
            break

if b.winner == "":
    print("Match has drawn.")
    b.reset_board()

b.display_board()