#source freeCodeCamp.org: https://www.youtube.com/watch?v=XpYz-q1lxu8
## Above is used to create the gameboard
#source freeCodeCamp.org (AI): https://www.youtube.com/watch?v=8392NJjj8s0&t=58s
## Above is a tutorial for the search AI
import numpy as np
import pygame
import sys
import math
import random

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

AI_1 = 0
AI_2 = 1

EMPTY = 0
#PLAYER_PEICE = 1
#AI_PEICE = 2
AI_1_PEICE = 1
AI_2_PEICE = 2


WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    #if return true, column is not filled - elif false column is filled up
    return board[5][col] == 0 

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board,piece):
    #NOTE: functions are naive (can be revamped)

    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    # Check vertical location for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    # Check for positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    # Check for negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, peice):
    score = 0
    opp_peice = AI_1_PEICE
    if peice == AI_1_PEICE:
        opp_peice = AI_2

    if window.count(peice) == 4:
        score += 100
    elif window.count(peice) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(peice) == 2 and window.count(EMPTY) == 2:
        score += 5
    
    if window.count(opp_peice) == 3 and window.count(EMPTY) ==1:
        score -= 80
    
    return score


def score_position(board, piece):
    score = 0

    # Score center column (preference for center)
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count*6

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c: c+WINDOW_LENGTH]
            score += evaluate_window(window,piece)
   
    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window,piece)
    
    # Score positive-sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)
    
    # Score negatively-sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)
    
    return score

def is_terminal_node(board):
    return winning_move(board, AI_1_PEICE) or winning_move(board, AI_2_PEICE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maxi_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            #edge case 1: AI is in winning move
            if winning_move(board, AI_2_PEICE):
                return (None, 10000000000000000000000)
            #edge case 2: Player is in winning move
            elif winning_move(board, AI_1_PEICE):
                return (None, -10000000000000000000000)
            #if no moves left (game over)
            else:
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_2_PEICE))
    if maxi_player: #maximizing player (AI)
        value = - math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_2_PEICE)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else: #minimizing player (PLAYER)
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_1_PEICE)
            new_score = minimax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value
    
def alphaBeta(board, depth, alpha, beta, maxi_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            #edge case 1: AI is in winning move
            if winning_move(board, AI_2_PEICE):
                return (None, 10000000000000000000000)
            #edge case 2: Player is in winning move
            elif winning_move(board, AI_1_PEICE):
                return (None, -10000000000000000000000)
            #if no moves left (game over)
            else:
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_2_PEICE))
    if maxi_player: #maximizing player (AI)
        value = - math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_2_PEICE)
            new_score = alphaBeta(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: #minimizing player (PLAYER)
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_1_PEICE)
            new_score = alphaBeta(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

      

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    best_score = -10000
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == AI_1_PEICE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_2_PEICE:    
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    
            pygame.display.update()
 

total_games= 0
Player1_wins = 0
Player2_wins = 0            
while total_games != 100:
    board = create_board()
    #print_board(board)
    game_over = False
    #turn = 0   #player always goes first
    turn = AI_1    #first player 

    pygame.init()

    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE/2 -5)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            #NOTE: color updates on mouse motion - wont update if mouse is static
            
                            
                # #Ask for player 1 input
        if turn == AI_1 and not game_over:
            pygame.time.wait(0)
            
            col, minimax_score = alphaBeta(board, 4, -math.inf, math.inf, True)  #alphabeta solver
            if is_valid_location(board,col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_1_PEICE)

                if winning_move(board, AI_1_PEICE):                        #print("\nPlayer 2 Wi2ns!!\n Here is the final board:\n ")
                    label = myfont.render("Player 1 WINS!!!", 1, RED)
                    screen.blit(label, (40,10))
                    total_games+= 1
                    Player1_wins+= 1
                    game_over = True
                    


                #print_board(board)
                draw_board(board)
                
                turn += 1
                turn = turn % 2 #turn will alternate between 0 and 1

        # #Ask for Player 2 input
        if turn == AI_2 and not game_over:
            pygame.time.wait(0)
            #col = random.randint(0, COLUMN_COUNT-1) #random walk peice placement
            #col = pick_best_move(board, AI_2_PEICE) #score hueristic search
            #col, minimax_score = minimax(board, 4, True)    #minimax solving algorithm
            col, minimax_score = alphaBeta(board, 4, -math.inf, math.inf, True)  #alphabeta solver
            if is_valid_location(board,col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_2_PEICE)

                if winning_move(board, AI_2_PEICE):
                    #print("\nPlayer 2 Wi2ns!!\n Here is the final board:\n ")
                    label = myfont.render("Player 2 WINS!!!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    total_games+= 1
                    Player2_wins+= 1
                    game_over = True
                    


                #print_board(board)
                draw_board(board)
                
                turn += 1
                turn = turn % 2 #turn will alternate between 0 and 1

        if get_valid_locations(board) == None:
            label = myfont.render("DRAW MATCH.", 1, BLUE)
            screen.blit(label, (40,10))
                    
            game_over = True
        if game_over:
            pygame.time.wait(20)
print("Total Games: "+ str(total_games))
print("Player 1 Wins: "+ str(Player1_wins))
print("Player 2 Wins: "+ str(Player2_wins))