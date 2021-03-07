#This file is meant for creating code that allows to play the tic tac toe game using Reinforcement Learning
import environment
import agent

winner = ""
board = environment.Board("state_rewards_X.json", "state_rewards_O.json")
board.display_board()
for i in range(0, 9):
    if(i%2==0):
        print("Player 1's Turn")
        move, _ = board.player1.make_move(board.states_reward_X, board.board)
        print(move)
        x = int(input("row pos: "))
        y = int(input("col pos: "))
        board.make_move("X", [x, y])
        board.display_board()
        winner = board.is_win()
        if winner == "X":
            print("Player 1 has won.")
            board.reset_board()
            break
    else:
        print("Player 2's Turn")
        move, _ = board.player2.make_move(board.states_reward_O, board.board)
        print(move)
        x = int(input("row pos: "))
        y = int(input("col pos: "))
        board.make_move("O", [x, y])
        board.display_board()
        winner = board.is_win()
        if winner == "O":
            print("Player 2 has won.")
            board.reset_board()
            break

if board.is_win() == "Draw":
    print("Match has drawn.")
    board.reset_board()

board.display_board()