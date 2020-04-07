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

ABPLAYER = 0
MCTSAI = 1

EMPTY = 0
ABPLAYER_PEICE = 1
MCTSAI_PEICE = 2

WINDOW_LENGTH = 4

SIMULATIONS = [35,40,45,50,55,60,65,70,70,80,85,90,100,110]
#SIMULATIONS = [42]

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
    opp_peice = ABPLAYER_PEICE
    if peice == ABPLAYER_PEICE:
        opp_peice = MCTSAI

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
    return winning_move(board, ABPLAYER_PEICE) or winning_move(board, MCTSAI_PEICE) or len(get_valid_locations(board)) == 0

def game_result(board):
    if is_terminal_node(board):
        if winning_move(board, MCTSAI_PEICE):
            return MCTSAI_PEICE
        elif winning_move(board, ABPLAYER_PEICE):
            return ABPLAYER_PEICE
        else:
            return EMPTY
    return None

    
def alphaBeta(board, depth, alpha, beta, maxi_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            #edge case 1: AI is in winning move
            if winning_move(board, MCTSAI_PEICE):
                return (None, 10000000000000000000000)
            #edge case 2: Player is in winning move
            elif winning_move(board, ABPLAYER_PEICE):
                return (None, -10000000000000000000000)
            #if no moves left (game over)
            else:
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, MCTSAI_PEICE))
    if maxi_player: #maximizing player (AI)
        value = - math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, MCTSAI_PEICE)
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
            drop_piece(b_copy, row, col, ABPLAYER_PEICE)
            new_score = alphaBeta(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def monte_carlo_tree_search(board, SIMULATIONS, piece):
    #run a simulation to find MCTSAI_PLAYER'S best move
    search_board = board.copy()
    valid_moves = get_valid_locations(search_board)
    toplay = turn ##maybe peice instead of player?
    best_result, best_move_MC = -20.0, None    # 
    best_move_MC = valid_moves[0]
    wins_MC = np.zeros(len(valid_moves))
    visits_MC = np.zeros(len(valid_moves))
    for sim in range(SIMULATIONS):
        for i, col in enumerate(valid_moves):
            row = get_next_open_row(board, col)
            drop_piece(search_board, row, col, piece)
            result = game_result(search_board)
            if result == piece:
                #this move results in a win
                undo(search_board, row, col)
                return col
            sim_result = simulate_play(search_board, piece)
            wins_MC[i] += sim_result
            visits_MC[i] += 1.0
            win_rate_MC = wins_MC[i] / visits_MC[i]
            if win_rate_MC > best_result:
                best_result = win_rate_MC
                best_move_MC = col
            undo(board, row, col)
    
    #Simulate Opponent's plays and find best opponent move
    opponent = ABPLAYER_PEICE
    search_board = board.copy()
    valid_moves = get_valid_locations(search_board)
    toplay = turn ##maybe peice instead of player?
    best_result, best_move_Opp = -20.0, None    # 
    best_move_Opp = valid_moves[0]
    wins_Opp = np.zeros(len(valid_moves))
    visits_Opp = np.zeros(len(valid_moves))
    for sim in range(7):
        for i, col in enumerate(valid_moves):
            row = get_next_open_row(board, col)
            drop_piece(search_board, row, col, opponent)
            result = game_result(search_board)
            if result == opponent:
                #this move results in a win
                undo(search_board, row, col)
                return col
            sim_result = simulate_play(search_board, piece)
            wins_Opp[i] += sim_result
            visits_Opp[i] += 1.0
            win_rate_Opp = wins_Opp[i] / visits_Opp[i]
            if win_rate_Opp > best_result:
                best_result = win_rate_Opp
                best_move_Opp = col   
            undo(board, row, col)

    #if opponents move returns a better score, use the opponents move instead
    if max(win_rate_Opp,win_rate_MC) == win_rate_Opp:
        best_move = best_move_Opp
    else:
        best_move = best_move_MC
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
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, toplay)
        move = [row, col]
        simulation_moves.append(move)
        result = game_result(board)
        #switch turns
        if toplay == MCTSAI_PEICE:
            toplay = ABPLAYER_PEICE
        else:
            toplay = MCTSAI_PEICE
    for m in simulation_moves[::-1]:
        undo(board, m[0], m[1])
    res_value = 1.0 if result == piece else 0.0
    return res_value      

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
            if board[r][c] == ABPLAYER_PEICE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == MCTSAI_PEICE:    
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

            pygame.display.update()


