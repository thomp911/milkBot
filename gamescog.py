import asyncio
import os
import discord
from discord.utils import find
import discord.utils
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
import sys
import math
import random
import requests
import shutil
import string
import time as t
import json
import gameFramework
import botConfig
import gameAdditions
import re
from threading import Thread

async def allowed(ctx):
        if ctx.author.id in [206309860038410240,179292162037514241,365682211376201733]:
            return True
        else:
            return False

#auto games
async def startWordScramble(self):#wordscramble
    startedTime=t.time()
    elaspedTime=0
    fails=0
    completed=False
    word=(await(gameAdditions.wordscramble.get_word()))
    channel=(await(botConfig.returnConfig("wordscrambleChannel")))
    channel=self.bot.get_channel(int(channel))
    def check(m):
        return m.channel.id==channel.id and m.author.id !=self.bot.user.id
    scrambleword=(await (gameAdditions.wordscramble.scramble_word(word)))
    await channel.send(f"Word scramble: `{scrambleword}`")
    #await channel.send(f"debug: word is {word}")
    while elaspedTime<14399: # game lasts maximum of 4 hours (-1 because of the check.)
        elaspedTime=t.time()-startedTime
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)#expires every 30 seconds to check the time.
        except Exception as e:
            ignore=True
        try:
            user=msg.author
        except:
            pass
        try:
            guess=msg.content.lower()
        except:
            pass
        ignore=False
        messages=[]
        async for message in channel.history(limit=2):
            messages.append(message.content)
        if guess==messages[1]:
            ignore=True
        if guess is None or guess == "":
            ignore=True
        if not ignore:
            if guess==word:
                completed=True
            elif guess!=word:
                if len(guess) != len(word):
                    fails+=1
                    await channel.send(f"Incorrect, <@{user.id}>! Your guess does not have the right amount of letters! You have used {fails}/8 attempts.")
                elif sorted(list(guess)) != sorted(list(word)):
                    fails+=1
                    await channel.send(f"Incorrect, <@{user.id}>! Your guess does not have the correct letters! You have used {fails}/8 attempts.")
                else:
                    fails+=1
                    await channel.send(f"Incorrect, <@{user.id}>! Try a new order! You have used {fails}/8 attempts.")
            if completed or fails==8:
                break
    if completed:
        points=(await(botConfig.returnReward('wordscramble')))
        await gameFramework.addpoints_leaderboard(str(user.id),points)
        await channel.send(f"Completed successfully! {user.name} wins {points} points!")
    elif not completed and fails<8:
        await channel.send(f"The word scramble was not completed in time. The word was {word}")
    elif not completed and fails==8:
        await channel.send(f"The word scramble was answered incorrectly too many times. The word was {word}")
    await channel.send("Sending a new word scramble.")
    await startWordScramble(self)#restart it

async def queueDelete(message,time):
    await asyncio.sleep(time)
    await message.delete()

