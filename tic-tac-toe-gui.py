import pygame, sys, math

HEIGHT = 600
WIDTH = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

#colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

#tic tac toe board
board = [
			["", "", ""],
			["", "", ""],
			["", "", ""],
		]

scores = {
			'X' : 10,
		  	'O' : -10,
		  	'TIE' : 0
		}

player = "X"
game_over = False


pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE GAME")
window.fill(BG_COLOR)

def draw_lines():
	#horizontal 1
	pygame.draw.line(window, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
	#horizontal 2
	pygame.draw.line(window, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)

	#vertical 1
	pygame.draw.line(window, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
	#vertical 2
	pygame.draw.line(window, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

def best_move():
	best_score = -math.inf
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == "":
				board[row][col] = "X"
				score = minimax(board, 0, False)
				board[row][col] = ""
				if score > best_score:
					best_score = score
					best_row = row
					best_col = col

	board[best_row][best_col] = "X"
	draw_mark(best_row, best_col)
	winner, win_line = check_win()

	if winner != None:
		if win_line != None:
			if win_line == "ver":
				draw_vertical_winning_line(best_col, "X")
				return True
			elif win_line == "hor":
				draw_horizontal_winning_line(best_row, "X")
				return True
			elif win_line == "asc":
				draw_asc_winning_line("X")
				return True
			elif win_line == "desc":
				draw_desc_winning_line("X")
				return True
	return False

def minimax(board, depth, isMaximizing):
	result, line = check_win()
	if result is not None:
		return scores[result]

	if isMaximizing:
		best_score = -math.inf
		for row in range(BOARD_ROWS):
			for col in range(BOARD_COLS):
				if board[row][col] == "":
					board[row][col] = "X"
					score = minimax(board, depth+1, False)
					board[row][col] = ""
					best_score = max(score, best_score)

		return best_score

	else:
		best_score = math.inf
		for row in range(BOARD_ROWS):
			for col in range(BOARD_COLS):
				if board[row][col] == "":
					board[row][col] = "O"
					score = minimax(board, depth+1, True)
					board[row][col] = ""
					best_score = min(score, best_score)
		return best_score

def draw_mark(row, col):
	if board[row][col] == "O":
		pygame.draw.circle(window, CIRCLE_COLOR, (int(col*200 + 100), int(row*200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
	elif board[row][col] == "X":
		pygame.draw.line(window, CROSS_COLOR, (col*200 + SPACE, row*200 + 200 - SPACE), (col*200 + 200 - SPACE, row*200 + SPACE), CROSS_WIDTH)
		pygame.draw.line(window, CROSS_COLOR, (col*200 + SPACE, row*200 + SPACE), (col*200 + 200 - SPACE, row*200 + 200 - SPACE), CROSS_WIDTH)

def mark_cell(row, col, player):
	board[row][col] = player

def available_cell(row, col):
	return board[row][col] == ""

def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == "":
				return False
	return True

def check_win():
	winner = None
	empty_cell = 0 
	line = None
	#vertical win
	for col in range(BOARD_COLS):
		if board[0][col] == board[1][col] == board[2][col] == "X" or board[0][col] == board[1][col] == board[2][col] == "O":
			winner = board[0][col]
			line = "ver"

	#horizontal win
	for row in range(BOARD_ROWS):
		if board[row][0] == board[row][1] == board[row][2] == "X" or board[row][0] == board[row][1] == board[row][2] == "O":
			winner = board[row][0]
			line = "hor"

	#asc diagonal win
	if board[2][0] == board[1][1] == board[0][2] == "X" or board[2][0] == board[1][1] == board[0][2] == "O":
		winner = board[1][1]
		line = "asc"

	#desc diagonal win
	if board[0][0] == board[1][1] == board[2][2] == "X" or board[0][0] == board[1][1] == board[2][2] == "O":
		winner = board[0][0]
		line = "desc"

	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == "":
				empty_cell += 1

	if winner == None and empty_cell == 0:
		return "TIE", line

	else:
		return winner, line


def draw_vertical_winning_line(col, player):
	posX = col*200 + 100

	if player == "X":
		color = CROSS_COLOR
	elif player == "O":
		color = CIRCLE_COLOR

	pygame.draw.line(window, color, (posX, 15), (posX, HEIGHT -15), LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
	posY = row*200 + 100

	if player == "X":
		color = CROSS_COLOR
	elif player == "O":
		color = CIRCLE_COLOR

	pygame.draw.line(window, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)

def draw_asc_winning_line(player):
	if player == "X":
		color = CROSS_COLOR
	elif player == "O":
		color = CIRCLE_COLOR

	pygame.draw.line(window, color, (15, HEIGHT - 15), (WIDTH - 15, 15), LINE_WIDTH)

def draw_desc_winning_line(player):
	if player == "X":
		color = CROSS_COLOR
	elif player == "O":
		color = CIRCLE_COLOR

	pygame.draw.line(window, color, (15, 15), (WIDTH - 15, HEIGHT - 15), LINE_WIDTH)

def reset_board():
	window.fill(BG_COLOR)
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = ""


draw_lines()

#mainloop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if not game_over:
			if player == "X":
				if best_move():
					game_over = True
				else:
					player = "O"
			elif player == "O":
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouseX = event.pos[0]
					mouseY = event.pos[1]

					clicked_row = int(mouseY // 200)	#row index
					clicked_col = int(mouseX // 200)	#column index

					if available_cell(clicked_row, clicked_col):
						mark_cell(clicked_row, clicked_col, "O")
						draw_mark(clicked_row, clicked_col)
						player = "X"
						mark, win_line = check_win()
						if win_line == "ver":
							draw_vertical_winning_line(clicked_col, mark)
							game_over = True
						elif win_line == "hor":
							draw_horizontal_winning_line(clicked_row, mark)
							game_over = True
						elif win_line == "asc":
							draw_asc_winning_line(mark)
							game_over = True
						elif win_line == "desc":
							draw_desc_winning_line(mark)
							game_over = True

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F5:
				reset_board()
				player = "X"
				game_over = False

	pygame.display.update()

