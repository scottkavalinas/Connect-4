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

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PEICE = 1
AI_PEICE = 2

WINDOW_LENGTH = 4

SIMULATIONS = 100

def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def undo(board, row, col):
    board[row][col] = EMPTY

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
    opp_peice = PLAYER_PEICE
    if peice == PLAYER_PEICE:
        opp_peice = AI

    if window.count(peice) == 4:
        score += 100
    elif window.count(peice) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(peice) == 2 and window.count(EMPTY) == 2:
        score += 2
    
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
    return winning_move(board, PLAYER_PEICE) or winning_move(board, AI_PEICE) or len(get_valid_locations(board)) == 0

def game_result(board):
    if is_terminal_node(board):
        if winning_move(board, AI_PEICE):
            return AI_PEICE
        elif winning_move(board, PLAYER_PEICE):
            return PLAYER_PEICE
        else:
            return EMPTY
    return None

def minimax(board, depth, maxi_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            #edge case 1: AI is in winning move
            if winning_move(board, AI_PEICE):
                return (None, 10000000000000000000000)
            #edge case 2: Player is in winning move
            elif winning_move(board, PLAYER_PEICE):
                return (None, -10000000000000000000000)
            #if no moves left (game over)
            else:
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PEICE))
    if maxi_player: #maximizing player (AI)
        value = - math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PEICE)
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
            drop_piece(b_copy, row, col, PLAYER_PEICE)
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
            if winning_move(board, AI_PEICE):
                return (None, 10000000000000000000000)
            #edge case 2: Player is in winning move
            elif winning_move(board, PLAYER_PEICE):
                return (None, -10000000000000000000000)
            #if no moves left (game over)
            else:
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PEICE))
    if maxi_player: #maximizing player (AI)
        value = - math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PEICE)
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
            drop_piece(b_copy, row, col, PLAYER_PEICE)
            new_score = alphaBeta(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def monte_carlo_tree_search(board, SIMULATIONS, piece):
    search_board = board.copy()
    valid_moves = get_valid_locations(search_board)
    toplay = turn ##maybe peice instead of player?
    best_result, best_move = -20.0, None
    best_move = valid_moves[0]
    wins = np.zeros(len(valid_moves))
    visits = np.zeros(len(valid_moves))
    for sim in range(SIMULATIONS):
        for i, col in enumerate(valid_moves):
            row = get_next_open_row(board, col)
            drop_piece(search_board, row, col, piece)
            result = game_result(search_board)
            if result == piece:
                #this move results in a win
                undo(search_board, row, col)
                # best_result = win_rate
                # best_move = col
                # break
                return col
            sim_result = simulate_play(search_board, piece)
            wins[i] += sim_result
            visits[i] += 1.0
            win_rate = wins[i] / visits[i]
            # if win_rate < best_result:
            #     best_result = win_rate
            #     best_move = col
            if win_rate > best_result:
                best_result = win_rate
                best_move = col
            
            undo(board, row, col)
        assert best_move is not None
    return best_move

def simulate_play(board, piece):
    result = game_result(board)
    simulation_moves = []
    toplay = piece
    while result is None:
        #NOTE: can I switch simulation with hueristic search? or minimax? or AB?
        valid_moves = get_valid_locations(board)
        while True:
            col = random.randint(0, COLUMN_COUNT-1) #random walk peice placement
            if col in valid_moves:
                break
        #col = pick_best_move(board, toplay) #score hueristic search
        #col, minimax_score = minimax(board, 3, True)    #minimax solving algorithm
        #col, minimax_score = alphaBeta(board,3, -math.inf, math.inf, True)  #alphabeta solver
        
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, toplay)
        move = [row, col]
        simulation_moves.append(move)
        result = game_result(board)
        #switch turns
        if toplay == AI_PEICE:
            toplay = PLAYER_PEICE
        else:
            toplay = AI_PEICE
    for m in simulation_moves[::-1]:
        undo(board, m[0], m[1])
    res_value = 1.0 if result == piece else 0.0
    return res_value
        


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

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations



def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PEICE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PEICE:    
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    
            pygame.display.update()
            

board = create_board()
#print_board(board)
game_over = False
#turn = 0   #player always goes first
turn = random.randint(PLAYER,AI)    #first player alternates

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
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #print_board(event.pos)
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        
    # #Ask for player 1 input
    if turn == PLAYER:
        #note: add error check for 0-6
        #posx = event.pos[0]
        #col = int(math.floor(posx/SQUARESIZE))
        col, minimax_score = alphaBeta(board, 4, -math.inf, math.inf, True)  #alphabeta solver
        
        #col = int(input("Player 1 Make Your Selection (0-6): "))
        if is_valid_location(board,col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PEICE)

            if winning_move(board, PLAYER_PEICE):
                #print("\nPlayer 1 Wins!!\n Here is the final board:\n ")
                label = myfont.render("Player 1 WINS!!!", 1, RED)
                screen.blit(label, (40,10))
                game_over = True

            #print_board(board)
            draw_board(board)
            
            turn += 1
            turn = turn % 2 #turn will alternate between 0 and 1


    # #Ask for Player 2 input
    if turn == AI and not game_over:
        #pygame.time.wait(500)
        #col = random.randint(0, COLUMN_COUNT-1) #random walk peice placement
        #col = pick_best_move(board, AI_PEICE) #score hueristic search
        #col, minimax_score = minimax(board, 4, True)    #minimax solving algorithm
        #col, minimax_score = alphaBeta(board, 4, -math.inf, math.inf, True)  #alphabeta solver
        col = monte_carlo_tree_search(board, SIMULATIONS, AI_PEICE)
        if is_valid_location(board,col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PEICE)

            if winning_move(board, AI_PEICE):
                #print("\nPlayer 2 Wi2ns!!\n Here is the final board:\n ")
                label = myfont.render("Player 2 WINS!!!", 1, YELLOW)
                screen.blit(label, (40,10))
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
        pygame.time.wait(3000)
