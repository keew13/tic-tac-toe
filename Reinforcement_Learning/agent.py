import numpy as np

class SmartPlayer():
    """
        SmartPlayer class represents the smart player which has been trained
        in playing TicTacToe over multiple games through Reinforcement Learning.
    """

    def __init__(self, player):
        self.player = player
        self.exploration = 0.3
        self.gamma = 0.9
        self.learning_rate = 0.2

    def find_empty(self, board):
        empty_locn = []
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == "":
                    empty_locn.append([i, j])
        return empty_locn

    def generate_states(self, board):
        transform_marker = {"X":"1", "O":"-1", "":"0"}
        state = ""
        for i in range(0, 3):
            for j in range(0, 3):
                state+=transform_marker[board[i][j]]
        return state

    def make_move(self, state_reward, board):
        """
            make_move allows the player to put his marker on the board
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
        for state in reversed(states_of_game):
            if state not in  state_reward.keys():
                state_reward[state] = 0
            state_reward[state] = state_reward[state] + self.learning_rate*(reward*self.gamma - state_reward[state])
            reward = state_reward[state]
        return state_reward
