from agent import SmartPlayer
import json
from tqdm import tqdm

class Board:
    def __init__(self, state_rewards_path_X, state_rewards_path_O):
        self.path_X = state_rewards_path_X
        self.path_O = state_rewards_path_O
        with open(self.path_X) as file:
            self.states_reward_X = json.load(file)
        with open(self.path_O) as file:
            self.states_reward_O = json.load(file)
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.player1 = SmartPlayer("X")
        self.player2 = SmartPlayer("O")
        self.states_of_game = []

    def reset_board(self):
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.states_of_game = []

    def is_win(self):
        win_X = ["X"]*3
        win_O = ["O"]*3

        for i in range(0, 3):
            temp = self.board[i]
            if temp == win_X:
                return "X"
            elif temp == win_O:
                return "O"

        for j in range(0, 3):
            temp = [self.board[i][j] for i in range(0, 3)] 
            if temp == win_X:
                return "X"
            elif temp == win_O:
                return "O"

        temp1 = [self.board[i][i] for i in range(0, 3)]
        temp2 = [self.board[i][2-i] for i in range(0, 3)]
        if(temp1 == win_X or temp2 == win_X):
            return "X"
        elif(temp1 == win_O or temp2 == win_O):
            return "O"
        
        for i in range(0, 3):
            for j in range(0, 3):
                if(self.board[i][j]==""):
                    return "Match Ongoing"        
        return "Draw"

    def generate_states(self):
        transform_marker = {"X":"1", "O":"-1", "":"0"}
        state = ""
        for i in range(0, 3):
            for j in range(0, 3):
                state+=transform_marker[self.board[i][j]]
        return state
    
    def give_reward(self):
        if self.is_win() == "X":
            self.states_reward_X = self.player1.backpropagate(self.states_of_game, 1, self.states_reward_X)
            self.states_reward_O = self.player2.backpropagate(self.states_of_game, -1, self.states_reward_O)
        elif self.is_win() == "O":
            self.states_reward_X = self.player1.backpropagate(self.states_of_game, -1, self.states_reward_X)
            self.states_reward_O = self.player2.backpropagate(self.states_of_game, 1, self.states_reward_O)
        elif self.is_win() == "Draw":
            self.states_reward_X = self.player1.backpropagate(self.states_of_game, 0, self.states_reward_X)
            self.states_reward_O = self.player2.backpropagate(self.states_of_game, 0, self.states_reward_O)    
    
    def train_agents(self):
        for game_simulation in tqdm(range(0, 50000)):
            for m in range(0, 9, 2):
                move, self.states_reward_X = self.player1.make_move(self.states_reward_X, self.board)
                self.board[move[0]][move[1]] = self.player1.player                
                self.states_of_game.append(self.generate_states())
                if(m==8):
                    break
                move, self.states_reward_O =  self.player2.make_move(self.states_reward_O, self.board)
                self.board[move[0]][move[1]] = self.player2.player
                self.states_of_game.append(self.generate_states())
            self.give_reward()
            self.reset_board()
        with open(self.path_X, 'w') as file:
            json.dump(self.states_reward_X, file, indent=4)
        with open(self.path_O, 'w') as file:
            json.dump(self.states_reward_O, file, indent=4)

if __name__ == "__main__":
    TicTacToe = Board("state_rewards_X.json", "state_rewards_O.json")
    TicTacToe.train_agents()