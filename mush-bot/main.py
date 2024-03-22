#!/usr/bin/env python
# tells linux that it is a python file

import discord
from discord.ext import commands
import os
from database import Settings
import sys
import aiofiles
import socket
# USES PY-CORD DISCORD LIBRARY
import logging

if sys.platform == "linux":
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind('\0postconnect_gateway_notify_lock')
    except socket.error as e:
        error_code = e.args[0]
        error_string = e.args[1]
        print("Process already running (%d:%s ). Exiting" % (error_code, error_string))
        sys.exit(0)

#bot intents to allow for getting info
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

if "mush-bot" not in os.getcwd().lower():
    os.chdir(os.getcwd()+"/Mush-Squadron/mush-bot")
    # os.chdir(os.getcwd()+"/mush-bot")

bot.join_message = ''

bot.settings = Settings

logging.basicConfig(filename='app.log', format='%(asctime)s - %(levelname)s - %(funcName)s() - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
bot.logging = logging

#token allows to sign in to the bot account
TOKEN = str(os.environ.get('BOT_TOKEN'))

#loads cogs from ./cogs folder
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension("cogs." + file[:-3])

#on boot function
@bot.event
async def on_ready():
    #reads join_message file and puts data into join_message list
    async with aiofiles.open("join_message.txt", mode="r") as file:
        bot.join_message = await file.read()

    print("logged in and ready")

#on join function to send the new member form
@bot.event
async def on_member_join(ctx):
    try:
        #sends message in new members in mush, if test bot, then test server channel
        try:
            join_channel = await bot.fetch_channel(970370019701690468)#new members chat in mush
        except: 
            join_channel = await bot.fetch_channel(1128381656609341442)#new members chat in test server
    except Exception as e:
        logging.error(e)

    await join_channel.send(f'{ctx.mention}\n {bot.join_message}')

@bot.slash_command(description="test if the bot is working")
async def test(ctx):
    await ctx.respond("Operational")

#run bot
bot.run(TOKEN)
