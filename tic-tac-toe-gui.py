import pygame, sys

pygame.init()

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


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE GAME")
window.fill(BG_COLOR)

#tic tac toe board
board = [
			["", "", ""],
			["", "", ""],
			["", "", ""],
		]

def draw_lines():
	#horizontal 1
	pygame.draw.line(window, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
	#horizontal 2
	pygame.draw.line(window, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)

	#vertical 1
	pygame.draw.line(window, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
	#vertical 2
	pygame.draw.line(window, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

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

def check_win(player):
	#vertical win
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(col, player)
			return True

	#horizontal win
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			return True

	#asc diagonal win
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_winning_line(player)
		return True

	#desc diagonal win
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_winning_line(player)
		return True

	return False


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

player = "X"
game_over = False

#mainloop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
			mouseX = event.pos[0]
			mouseY = event.pos[1]

			clicked_row = int(mouseY // 200)	#row index
			clicked_col = int(mouseX // 200)	#column index

			if available_cell(clicked_row, clicked_col):
				if player == "X":
					mark_cell(clicked_row, clicked_col, "X")
					if check_win(player):
						game_over = True
					player = "O"
				elif player == "O":
					mark_cell(clicked_row, clicked_col, "O")
					if check_win(player):
						game_over = True
					player = "X"

				draw_mark(clicked_row, clicked_col)

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				reset_board()
				player = "X"
				game_over = False

	pygame.display.update()

