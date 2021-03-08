from agent import SmartPlayer
import json
from tqdm import tqdm

class Board:
    """
        Board class represents the TicTacToe board (environment) on which the
        game will be played and it provides the basic utilities to do so.
    """

    def __init__(self, state_rewards_path_X, state_rewards_path_O, exploration):
        """
            Initializes the tic tac toe board and loads the contents of rewards files.

            Parameter(s):
                state_rewards_path_X (string): path for the json file containing the states
                                               and associated rewards for player X
                state_rewards_path_O (string): path for the json file containing the states
                                               and associated rewards for player O
                exploration (float): represents the probability of exploring for a solution
                                     range: 0<=exploration<=1
        """
        self.path_X = state_rewards_path_X
        self.path_O = state_rewards_path_O
        with open(self.path_X) as file:
            self.states_reward_X = json.load(file)
        with open(self.path_O) as file:
            self.states_reward_O = json.load(file)
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.player1 = SmartPlayer("X", exploration)
        self.player2 = SmartPlayer("O", exploration)
        self.states_of_game_X = []
        self.states_of_game_O = []

    def display_board(self):
        """
            display_board allows to display the board in its current
            status on the console terminal.
        
            Parameter(s):
                None
        """
        for i in range(0, 3):
            for j in range(0, 3):
                if j<2:
                    print("\t"+self.board[i][j]+"\t|", end = "")
                else:
                    print("\t"+self.board[i][j])
                    if(i!=2):
                        print("-"*50)
    
    def reset_board(self):
        """
            reset_board resets the board.

            Parameter(s):
                None
        """
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.states_of_game_X = []
        self.states_of_game_O = []

    def is_win(self):
        """
            is_win checks if any player has won given the current status of the board.
            The checks are made row wise, column wise and diagonally. If three of the 
            current player's marker line up then it wins.
        
            Parameter(s):
                None

            Return(s):
                "X": Player X has won
                "O": Player O has won
                "Draw": Match has drawn
                "Match Ongoing": Match is in play
        """
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
        """
            generate_states generates the state string of the board in current
            condition. This is done by iterating through each row one by one.

            Parameter(s):
                None
            
            Return(s):
                state: a string representing the state of the board

            Example:
                if the current condition of the board is:
                    X   |   O   |   X
                    O   |       |   X
                    O   |   X   |   O

                and {X: 1, O: -1, "":0} then,
                state = "1 -1 1 -1 0 1 -1 1 -1"
        """
        transform_marker = {"X":"1", "O":"-1", "":"0"}
        state = ""
        for i in range(0, 3):
            for j in range(0, 3):
                state+=transform_marker[self.board[i][j]]
        return state
    
    def make_move(self, player, move):
        """
            make_move makes a move on the board at the given position for the given player

            Parameter(s):
                player (string): represents the marker of the player
                                 accepted values: ["X", "O"]
                move (list): a list representing a valid move i, j
                             range: 1<=i<=3
                             range: 1<=j<=3
        """
        self.board[move[0]-1][move[1]-1] = player
    
    def give_reward(self):
        """
            give_reward gives rewards/feedbacks to the players based on their performance
            in the game. Reward value of 1 is given when the player wins and -1 when it loses.
            0 is given to both players if the game ends in a draw.

            Parameter(s):
                None
        """
        if self.is_win() == "X":
            self.states_reward_X = self.player1.backpropagate(self.states_of_game_X, 1, self.states_reward_X)
            self.states_reward_O = self.player2.backpropagate(self.states_of_game_O, -1, self.states_reward_O)
        elif self.is_win() == "O":
            self.states_reward_X = self.player1.backpropagate(self.states_of_game_X, -1, self.states_reward_X)
            self.states_reward_O = self.player2.backpropagate(self.states_of_game_O, 1, self.states_reward_O)
        elif self.is_win() == "Draw":
            self.states_reward_X = self.player1.backpropagate(self.states_of_game_X, 0, self.states_reward_X)
            self.states_reward_O = self.player2.backpropagate(self.states_of_game_O, 0, self.states_reward_O)    
    
    def train_agents(self):
        """
            train_agents trains the player to play the game of tic tac toe smartly.
            
            Parameter(s):
                None
        """
        for _ in tqdm(range(0, 50000)):
            for m in range(0, 9, 2):
                move, self.states_reward_X = self.player1.make_move(self.states_reward_X, self.board)
                self.board[move[0]][move[1]] = self.player1.player                
                self.states_of_game_X.append(self.generate_states())
                if(self.is_win()=="X" or m==8): 
                    break
                move, self.states_reward_O =  self.player2.make_move(self.states_reward_O, self.board)
                self.board[move[0]][move[1]] = self.player2.player
                self.states_of_game_O.append(self.generate_states())
                if(self.is_win()=="O"):
                    break
            self.give_reward()
            self.reset_board()
        with open(self.path_X, 'w') as file:
            json.dump(self.states_reward_X, file, indent=4)
        with open(self.path_O, 'w') as file:
            json.dump(self.states_reward_O, file, indent=4)

if __name__ == "__main__":
    TicTacToe = Board("state_rewards_X.json", "state_rewards_O.json", 0.1)
    TicTacToe.train_agents()