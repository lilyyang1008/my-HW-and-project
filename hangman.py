# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:14:40 2024

@author: user
"""

import random
from words import words
import string

#%%
def get_valid_word(words):
    word=random.choice(words) #randomly chooses the word from the list
    while '-' in word or ' ' in word:
        word=random.choice(words)
        
    return word.upper()

def hangman():
    word=get_valid_word(words)
    word_letters=set(word) #letters in the word
    alphabet=set(string.ascii_uppercase)
    used_latters=set() #what the user has guess
    
    lives=10
    
    while len(word_letters)>0 and lives>0:
        print("Yor have", lives," used those letters:"," ".join(used_latters))
        #current word
        word_list = [letter if letter in used_latters else '-' for letter in word]
        print("Current word:"," ".join(word_list))
        #get the input from user
        user_latter=input("guess a latter:").upper()
        if user_latter in alphabet-used_latters:
            used_latters.add(user_latter)
            if user_latter in word_letters:
                word_letters.remove(user_latter)
            else:
                lives=lives-1
                print("Letter is not in word")
        elif user_latter in used_latters:
            print("You have already used that character.Please try again.")
        else:
            print("Invalid character")
    #when len(word_letters)==0 or lives==0 
    if lives==0:
        print("Sorry,you are dead!.The word was",word)
    else:
        print("You guessed the word",word,"!")
hangman()