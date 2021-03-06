from mini_max import *

winner = ""
b = Approach1()
b.display_board()
for i in range(0, 9):
    if i%2==0:
        print("Player 1's Turn")
        print(b.best_move("X", "O", "X", 1, i, i))
        x = int(input("row pos: "))
        y = int(input("col pos: "))
        b.make_move(x, y, "X")
        b.display_board()
        winner = b.is_win()
        if winner == "X":
            print("Player 1 has won.")
            b.reset_board()
            break
    else:
        print("Player 2's Turn")
        print(b.best_move("O", "X", "O", 1, i, i))
        x = int(input("row pos: "))
        y = int(input("col pos: "))
        b.make_move(x, y, "O")
        b.display_board()
        winner = b.is_win()
        if winner == "O":
            print("Player 2 has won.")
            b.reset_board()
            break

if b.is_win() == "Draw":
    print("Match has drawn.")
    b.reset_board()

b.display_board()