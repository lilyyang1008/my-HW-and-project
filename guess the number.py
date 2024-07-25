# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 10:34:52 2024

@author: user
"""

import random

def guess(x):
    random_num=random.randint(1,x)
    guess=0
    while guess!=random_num:
        guess=int(input(f"guess a number between 1 and {x}:"))
        print(guess)
        if guess<random_num:
            print("please guess again.too low")
        elif guess>random_num:
            print("please guess again.to high")
            
    print(f"you have got the number {random_num} correctly")
    
def computer_guess(x):
    low=1
    high=x
    feedback=''
    while feedback!='c':
        if low!=high:
            guess=random.randint(low,high)
        else:
            guess=low
        feedback=input(f"is {guess} too high(H),too low(L),or correct(C)?").lower()
        if feedback=='h':
            high=guess-1
        elif feedback=='l':
            low=guess+1
            
    print(f"the computer guessed your number {guess} correctly")
            

computer_guess(10)
