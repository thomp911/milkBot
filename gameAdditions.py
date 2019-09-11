import asyncio
import os
import sys
import math
import random
import requests
import shutil
import time as t
import json

#anything needed multiple times or just a long function during the runtime of a game

class blackjack: #
    
    def listPrint(a):
        b=""
        for value in a:
            if value == "0":
                b+=f"`10` "
            elif value == "K":
                b+="`King` "
            elif value == "Q":
                b+="`Queen` "
            elif value == "J":
                b+="`Jack` "
            elif value == "A":
                b+="`Ace` "
            else:
                b+=f"`{value}` "
        return b

class hangman:
    states=[
r"""
-------__HANGMAN__-------
         ________
       []       |
       []      
       []                          
       []       
 ______[]___
|           |__________
|                      |
|______________________|
SUBJECT:%C
( 6 GUESSES LEFT )
PHRASE:%P
""",#0
r"""
-------__HANGMAN__-------
         ________
       []       |
       []       0
       []                          
       []       
 ______[]___
|           |__________
|                      |
|______________________|
SUBJECT:%C
( 5 GUESSES LEFT )
INCORRECT LETTERS: %W
        
        
PHRASE:%P
""",#1
r"""
-------__HANGMAN__--------
         ________
       []       |
       []       0
       []       |                   
       []      /
 ______[]___
|           |__________
|                      |
|______________________| 
SUBJECT:%C
( 3 GUESSES LEFT )
INCORRECT LETTERS: %W
        
PHRASE:%P
""",#2
r"""
-------__HANGMAN__--------
        ________
       []       |
       []       0
       []       |                   
       []      /
 ______[]___
|           |__________
|                      |
|______________________| 
SUBJECT:%C
( 3 GUESSES LEFT )
INCORRECT LETTERS: %W
        
PHRASE:%P
""",#3
r"""
-------__HANGMAN__---------
         ________
       []       |
       []       0
       []       |                   
       []      / \
 ______[]___
|           |__________
|                      |
|______________________|
SUBJECT:%C
( 2 GUESSES LEFT )
INCORRECT LETTERS: %W 
        
PHRASE:%P
""",#4
r"""
-------__HANGMAN__-------
         ________
       []       |
       []      \0
       []       |                   
       []      / \
 ______[]___
|           |__________
|                      |
|______________________|
SUBJECT:%C
( 1 GUESS LEFT )
INCORRECT LETTERS: %W
        
PHRASE:%P
""",#5
r"""
-------__HANGMAN__-------
         ________
       []       |
       []      \0/
       []       |                   
       []      / \
 ______[]___
|           |__________
|                      |
|______________________| 
SUBJECT:%C
( REST IN PEACE )
INCORRECT LETTERS: %W
        
PHRASE:%P
""",#6
r"""
-------__HANGMAN__-------
        ________
       []       |
       []     
       []                        
       []         \0/
 ______[]___       |
|           |_____/_\__
|                      |
|______________________|
( YAY! YOU  SAVED HANGMAN! )
        
PHRASE:%P
"""#7
        ]

    async def wordGen():
        with open("hangmanwords.json","r",encoding="UTF-8") as h:
            words=json.loads(h.read())
            word = random.choice(list(words.keys()))
            category = words[word]
            return [word,category]

    async def getLetters(word):
        letters = []
        for letter in word:
            if letter not in letters:
                letters.append(letter)
        return letters
    
    async def giveLetterOccurences(letter, word):
        word=list(word)
        return [index for index, value in enumerate(word) if value == letter]

class wordscramble:
    async def get_word():
        with open("wordscramble.json", "r", encoding="UTF-8") as words:
            words=json.loads(words.read())
            return random.choice(words)

    async def scramble_word(word):
        word=list(word)
        random.shuffle(word)
        return ''.join(word)