async def count10k(self):#countto10k
    channelid=(await(botConfig.returnConfig('count10kChannel')))
    channel=self.bot.get_channel(int(channelid))
    while True:
        try:
            async for message in channel.history(limit=100):
                if message.author.id != self.bot.user.id:
                    lastuser=message.author
                    lastnumber = int(re.sub('[,]', '', message.content)) #lastnumber is the message content with commas removed
                    break

        except Exception as e:
            print(e)
            lastnumber=0
            lastuser=self.bot.user
        def check(m):
            return m.channel.id == channel.id
        msg = await self.bot.wait_for('message', check=check)

        try:
            int(msg.content)
            cont=True
        except:
            cont=False
            response=await channel.send(f"Send a number, <@{msg.author.id}>!")
            await msg.delete()
            loop = asyncio.get_event_loop()
            loop.create_task(queueDelete(response,3))
        
        if msg.author.id==lastuser.id and cont:#if its the same user
            response=await channel.send(f"Wait for another user, <@{msg.author.id}>!")
            await msg.delete()
            loop = asyncio.get_event_loop()
            loop.create_task(queueDelete(response,3))

        elif int(msg.content)-lastnumber!=1 and cont:#if they went higher than +1
            response=await channel.send(f"Count by one number at a time, <@{msg.author.id}>!")
            await msg.delete()
            loop = asyncio.get_event_loop()
            loop.create_task(queueDelete(response,3))

        if int(msg.content)==10000:#10000 gg
            await msg.add_reaction("🌟")
            await msg.add_reaction("⭐")
            await msg.add_reaction("👏")
            await gameFramework.addpoints_leaderboard(str(msg.author.id), (await(botConfig.returnReward("countto10k_10000"))))
            await channel.send(f"Way to go, <@{msg.author.id}>! Time to start over, everyone!")
            await channel.send("0")

        elif int(msg.content) % 1000==0:#check if its divisable by 1000 
            await msg.add_reaction("⭐")
            await msg.add_reaction("👏")
            await gameFramework.addpoints_leaderboard(str(msg.author.id), (await(botConfig.returnReward("countto10k_1000"))))

        elif int(msg.content) % 100==0:#check if its divisable by 100
            await msg.add_reaction("👏")
            await gameFramework.addpoints_leaderboard(str(msg.author.id), (await(botConfig.returnReward("countto10k_100"))))
    
async def ratepfp(self):
    channelid=(await(botConfig.returnConfig('ratepfpChannel')))
    channel=self.bot.get_channel(int(channelid))
    allowed=["0/10","1/10","2/10","3/10","4/10","5/10","6/10","7/10","8/10","9/10","10/10"]
    async for message in channel.history(limit=1):
        if message.content == "":
            await channel.send(f"Guess I'm first! https://cdn.discordapp.com/avatars/{self.bot.user.id}/{self.bot.user.avatar}.png?size1024")
    def check(m):
        return m.channel.id == channel.id
    while True:
        msg = await self.bot.wait_for('message', check=check, timeout=86400)
        permitted=True
        if msg is None:
            async for message in channel.history(limit=2):
                if message.author.id == self.bot.author.id and "https://" not in message.content:
                    await message.send("I'm not narcissitic or anything, but my pfp is looking finnne. 10/10, Beautiful.")
                else:
                    await channel.send(random.choice(allowed))
        elif msg.content not in allowed:
            await msg.delete()
        else:
            async for message in channel.history(limit=2):
                if f"https://cdn.discordapp.com/avatars/{msg.author.id}/{msg.author.avatar}.png?size1024" in message.content:
                    await msg.delete()
                    permitted=False
            avatar = msg.author.avatar
            if avatar is None:
                await channel.send("I can't seem to get this user's avatar.")
            elif permitted:
                await channel.send(f"https://cdn.discordapp.com/avatars/{msg.author.id}/{avatar}.png?size1024")

