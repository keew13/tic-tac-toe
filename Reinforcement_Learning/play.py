#This file is meant for creating code that allows to play the tic tac toe game using Reinforcement Learning
import environment
import agent

winner = ""
b = environment.Board("state_rewards_X.json", "state_rewards_O.json", 0)
b.display_board()
for i in range(0, 9):
    if(i%2==0):
        print("Player 1's Turn")
        move, _ = b.player1.make_move(b.states_reward_X, b.board)
        print("[", move[0]+1, ", ", move[1]+1, "]")
        x = int(input("row pos: "))
        y = int(input("col pos: "))
        b.make_move("X", [x, y])
        b.display_board()
        winner = b.is_win()
        if winner == "X":
            print("Player 1 has won.")
            b.reset_board()
            break
    else:
        print("Player 2's Turn")
        move, _ = b.player2.make_move(b.states_reward_O, b.board)
        print("[", move[0]+1, ", ", move[1]+1, "]")
        x = int(input("row pos: "))
        y = int(input("col pos: "))
        b.make_move("O", [x, y])
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