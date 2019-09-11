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

class economy(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    async def on_ready(self):
        print("Cog - Games: Ready")

    @commands.group(name="economy", aliases=["e","eco"],description="Economy commands")
    async def economy(self,ctx):
        if ctx.invoked_subcommand is None:
            message=""
            for command in sorted(ctx.command.commands, key=lambda o: f"{o.full_parent_name} {o.name}"):
                message += f"**{command.full_parent_name} {command.name} {command.description.split('|')[0]}** | {command.brief or command.description.split('|')[1]}\n"
            await ctx.send(message)
    
    @economy.command(name="pay",description="<user> <amount> | Pay a user a certain amount of points.")
    async def pay(self,ctx,user:discord.User=None,amount:int=None):
        if user is None:
            return await ctx.send("You must specify a user.")
        if amount is None:
            return await ctx.send("You must specify an amount.")
        if (await(gameFramework.getpoints(str(ctx.author.id))))<amount:
            return await ctx.send(f"You do not have enough points to pay {user.name} {amount}.")
    
        await gameFramework.rempoints_leaderboard(str(ctx.author.id),amount)
        await gameFramework.addpoints_leaderboard(str(user.id), amount)
        await ctx.send(f"{amount} points has successfully been paid to {user.name}.")

    @economy.command(name="bal",description="<user> | Returns balance of specified user.")
    async def bal(self,ctx,user:discord.User=None):
        if user is None:
            user=ctx.author
        return await ctx.send(f"User {user.name} has {gameFramework.getBalance(str(user.id))} points.")


    @economy.group(name="admin", description="| Economy administration")
    @commands.check(allowed)
    async def dev(self,ctx):
        if ctx.invoked_subcommand is None:
            message=""
            for command in sorted(ctx.command.commands, key=lambda o: f"{o.full_parent_name} {o.name}"):
                message += f"**{command.full_parent_name} {command.name} {command.description.split('|')[0]}** | {command.brief or command.description.split('|')[1]}\n"
            await ctx.send(message)

    @dev.command(name="addpoints", description="<user> <points> | Force add a points")
    async def addpoints(self,ctx, user:discord.User=None, points:int=None):
        await gameFramework.addpoints_leaderboard(str(user.id), points)
        await ctx.send(f"Successfully added {points} to {user.name}")

    @dev.command(name="removepoints", description="<user> <points | Force remove a points")
    async def rempoints(self,ctx, user:discord.User=None, points:int=None):
        await gameFramework.rempoints_leaderboard(str(user.id), points)
        await ctx.send(f"Successfully removed {points} from {user.name}")

    @dev.command(name="resetpoints", description="<user>| Resets a users points. (Or leave empty to reset everyone)")
    async def resetpoints(self,ctx,user:discord.User=None):
        if user is None:
            await ctx.send("Are you sure you wish to reset all users points? [Y/N]")
            def check(m):
                return m.author==ctx.author
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
            except:
                pass
            if msg.content.lower()=="y":
                with open("leaderboard.json", "w+", encoding="UTF-8") as l:
                    json.dump(dict(), l)
                for user in self.bot.users:
                    await gameFramework.adduser(user)
            else:
                await ctx.send("Cancelled.")
        else:
            bal=await gameFramework.getBalance(str(user.id))
            await gameFramework.rempoints_leaderboard(str(user.id), bal)

    @dev.error
    async def deverror(self, ctx, error):
        if isinstance(error, commands.CheckFailure): #Not allowed
            await ctx.send("❌ | You do not have permission to execute this command")
        else:
            embed=discord.Embed(title="Error", description="An error has occured!", color=0x2d2d2d)
            embed.add_field(name="Error", value=f"{error}", inline=False)#
            embed.set_footer(text=datetime.utcnow())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(economy(bot))