async def hangman(self,channel):
    startedTime=t.time()
    elaspedTime=0
    turn=0
    states=gameAdditions.hangman.states
    completed=False
    word,category=(await(gameAdditions.hangman.wordGen()))
    letters=(await(gameAdditions.hangman.getLetters(word)))
    incorrectletters=[]
    knownchars=[]
    for letter in list(word):
        knownchars.append("_")
    def check(m):
        return m.channel.id==channel.id and m.author.id !=self.bot.user.id
    def hangmanReplace(hangman,category,incorrectletters,knownchars):
        il=''
        kc=''
        for letter in incorrectletters:
            il+=f"{letter} "
        for letter in knownchars:
            kc+=f"{letter} "
        
        hangman=hangman.replace("%C", category)
        hangman=hangman.replace("%W", il)
        hangman=hangman.replace("%P", kc)
        return hangman

    gameInstance=await channel.send(f"```{hangmanReplace(states[turn],category,incorrectletters,knownchars)}```")#start game instance
    while elaspedTime<28799: # game lasts maximum of 8 hours (-1 because of the check.)
        elaspedTime=t.time()-startedTime
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)#expires every 30 seconds to check the time.
        except Exception as e:
            print(e)
        try:
            guess=msg.content.lower()
        except:
            guess=""

        if guess==word:#wow got the word
            completed=True
            await gameInstance.edit(content=f"```{hangmanReplace(states[7],category,incorrectletters,list(word))}```")
            points=(await(botConfig.returnReward('hangmanword')))
            await gameFramework.addpoints_leaderboard(str(msg.author.id), points)
            await channel.send(f"Congratulations, <@{msg.author.id}> you have been awarded {points} points for guessing the hangman correctly!")
            break

        elif guess!=word:#letter guess
            if len(guess) == 1:#letter only
                if guess in letters:#is the one letter in the letters?
                    letter=guess
                    for value in (await(gameAdditions.hangman.giveLetterOccurences(letter,word))):#get all index values of the letter thats found
                        knownchars[value]=word[value] # replace all the unknown characters with those that are known
                    await gameInstance.edit(content=f"```{hangmanReplace(states[turn],category,incorrectletters,knownchars)}```")#update the game
                    await gameFramework.addpoints_leaderboard(str(msg.author.id),(await(botConfig.returnReward('hangmanletter')))) # add points for guessing letter
                else:
                    turn+=1
                    incorrectletters.append(guess)
                    await gameInstance.edit(content=f"```{hangmanReplace(states[turn],category,incorrectletters,knownchars)}```")
        try:
            await msg.delete()
        except:
            pass
        if knownchars==letters:#has word been found?
            await gameInstance.edit(content=f"```{hangmanReplace(states[7],category,incorrectletters,list(word))}```")
            points=(await(botConfig.returnReward('hangmanword')))
            await gameFramework.addpoints_leaderboard(str(msg.author.id), points)
            await channel.send(f"Congratulations, <@{msg.author.id}> you have been awarded {points} points for guessing the hangman correctly!")
            break
        if turn==6:
            break

    await channel.send("Sending a new hangman in 5 seconds...")
    await asyncio.sleep(5)
    await hangman(self, channel)#restart it


