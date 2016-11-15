# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 09:08:46 2016

@author: Herbee
"""

tic_tac = {'A':{1:' ',2:' ',3:' '},'B':{1:' ',2:' ',3:' '},'C':{1:' ',2:' ',3:' '}}

def printboard(tic_tac):
    for row in ['A','B','C']:
        for col in [1,2,3]:
            print (tic_tac[row][col], end='|')
        print('\n' + '-------')

turn = 0 
while True:
    print('input your position i.e. A1')
    place = input()
    place_row = place[0]
    place_col = int(place[1])
    turn = turn + 1
    if turn%2 == 0:
        tic_tac[place_row][place_col] = 'o'
    else:
        tic_tac[place_row][place_col] = 'x'
    printboard(tic_tac)
    
