import game_basics

class Approach1(game_basics.TicTacToe):
    def best_move(self, og_player, op_player, player, is_maximizing, og_depth, depth):
        winner = self.is_win()
        if winner==og_player:
            return 1
        elif winner=="Draw":
            return 0
        elif winner==op_player:
            return -1
        best_score = -5*is_maximizing
        move = []
        for i in range(1, 4):
            for j in range(1, 4):
                if self.check_empty(i, j)==1:
                    self.make_move(i, j, player)
                    if player == "X":
                        score = self.best_move(og_player, op_player, "O", is_maximizing*-1, og_depth, depth+1)
                    else:
                        score = self.best_move(og_player, op_player, "X", is_maximizing*-1, og_depth, depth+1)
                    self.board[i-1][j-1] = ""
                    if is_maximizing == 1:
                        if best_score<score:
                            best_score = score
                            move = [i, j]
                    else:
                        if best_score>score:
                            best_score = score
                            move = [i, j]
        if depth == og_depth:
            return move
        return best_score