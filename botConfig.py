import asyncio
import os
import sys
import math
import random
import requests
import shutil
import time as t
import json

defaultconf={
    "wordscrambleChannel":'0',
    "gambleChannel":'0',
    "count10kChannel":'0',
    "ratepfpChannel":'0',
    "hangman1Channel":'0',
    "hangman2Channel":'0',
    "hangman3Channel":'0',
    "wordRequestChannel":'0'

}

async def returnConfig(query):
    with open("config.json", "r", encoding="UTF-8") as c:
        c=json.loads(c.read())
        try:
            return c[query]
        except:
            return 'None'

async def returnReward(query):
    with open("rewards.json", "r", encoding="UTF-8") as r:
        r=json.loads(r.read())
        try:
            return r[query]
        except:
            return 'None'

async def setReward(game,amount):
    with open("rewards.json", "r", encoding="UTF-8") as r:
        r=json.loads(r.read())
    r[game]=amount
    with open("rewards.json", "w", encoding="UTF-8") as r2:
        json.dump(r,r2)

async def setConfig(key,value):
    with open("config.json", "r", encoding="UTF-8") as c:
        c=json.loads(c.read())
    c[key]=value
    with open("config.json", "w", encoding="UTF-8") as c2:
        json.dump(c,c2)
    
async def resetConfig():
    with open("config.json", "w", encoding="UTF-8") as c:
        json.dump(defaultconf,c)

async def addHangmanWord(word,category):
    with open("hangmanwords.json", "r", encoding="UTF-8") as h:
        words=json.loads(h.read())
    
    words[word]=category
    with open("hangmanwords.json", "w",encoding="UTF-8") as h:
        words=json.dump(words, h)
