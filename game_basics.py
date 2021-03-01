class BoardIndexNotInRange(Exception):
    """
        BoardIndexNotInRange is an exception raised when wrong indices 
        are provided for the board.
    """
    def __init__(self, x, y):
        self.message = "Positions out of bound for the board.\n"
        self.x = x
        self.y = y
        super().__init__(self.message)
    
    def __str__(self):
        return self.message+f"x:{self.x}, y:{self.y} --> Valid ranges for x and y are between [1, 3] and [1, 3]."

class BoardPositionOccupied(Exception):
    """
        BoardPositionOccupied is an exception raised when player tries
        to put his marker on an already occupied position.
    """
    def __init__(self, x, y, board):
        self.message = "Position already occupied.\n"
        self.x = x
        self.y = y
        self.board = board
        super().__init__(self.message)
    
    def __str__(self):
        return self.message+f"Board at position [{self.x}, {self.y}] already occupied by {self.board[self.x-1][self.y-1]}."

class TicTacToe:
    """
        TicTacToe class provides the basic board structure and utility functions
        to play a game of tic-tac-toe on it.
    """

    def __init__(self):
        """
            Initializes the board with all cells being empty.

            Parameter(s):
                None
        """
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.winner = ""

    def reset_board(self):
        """
            reset_board resets the board.

            Parameter(s):
                None
        """
        self.__init__()

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
    
    def make_move(self, x, y, player):
        """
            make_move allows to the player to put his marker on the
            board at his desired position.
        
            Parameter(s):
                x (integer): the x position of the cell,
                             range: 1<=X<=3
                y (integer): the y position of the cell,
                             range: 1<=y<=3
                player (string): marker of the player  
                                 accepted value: [X, O]
        """
        if((x<1 or x>3) or (y<1 or y>3)):
            raise BoardIndexNotInRange(x, y)
        elif(self.board[x-1][y-1]==""):
            self.board[x-1][y-1]=player
        elif(self.board[x-1][y-1]=="X" or self.board[x-1][y-1]=="O"):
            raise BoardPositionOccupied(x, y, self.board)

    def is_win(self, player):
        """
            is_win checks if any player has won given the current status of the board.
            The checks are made row wise, column wise and diagonally. If three of the 
            current player's marker line up then it wins.
        
            Parameter(s):
                player (string): marker of the current player
                                 accepted value: [X, O]
        """
        win = [player]*3
        if self.winner == "":
            for i in range(0, 3):
                temp = self.board[i]
                if temp == win:
                    self.winner = player
                    break
        if self.winner == "":
            for j in range(0, 3):
                temp = [self.board[i][j] for i in range(0, 3)] 
                if temp == win:
                    self.winner = player
                    break
        if self.winner == "":
            temp1 = [self.board[i][i] for i in range(0, 3)]
            temp2 = [self.board[i][2-i] for i in range(0, 3)]
            if(temp1 == win or temp2 == win):
                self.winner = player