import random
import math
# Import the pygame
import sys, pygame
from pygame.locals import *

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
  global current_player
  # If the current player was X, make it O
  if current_player == "X":
    current_player = "O"
    
  # Or if the current player was O, make it X
  elif current_player == "O":
    current_player = "X"

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
# display board
def Draw():
    counter = 0
    for key, board in enumerate(answer_table):
        counter += 1
        if counter > 2:
            print(f'{board} | ', end='')
            print(' ')
            counter = 0
        else:
            print(f'{board} | ', end='')
    print(' ')

def play_game():
    global game_ongoing
    while game_ongoing: 
        answer = chooseAnswer()
        answer_table[answer] = current_player
        flip_player()
        Draw()
        winner = check_winner()

        if winner == 'X' or winner == 'O':
            game_ongoing = False
            print(f'Winner is {winner}')
        elif winner == 'tie':
            game_ongoing = False
            print('No winner!!!')
play_game()
