import numpy as np

class SmartPlayer():
    """
        SmartPlayer class represents the smart player which has been trained
        in playing TicTacToe over multiple games through Reinforcement Learning.
    """

    def __init__(self, player, exploration):
        """
            Initializes the SmartPlayer with a set of certain characteristics.

            Parameter(s):
                player (string): represents the marker associated with the player
                                 accepted values: ["X", "O"]
                exploration (float): represents the probability of exploring for a solution
                                     range: 0<=exploration<=1
        """
        self.player = player
        self.exploration = exploration
        self.gamma = 0.9
        self.learning_rate = 0.2

    def find_empty(self, board):
        """
            find_empty finds all empty locations on the board.

            Parameter(s):
                board (list of lists): a tic tac toe board

            Return(s):
                empty_locn: a list of lists where each sublist represents
                            the indices of location
        """
        empty_locn = []
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == "":
                    empty_locn.append([i, j])
        return empty_locn

    def generate_states(self, board):
        """
            generate_states generates the state string of the board in current
            condition. This is done by iterating through each row one by one.

            Parameter(s):
                board (list of lists): a tic tac toe board

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
                state+=transform_marker[board[i][j]]
        return state

    def make_move(self, state_reward, board):
        """
            make_move allows the player to put his marker on the board.

            Parameter(s):
                state_reward (dict{string: float}): a dictionary containing the states and rewards
                                                    associated with them
                                                    key: should be a valid state string
                                                    value: rewards calculated for the particular state
                board (list of lists): a tic tac toe board

            Return(s):
                move (list): a move describe by the row and column position of the move
                state_reward(dict): a dictionary containing the states and rewards
                                    associated with them
        """
        move = []
        if np.random.uniform(0, 1)<self.exploration:
            #select a random position from available positions
            #generate the new status and if first time add it to the
            #state reward data structure with initialized value of 0
            empty_locn = self.find_empty(board)
            move = np.random.choice(len(empty_locn))
            move = empty_locn[move]

        else:
            #iterate in all available positions and select the one
            #which fetches the maximum reward
            max_rew = -10000
            for m in self.find_empty(board):
                board[m[0]][m[1]] = self.player
                state = self.generate_states(board)
                if state not in state_reward.keys():
                    rew = 0
                else:
                    rew = state_reward[state]
                if max_rew<rew:
                    max_rew = rew
                    move = m
                board[m[0]][m[1]] = ""
        return move, state_reward

    def backpropagate(self, states_of_game, reward, state_reward):
        """
            backpropagate backpropogates the reward received by the player at
            the end of the game to each of the contributing states.

            Parameter(s):
                states_of_game (list): a list of strings of each state the board has
                                       been for the player in the entirety of the game in sequence
                                       len(states_of_game)==5/4
                reward (int): reward/feedback sent by the board to the players based on the
                              performance in the game
                state_reward (dict{string: float}): a dictionary containing the states and rewards
                                                    associated with them
                                                    key: should be a valid state string
                                                    value: rewards calculated for the particular state
            
            Return(s):
                state_reward(dict): an updated dictionary containing the states and rewards
                                    associated with them
        """
        for state in reversed(states_of_game):
            if state not in state_reward.keys():
                state_reward[state] = 0
            state_reward[state] = state_reward[state] + self.learning_rate*(reward*self.gamma - state_reward[state])
            reward = state_reward[state]
        return state_reward