class games(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name="request", description="<word> <category> | Request for a word to be added to hangman!")
    async def request(self,ctx,word:str=None,category:str=None):
        if word is None or word =="":
            return await ctx.send("You must specify a word!")
        await ctx.send("Request made.")
        channelid=(await(botConfig.returnConfig("wordRequestChannel")))
        channel=self.bot.get_channel(int(channelid))
        def embedMake(word,category,color,footer):
            embed=discord.Embed(title="New word request", description="React to approve or disapprove.", color=color)
            embed.add_field(name="Word", value=f"{word}", inline=True)
            embed.add_field(name="Category", value=f"{category}", inline=True)
            embed.set_footer(text=footer)
            return embed
        sent=await channel.send(embed=embedMake(word,category,0xffff00,"Pending..."))
        await sent.add_reaction('👍')
        await sent.add_reaction('👎')
        def check(reaction,user):
            return str(reaction.message) == str(sent) and user != self.bot.user
        completed=False
        while completed is False:
            reaction,user = await self.bot.wait_for('reaction_add',check=check)
            if str(reaction.emoji)=="👍":
                await sent.edit(embed=embedMake(word,category,0x00ff00,"Approved."))
                await botConfig.addHangmanWord(word,category)
                completed=True
            elif str(reaction.emoji)=="👎":
                await sent.edit(embed=embedMake(word,category,0xff0000,"Denied."))
                completed=True

    @commands.group(name="play", description="<game> | Play a game!")
    async def gplay(self, ctx):
        if ctx.invoked_subcommand is None:
            message="You didn't specify a game! Pick one from:\n"
            for command in sorted(ctx.command.commands, key=lambda o: f"{o.full_parent_name} {o.name}"):
                message += f"**{command.name} {command.description.split('|')[0]}** | {command.brief or command.description.split('|')[1]}\n"
            await ctx.send(message)

    @commands.command(name="leaderboard", aliases=["l"], description="| Returns the leaderboard.")
    async def leaderboard(self,ctx):
        leaderboard = gameFramework.getLeaderboard()
        message="```Position | Username | points"
        pos=0
        for user in leaderboard:
            pos+=1
            username=self.bot.get_user(int(user))
            message+=f"\n{pos} | {username.name}#{username.discriminator} | {leaderboard[user]}"
            if pos==10:
                break
        message+=f"\n\n{gameFramework.getRank(str(ctx.author.id))} | {ctx.author.name}#{ctx.author.discriminator} | {leaderboard[str(ctx.author.id)]}"
        message+="```"
        await ctx.send(message)

    @commands.command(name="rank", aliases=["r"], description="<user> | Returns the specified user's rank. If no user is specified, the author is assumed the user.")
    async def returnrank(self,ctx,user:discord.User=None):
        if user is None:
            user=str(ctx.author.id)
        else:
            user=str(user.id)
        rank = gameFramework.getRank(user)
        points = gameFramework.getLeaderboard()[user]
        await ctx.send(f"`Your rank is: {rank} with: {points} points.`")

    ##############################    --- GAMES ---    ##############################

    @gplay.command(name="startautogames",description="| Starts the auto games (owner/dev only)")
    @commands.check(allowed)
    async def startautogames(self,ctx):
        await ctx.send("Starting auto games...")
        loop = asyncio.get_event_loop()
        try:
            for x in range(1,4):
                channel=(await(botConfig.returnConfig(f"hangman{x}Channel")))
                channel=self.bot.get_channel(int(channel))
                loop.create_task(hangman(self, channel))
        except Exception as e:
            print(e)
            return await ctx.send(f"An error occured while starting hangman{x}, you may need to set the channel. Use")


        if (await(botConfig.returnConfig('ratepfpChannel'))) == 0 or (await(botConfig.returnConfig('ratepfpChannel'))) is None:
            return await ctx.send("You have not set a channel for `ratepfp` to operate, use `m!config setchannel ratepfp <channel>` to do so.")
        else:
            loop.create_task(ratepfp(self))
        
        if (await(botConfig.returnConfig('count10kChannel'))) == 0 or (await(botConfig.returnConfig('count10kChannel'))) is None:
            return await ctx.send("You have not set a channel for `count10k` to operate, use `m!config setchannel count10k <channel>` to do so.")
        else:
            loop.create_task(count10k(self))

        if (await(botConfig.returnConfig('count10kChannel'))) == 0 or (await(botConfig.returnConfig('wordscrambleChannel'))) is None:
            return await ctx.send("You have not set a channel for `wordscramble` to operate, use `m!config setchannel wordscramble <channel>` to do so.")
        else:
            loop.create_task(startWordScramble(self))

    #Guessing game

    @gplay.command(name="guess-my-number", aliases=["guess"], description=" <wager> | Number Guessing game")
    async def guess(self,ctx, wager:int=None):
        if wager is None:
            return await ctx.send("You must specify a wager.")
        if wager>(await (gameFramework.getpoints(str(ctx.author.id)))):
            return await ctx.send("You do not have enough to wager this.")
        await gameFramework.rempoints_leaderboard(str(ctx.author.id), wager)
        number=random.randint(1,10)
        await ctx.send("I'm thinking of a number from 1 to 10, can you guess?")
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        
        msg = await self.bot.wait_for('message', check=check)
        if msg.content==str(number):
            await gameFramework.addpoints_leaderboard(str(ctx.author.id), wager*2)
            await ctx.send(f"Correct! You win {wager*2} points! Congratulations!")
        else:
            await ctx.send("Incorrect!")

    #Blackjack

    @gplay.command(name="blackjack",aliases=["bj"], description="<wager> | A game of blackjack")
    async def blackjack(self,ctx,wager:int=None):
        #define cards
        gambleChannel=(await (botConfig.returnConfig('gambleChannel')))
        if ctx.channel.id != int(gambleChannel):
            msg=await ctx.send(f"You must do that in <#{gambleChannel}>")
            await asyncio.sleep(5)
            await msg.delete()
            return await ctx.message.delete()
        elif wager is None:
            return await ctx.send("You must specify a wager.")
        elif wager>(await (gameFramework.getpoints(str(ctx.author.id)))):
            return await ctx.send(f"You do not have points enough to wager {wager}.")
        await gameFramework.rempoints_leaderboard(str(ctx.author.id), wager)
        deck = list('234567890JQKA'*4)
        random.shuffle(deck)
        player_cards = [deck.pop() for x in range(2)]
        bot_cards = [deck.pop() for x in range(2)]
        values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
         '9':9, '0':10, 'J':10, 'Q':10, 'K':10, 'A':1}
        #send initial game embed
        def makeEmbed(footer):
            embed=discord.Embed(title="Blackjack", color=0xff0000)
            embed.add_field(name=f"{ctx.author.name}", value=f"{gameAdditions.blackjack.listPrint(player_cards)}\nTotal:{sum(values[card] for card in player_cards)}", inline=True)
            embed.add_field(name="Bot", value=f"{gameAdditions.blackjack.listPrint(bot_cards)}\nTotal:{sum(values[card] for card in bot_cards)}", inline=True)
            embed.set_footer(text=footer)
            return embed

        if sum(values[card] for card in player_cards)==21:
            blackjack_game=await ctx.send(embed=makeEmbed(f"The player has 21, the player wins {wager*2} points!"))
            await gameFramework.addpoints_leaderboard(str(ctx.author.id), wager*2)
        elif sum(values[card] for card in bot_cards)==21:
            blackjack_game=await ctx.send(embed=makeEmbed(f"The bot has 21, the bot wins!"))

        blackjack_game=await ctx.send(embed=makeEmbed("Type hit or stand."))

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        while True:

            if sum(values[card] for card in bot_cards)<18:
                if random.randint(0,1)==0:
                    bot_cards.append(deck.pop())
                    if sum(values[card] for card in bot_cards)>21:
                        await gameFramework.addpoints_leaderboard(str(ctx.author.id), wager*2)
                        return await blackjack_game.edit(embed=makeEmbed(f"The player is closest to 21, the player wins {wager*2} points!"))

            response=await self.bot.wait_for('message', check=check)

            if response.content.lower() == "hit":
                player_cards.append(deck.pop())

                isBust=sum(values[card] for card in player_cards)>21

                if isBust:
                    return await blackjack_game.edit(embed=makeEmbed("You are bust! The bot wins!"))
                else:
                    await blackjack_game.edit(embed=makeEmbed("You hit"))

            elif response.content.lower() == "stand":
                await blackjack_game.edit(embed=makeEmbed("You stuck."))
                if sum(values[card] for card in player_cards) > sum(values[card] for card in bot_cards):
                    await gameFramework.addpoints_leaderboard(str(ctx.author.id), wager*2)
                    return await blackjack_game.edit(embed=makeEmbed(f"The player is closest to 21, the player wins {wager*2} points!"))
                elif sum(values[card] for card in player_cards) == sum(values[card] for card in bot_cards):
                    await gameFramework.addpoints_leaderboard(str(ctx.author.id), wager)
                    return await blackjack_game.edit(embed=makeEmbed("Draw! All wagers have been returned."))
                else:
                    return await blackjack_game.edit(embed=makeEmbed("The bot is closest to 21, the bot wins."))

def setup(bot):
    bot.add_cog(games(bot))