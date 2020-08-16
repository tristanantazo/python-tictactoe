import random
import math
# Import the pygame
import sys, pygame
from pygame.locals import *

# Initialise pygame
pygame.init()

line_color = (0, 0, 0) 

# to set width of the game window 
width = 400
# to set height of the game window 
height = 400

screen = pygame.display.set_mode((width, height), 0, 32) 

x_player = pygame.image.load('assets/x.png')
x_player = pygame.transform.scale(x_player, (110, 110)) 
o_player = pygame.image.load('assets/o.png')
o_player = pygame.transform.scale(o_player, (110, 110)) 

image_player = x_player

answer_table = ['-','-','-','-','-','-','-','-','-']
game_ongoing = True
current_player = 'X'

temp_score = {'X': 1, 'O':-1, 'tie': 0}

def minimax(depth, is_maximize):
    if check_winner() != '':
        return temp_score[check_winner()]

    if is_maximize:
        best_score = -math.inf
        for key, board in enumerate(answer_table):
            if answer_table[key] == '-':
                answer_table[key] = 'X'
                score = minimax(0, False)
                answer_table[key] = '-'
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for key, board in enumerate(answer_table):
            if answer_table[key] == '-':
                answer_table[key] = 'O'
                score = minimax(0, True)
                answer_table[key] = '-'
                best_score = min(score, best_score)
        return best_score

def bestMove():
    # return 1
    best_score = -math.inf
    for key, board in enumerate(answer_table):
        if answer_table[key] == '-':
            answer_table[key] = 'X'
            score = minimax(0, False)
            answer_table[key] = '-'
            if best_score < score:
                best_score = score
                move = key
    return move
def check_winner():
    global game_ongoing
    winner = ''
    # check for horizontal and diagonal
    row_count = col_count = 0
    for row in range(3):
        if answer_table[row_count] == answer_table[row_count + 1] == answer_table[row_count + 2] != '-':
            winner = answer_table[row_count]
        row_count += 3
        if answer_table[col_count] == answer_table[col_count + 3] == answer_table[col_count + 6] != '-':
            winner = answer_table[col_count]
        col_count += 1

    dia_1 = answer_table[0] == answer_table[4] == answer_table[8] != "-"
    dia_2 = answer_table[2] == answer_table[4] == answer_table[6] != "-"
    if dia_1 or dia_2:
        winner = answer_table[4]

    if winner != '':
        return winner
    elif '-' not in answer_table:
        winner = 'tie'
        return winner
    else:
        return ''

def flip_player():
  # Global variables we need
  global current_player, image_player
  # If the current player was X, make it O
  if current_player == "X":
    current_player = "O"
    image_player = o_player
    
  # Or if the current player was O, make it X
  elif current_player == "O":
    current_player = "X"
    image_player = x_player

def validateAnswer(answer):
    if answer_table[answer] == 'X' or answer_table[answer] == 'O':
        print('Already Answerd')
        return True
    else:
        return False

def chooseAnswer():
    print(f'Current Player {current_player}')
    incorrect = True
    while incorrect:
        if current_player == 'X':
            position = bestMove()
        else:
            position = int(input('Choose a position from 1 - 9: ')) - 1
        incorrect = validateAnswer(position)
    return position

def drawImage(image_player, current_width, current_height):
    x_position = current_width - (width / 3) + 10
    y_position = current_height - (width / 3) + 10
    screen.blit(image_player, (x_position, y_position))

# display board
def draw_answer(answer):
    array_index = 0
    is_get = False
    for row in range(3):
        current_height = (height / 3) * (row + 1)
        for col in range(3):
            current_width = (width / 3) * (col + 1)
            if current_player == 'X' and answer == array_index:
                is_get = True
            elif current_player == 'O':
                x, y = pygame.mouse.get_pos()
                if current_width > x and current_height > y:
                    is_get = True
            if is_get:
                answer_table[array_index] = current_player
                drawImage(image_player, current_width, current_height)
                flip_player()
                break
            array_index += 1
        if is_get:
            break


def game_initiating_window(): 
    # make background
    screen.fill((255, 255, 255))  

    pygame.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 1) 
    pygame.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 1) 
   
    # # drawing horizontal lines 
    pygame.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 1) 
    pygame.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 1) 

    pygame.display.update()

def restart():
    global current_player, answer_table, image_player
    current_player = 'X'
    image_player = x_player
    answer_table = ['-','-','-','-','-','-','-','-','-']
    game_initiating_window() 

def play_game():
    global game_ongoing
    game_initiating_window()
    while game_ongoing: 
        winner = check_winner()
        if winner == 'X' or winner == 'O':
            game_ongoing = False
            print(f'Winner is {winner}')
        elif winner == 'tie':
            game_ongoing = False
            print('No winner!!!')
        if current_player == 'X':
            answer = chooseAnswer()
            draw_answer(answer)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_ongoing = False
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    pass
            elif event.type == MOUSEBUTTONDOWN: 
                draw_answer('')
                pass
        pygame.display.update()

play_game()
