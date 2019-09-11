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
import gamescog
import botConfig

print("Loading...")

bot = commands.Bot(command_prefix='m!')

bot.remove_command("help")
cogs=[]
for file in os.listdir():
    if file[-6:]=="cog.py":
        cogs.append(file[:-3])

async def allowed(ctx):
    if ctx.author.id in [206309860038410240,179292162037514241,365682211376201733]:
        return True
    else:
        return False
localStore={}
@bot.event
async def on_ready():
    print(f"Core: Ready\nRunning on {bot.user.name}\nID: {bot.user.id}")
    await gameFramework.startFramework()
    await bot.change_presence(activity=discord.Game(name=f'{bot.user.name} v0.10'))

@bot.event
async def on_member_join(member):
    await gameFramework.adduser(member)

@bot.event
async def on_member_leave(member):
    await gameFramework.removeuser(member.id)

@bot.event
async def on_message(message):
    try:
        localStore[str(message.author.id)]+=1
    except:
        localStore[str(message.author.id)]=1
    if localStore[str(message.author.id)] == 15:
        await gameFramework.addpoints_leaderboard(str(message.author.id), (await (botConfig.returnReward('per15messages'))))
        localStore[str(message.author.id)]=0

    await bot.process_commands(message)

@bot.group(name="modules", aliases=["mod"], description="Module Management")
@commands.check(allowed)
async def modules(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(":exclamation: You must specify a subcommand.")
    
@modules.command(name="load", aliases=["l"], description="<module> | Loads a module")
async def _load(ctx, specmodule:str):
    if specmodule is None:
        await ctx.send("You must specify a module")
    else:
        bot.load_extension(specmodule)
        await ctx.send(f"Loaded {specmodule}")

@modules.command(name="unload", aliases=["ul"], description="<module> | Unoads a module")
async def _unload(ctx, specmodule:str):
    if specmodule is None:
        await ctx.send("You must specify a module")
    else:
        bot.unload_extension(specmodule)
        await ctx.send(f"Unloaded {specmodule}")

@modules.command(name="reloadall", aliases=["rea"], description=" | Reloads all modules")
async def _reloadall(ctx):
    cogs=[]
    for file in os.listdir():
        if file[-6:]=="cog.py":
            cogs.append(file[:-3])
    for cog in cogs:
        bot.unload_extension(cog)
        bot.load_extension(cog)
    await ctx.send("Finished reloading all modules.")

@modules.command(name="reload", aliases=["re"], description="<module> | Reloads a module")
async def _reload(ctx, specmodule : str):
    if specmodule is None:
        await ctx.send("You must specify a module")
    else:
        bot.unload_extension(specmodule)
        bot.load_extension(specmodule)
        await ctx.send(f"Reloaded {specmodule}")

@modules.error
async def moduleserror(ctx, error):
    if error=="CheckError":
        await ctx.send("❌ | You do not have permission to execute this command")
    else:
        embed=discord.Embed(title="Error", description="An error has occured!", color=0x2d2d2d)
        embed.add_field(name="", value=f"{error}", inline=False)
        await ctx.send(embed=embed)


@bot.command(name="help", description="Returns list of all commands with their usage and description")
async def custom_help(ctx, module=""):
    message = ""
    modules = dict()
    modules['misc'] = []
    for command in bot.commands:
        if type(command) is discord.ext.commands.core.Group:
            modules[command.name.lower()] = command
        else:
            modules['misc'].append(command)

    if module == "":
        message = f"Please specify a module that you would like to look up\n\n"
        for k in sorted(modules.keys()):
            if k == "misc":
                message += f":game_die: **MISC** - `List of commands not grouped`\n\n"
            if k == "play":
                message += f":video_game: **PLAY** - `Gaming commands`\n\n"
            if k == "economy":
                message += f":moneybag: **ECONOMY** - `Economy commands`\n\n"
            if k == "config":
                message += f":gear: **CONFIG** - `Economy commands`\n\n"
            if k == "modules":
                message += f":hammer_pick: **MODULES** - `Cog management`\n\n"
            c = bot.get_command(k)
        return await ctx.send(message)

    if module != "":
        if module.lower() in modules.keys():
            modules = {module.lower(): modules[module.lower()]}
        else:
            message = f"Could not find a module with the name: **{module}**\n"
            return await ctx.send(message)

    for cog, cog_obj in modules.items():
        if cog.lower() in ['misc']:
            sub_message = ""
            sub_message += f"\n**:game_die:  MISCELLANEOUS**\n\n"
            for command in sorted(cog_obj, key=lambda o: f"{o.full_parent_name} {o.name}"):
                if len(command.description.split("|")) >= 2:
                    sub_message += f"**{command.full_parent_name} {command.name} {command.description.split('|')[0]}** | {command.brief or command.description.split('|')[1]}\n"
                else:
                    sub_message += f"**{command.full_parent_name} {command.name}** | {command.brief or command.description}\n"
            if len(message) + len(sub_message) > 2048:
                await ctx.send(message)
                message = ""
        else:
            sub_message = ""
            sub_message += f"\n**{cog_obj.description}  {cog.upper()}**\n\n"
            for command in sorted(cog_obj.commands, key=lambda o: f"{o.full_parent_name} {o.name}"):
                if len(command.description.split("|")) >= 2:
                    sub_message += f"**{command.full_parent_name} {command.name} {command.description.split('|')[0]}** | {command.brief or command.description.split('|')[1]}\n"
                else:
                    sub_message += f"**{command.full_parent_name} {command.name}** | {command.brief or command.description}\n"
            if len(message) + len(sub_message) > 2048:
                await ctx.send(message)
                message = ""
        message += sub_message

    await ctx.send(message)

for cog in cogs:
    bot.load_extension(cog)

with open("token.json", "r+", encoding="UTF-8") as a:
    token = json.loads(a.read())["token"]
bot.run(token)