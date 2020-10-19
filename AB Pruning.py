# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:30:24 2019

@author: lewis
"""
state = ([3, 2], 1)
alpha = -1
beta = 1

#def initial_state():
    #state = ([3, 2], 1)
    #aplha = -1
    #beta = 1
    #return state
    
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

#import time

def min_value(state, alpha, beta):
    if terminal_test(state):
        return utility_function(state)
    value = 1
    for s in successor_state(state):
        value1 = min(value, max_value(s, alpha, beta))
        if value1 <= value:
            value = value1
        if value <= alpha:
            return value
        else:
            if value < beta:
                value = beta
    return value
    
def max_value(state, alpha, beta):
    if terminal_test(state):
        return utility_function(state)
    value = -1
    for s in successor_state(state):
        value1 = max(value, min_value(s, alpha, beta))
        if value1 >= value:
            value = value1
        if value >= beta:
            return value
        else:
            if value > alpha:
                value = alpha
    return value