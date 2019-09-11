import asyncio
import os
import sys
import random
import requests
import shutil
import time as t
import json


async def startFramework():
    await updateLeaderboard()
    print("Game framework Initalized.")

async def addpoints_leaderboard(user, points):
    with open("leaderboard.json", "r", encoding="UTF-8") as l:
        l=json.loads(l.read())
        if await userExists(l,user):
            l[user]+=points #add the points
        else:
            l[user]=points
    with open("leaderboard.json", "w+", encoding="UTF-8") as l2:
        json.dump(l,l2) # l is the updated dict, l2 is the file, dont get confused 9Head
    await updateLeaderboard()

async def rempoints_leaderboard(user, points):
    with open("leaderboard.json", "r", encoding="UTF-8") as l:
        l=json.loads(l.read())
        if await userExists(l,user):
            l[user]-=points #remove the points
        else:
            l[user]=0-points
    with open("leaderboard.json", "w+", encoding="UTF-8") as l2:
        json.dump(l,l2) # l is the updated dict, l2 is the file, dont get confused 9Head
    await updateLeaderboard()

async def getpoints(user):
    with open("leaderboard.json", "r", encoding="UTF-8") as l:
        l=json.loads(l.read())
    return l[user]

async def adduser(user):
    with open("leaderboard.json", "r", encoding="UTF-8") as l:
        l=json.loads(l.read())
        l[str(user.id)]=0
    with open("leaderboard.json", "w+", encoding="UTF-8") as l2:
        json.dump(l,l2)

async def removeuser(user):
    with open("leaderboard.json", "r", encoding="UTF-8") as l:
        l=json.loads(l.read())
        del l[str(user.id)]
    with open("leaderboard.json", "w+", encoding="UTF-8") as l2:
        json.dump(l,l2)

async def userExists(l,user):
    if user in l:
        return True
    else:
        return False

async def updateLeaderboard():
    with open("leaderboard.json", "r", encoding="UTF-8") as l:
        l=json.loads(l.read())
        sorted_leaderboard = dict(sorted(l.items(), key=lambda kv: kv[1],reverse=True)) #Sorts the dictionary so the leaderboard makes sense.
    with open("leaderboard.json", "w", encoding="UTF-8") as l:
        json.dump(sorted_leaderboard, l)

def getLeaderboard():
    with open("leaderboard.json", "r", encoding="UTF-8") as l:
        l=json.loads(l.read())
    return l

def getBalance(user):
    l=getLeaderboard()
    return l[user]

def getRank(checkuser):
    l=getLeaderboard()
    pos=0
    for user in l:
        pos+=1
        if checkuser==user:
            break
    return pos
