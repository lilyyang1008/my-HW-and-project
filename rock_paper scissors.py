# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 13:28:14 2024

@author: user
"""

import random

def play():
    user=input("What is your choice?'r' for rock,'p' for paper,'s' for scissors\n")
    computer=random.choice(['r','p','s'])
    
    if user==computer:
        return "It\'s a tie"
    if is_win(user,computer):
        return "You won!"
    else:
        return "You lost!"
    
def is_win(player,opponent):
    #return true if player wins
    if (player=='r' and opponent=='s') or (player=='s' and opponent=='p')\
        or (player=='p' and opponent=='r'):
            return True
        
print(play())