import discord
from discord.ext import commands
import os
# USES PY-CORD DISCORD LIBRARY

#bot intents to allow for getting info
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

#token allows to sign in to the bot account
TOKEN = str(os.environ.get('BOT_TOKEN'))

#loads cogs from ./cogs folder
for file in os.listdir('./mush-bot/cogs'):
    if file.endswith('.py'):
        bot.load_extension("cogs." + file[:-3])

#on boot function
@bot.event
async def on_ready():
    print("logged in and ready")

#on join function to send the new member form
@bot.event
async def on_member_join(ctx):
    #sends message in new members in mush, if test bot, then test server channel
    try:
        join_channel = await bot.fetch_channel(970370019701690468)#new members chat in mush
    except: 
        join_channel = await bot.fetch_channel(993562809994584197)#new members chat in test server

    await join_channel.send(f'{ctx.mention}\n {bot.join_message}')

@bot.slash_command(description="test if the bot is working")
async def test(ctx):
    await ctx.respond("Operational")

#run bot
bot.run(TOKEN)