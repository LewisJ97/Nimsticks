# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:59:59 2019

@author: lewis
"""

import time

state = ([3, 2], 1)
alpha = -1
beta = 1
    
def terminal_test(state):
    if state == ([1], 1):
        return True
    if state == ([1], 2):
        return True  
    if state == ([], 1):
        return True
    if state == ([], 2):
        return True
        
    return 

def utility_function(state):
    assert terminal_test(state)
    if state == ([1], 1):
        return -1
    elif state == ([1], 2):
        return 1
    elif state == ([], 1):
        return 1
    elif state == ([], 2):
        return -1
    assert False

def remove_duplicates(l):
    res = []
    for x in l:
        if x not in res:
            res.append(x)
    return res
    
def successor_state(state):
    successors = []
    cb = state[0]
    cp = state[1]
    if cp == 1:
        np = 2
    elif cp == 2:
        np =1
    else:
        raise Exception('invalid state: current player should be 1 or 2')
    for i in range(len(cb)):
        if cb[i] < 1:
            raise Exception('invalid state: ' + str(cb) + ' has a pile with < 1 stick')
        for d in [1, 2, 3]:
            if cb[i] - d >= 0:
               nb = cb.copy()
               nb[i] = nb[i] - d
               nb.sort(reverse = True)
               if nb[-1] == 0:
                   nb.pop()
               ns = (nb, np)
               successors.append(ns)
    #print('successors:', successors)
    return (remove_duplicates(successors))

def minimax(state):
    if terminal_test(state):
        return utility_function(state)
    else:
        if state[1] == 2:
            value = 1
            for s in successor_state(state):
                value = min(value, minimax(s))
        elif state[1] == 1:
            value = -1
            for s in successor_state(state):
                value = max(value, minimax(s))
    return value

def call_minimax(state):
    start = time.time()
    result = minimax(state)
    end = time.time()
    print('time taken =', (end - start))
    return result
    
def minimax_ab(state, alpha, beta):
    if terminal_test(state):
        return utility_function(state)
    else:
        if state[1] == 2:
            value = 1
            for s in successor_state(state):
                value1 = min(value, minimax_ab(s, alpha, beta))
                if value1 <= value:
                    value = value1
                    if value <= alpha:
                        return value
                    else:
                        if value < beta:
                            value = beta
        elif state[1] == 1:
            value = -1
            for s in successor_state(state):
                value1 = max(value, minimax_ab(s, alpha, beta))
                if value1 >= value:
                    value = value1
                    if value >= beta:
                        return value
                    else:
                        if value > alpha:
                            value = alpha
        
        return value 

def call_minimax_ab(state, alpha, beta):
    start_time = time.time()
    result_ab = minimax_ab(state, alpha, beta)
    end_time = time.time()
    print('time taken =', (end_time - start_time))
    return result_ab

from random import randrange
print("""************ NIM GAME   ***********
************ Game Start ***********
************ The rules  ***********
-----------------------------------------------------
You need to remove from 1 to 3 sticks from a pile.
The player that removes the final stick is the loser.
-----------------------------------------------------""")

def get_user_input(min, max, prompt):

    while True:
        user_input = int(input(prompt))
        if user_input >= min and user_input <= max:
            break
        else:
            print("Please input an integer between {} and {}.".format(min, max))

    return user_input

number_of_piles = get_user_input(1, 10, "Number of piles: ")
maximum_pile_size = get_user_input(1, 100, "Maximum number of sticks: ")
first_player = get_user_input(1, 2, "First player (enter either 1 for human, or 2 for computer): ")
initial_piles = []

for pile in range(0,number_of_piles):

    pile_size = randrange(1, maximum_pile_size)

    initial_piles.append(pile_size)

    state = (initial_piles, first_player)
print("Here is the inital state: ", state) 

def human_play(state):
        maximum_possible_pick = 3
        n = 0
        if state[1] == 1:
            pile_to_pick_from = get_user_input(1, number_of_piles, "Pile to pick from (see above): ")
            pick = get_user_input(1, maximum_possible_pick, "Number of sticks to remove (between 1 and {}): ".format(maximum_possible_pick)) 
            state[0][pile_to_pick_from - 1] = state[0][pile_to_pick_from - 1] - pick
            next_player = 2
            state = list([state[0]] + [next_player])
            if 0 in state[0]:
                state[0].remove(0)
        return tuple(state)

def computer_play(state):
    n = 0
    end = len(successor_state(state))
    next_player = 2
    state = tuple([state[0]] + [next_player])
    if state[1] == 2:
        for items in successor_state(state):
            value = minimax_ab(items, -1, 1)
            n += 1
            if value == -1:
                state = items 
                return state
            elif n == end:
                state = items
    return state            

def domain(state):
    end = state
    while True:   
        end = human_play(end)
        print("human's move: ", end)
        end = computer_play(end)
        print("computer's move: ", end)
        if terminal_test(end):
            final = utility_function(end)
            if final == -1:
                print('!!! The computer player wins !!!')
                return
            if final == 1:
                print('!!! The huamn player wins !!!')
                return

domain(state)