def endgame_results(total_games, alphaBetawins, MCTSwins, sims):
    #endgame: clear screen and show wins
    screen.fill(BLACK)
    gameTotalLabel = myfont.render("GAMES: "+ str(total_games), 1, BLUE)
    ABwinsLabel = myfont.render("AB WINS: " +str(alphaBetawins), 1, RED)
    MCSTSwinsLabel = myfont.render("MCTS WINS: " +str(MCTSwins), 1, YELLOW)

    print("GAMES: "+ str(total_games))
    print("MCTS Simulations: " +str(sims))
    print("AB WINS: " +str(alphaBetawins))
    print("MCTS WINS: " +str(MCTSwins))

    screen.blit(gameTotalLabel, (40,50))        
    screen.blit(ABwinsLabel, (40,300))        
    screen.blit(MCSTSwinsLabel, (40,500)) 
    pygame.display.update()       
    pygame.time.wait(100)

for sims in SIMULATIONS:
	#main function
	total_games= 30
	alphaBetawins = 0
	MCTSwins = 0   

	SQUARESIZE = 100
	width = COLUMN_COUNT * SQUARESIZE
	height = (ROW_COUNT+1) * SQUARESIZE

	size = (width, height)

	RADIUS = int(SQUARESIZE/2 -5)         
	for i in range(total_games):
	    board = create_board()
	    #print_board(board)
	    game_over = False
	    #turn = 0   #player always goes first
	    #turn = random.randint(ABPLAYER,MCTSAI)    #first player alternates
	    turn = MCTSAI
	    #turn = ABPLAYER
	    #turn = 1
	    pygame.init()


	    screen = pygame.display.set_mode(size)
	    draw_board(board)
	    pygame.display.update()

	    myfont = pygame.font.SysFont("monospace", 75)

	    while not game_over:

	        for event in pygame.event.get():
	            if event.type == pygame.QUIT:
	                sys.exit()
	                            
	        # #Ask for player 1 input
	        if turn == ABPLAYER:
	            #RED player is set to use alphaBeta
	            col, minimax_score = alphaBeta(board, 4, -math.inf, math.inf, True)  #alphabeta solver
	            if is_valid_location(board,col):
	                row = get_next_open_row(board, col)
	                drop_piece(board, row, col, ABPLAYER_PEICE)
	                #if AlphaBeta wins: gameover
	                if winning_move(board, ABPLAYER_PEICE):
	                    #print("\nPlayer 1 Wins!!\n Here is the final board:\n ")
	                    label = myfont.render("ALPHABETA WINS!!!", 1, RED)
	                    screen.blit(label, (40,10))
	                    alphaBetawins += 1
	                    game_over = True

	                draw_board(board)
	                
	                turn += 1
	                turn = turn % 2 #turn will alternate between 0 and 1


	        # #Ask for Player 2 input
	        if turn == MCTSAI and not game_over:
	            #YELLOW player is set to use MCTS
	            col = monte_carlo_tree_search(board, sims, MCTSAI_PEICE)
	            if is_valid_location(board,col):
	                row = get_next_open_row(board, col)
	                drop_piece(board, row, col, MCTSAI_PEICE)
	                #if MCTS wins: gameover
	                if winning_move(board, MCTSAI_PEICE):
	                    label = myfont.render("MONTE CARLO ts WINS!!!", 1, YELLOW)
	                    screen.blit(label, (40,10))
	                    MCTSwins += 1
	                    game_over = True

	                draw_board(board)
	                
	                turn += 1
	                turn = turn % 2 #turn will alternate between 0 and 1
	        
	        #if there are no valid locations left: gameover (draw)
	        if get_valid_locations(board) == None:
	            label = myfont.render("DRAW MATCH.", 1, BLUE)
	            screen.blit(label, (40,10))     
	            game_over = True
	        #if game over then wait 3sec before next game starts
	        if game_over:
	            pygame.time.wait(100)

	#displaying the results at endgame
	endgame_results(total_games, alphaBetawins, MCTSwins,sims )
