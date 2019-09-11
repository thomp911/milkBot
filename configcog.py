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
import time
import json
import gameFramework
import botConfig

async def allowed(ctx):
        if ctx.author.id in [206309860038410240,179292162037514241,365682211376201733]:
            return True
        else:
            return False

class config(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.group(name="config",description="Configuration for the bot.")
    @commands.check(allowed)
    async def config(self,ctx):
        if ctx.invoked_subcommand is None:
            message=""
            for command in sorted(ctx.command.commands, key=lambda o: f"{o.full_parent_name} {o.name}"):
                message += f"**{command.full_parent_name} {command.name} {command.description.split('|')[0]}** | {command.brief or command.description.split('|')[1]}\n"
            await ctx.send(message)
    
    @config.command(name="setreward", description="<game> <amount> | Sets the reward amount for a specific game.")
    async def setreward(self,ctx,game:str=None,amount:int=None):
        if game is None:
            return await ctx.send("You must specify a game.")
        if amount is None:
            return await ctx.send("You must specify an amount.")
        if game.lower().capitalize() not in gameFramework.listGames():
            return await ctx.send("That game is not recognised.")
        await botConfig.setReward(game, amount)
        await ctx.send(f"Successfully set the reward for {game} to {amount}")
    
    @config.command(name="setchannel", description="<function/game> <channel> | Sets a specific channel for a specific function if applicable.")
    async def setchannel(self,ctx,game:str=None,channel:discord.TextChannel=None):
        if game is None:
            return await ctx.send("You must specify a game.")
        if channel is None:
            return await ctx.send("You must specify a channel.")
        try:
            await botConfig.setConfig(f"{game.lower()}Channel",str(channel.id))
            await ctx.send(f"Successfully set the channel for {game} to {channel.name}")
        except:
            await ctx.send(f"{game.capitalize()} is not recognised as a function/game that has a specific channel type.")
    
    @config.command(name="resetconfig", description="| Resets all configuration.")
    async def resetconfig(self,ctx):
        await ctx.send("Are you sure you wish to reset all configuration? [Y/N]")
        def check(m):
            return m.author==ctx.author
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
        except:
            pass
        if msg.content.lower()=="y":
            await botConfig.resetConfig()
            await ctx.send("Reset.")
        else:
            await ctx.send("Cancelled.")

    @config.error
    async def conferror(self, ctx, error):
        if isinstance(error, commands.CheckFailure): #Not allowed
            await ctx.send("❌ | You do not have permission to execute this command")
        else:
            embed=discord.Embed(title="Error", description="An error has occured!", color=0x2d2d2d)
            embed.add_field(name="Error", value=f"{error}", inline=False)#
            embed.set_footer(text=datetime.utcnow())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(config(bot))