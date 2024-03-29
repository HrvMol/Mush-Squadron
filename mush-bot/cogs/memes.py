import discord
from discord.ext import commands
from discord.commands import slash_command
import random
import datetime

class Memes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Db Cog Loaded")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author != self.bot.user:
            if random.randint(0, 2500) == 1:
                await ctx.channel.send("fuck you")


        
    @slash_command()
    async def scotsman(self, ctx):
        await ctx.respond("https://cdn.discordapp.com/attachments/987513534227316789/1003431507597205584/received_272561204831416.jpeg")

    @slash_command()
    async def posh(self, ctx):
        await ctx.respond("https://cdn.discordapp.com/attachments/987513534227316789/1005955570991370380/unknown.png")
    
    @slash_command()
    async def russianbias(self, ctx):
        await ctx.respond("https://tinyurl.com/4e2x43nd")
    
    @slash_command()
    async def salty(self, ctx):
        await ctx.respond("2 world wars, 1 world cup and one womens Euros \nhttps://static.independent.co.uk/2021/06/30/15/crying-girl.jpg?width=1200")
    
    @slash_command()
    async def potatoes(self, ctx):
        await ctx.respond("POV: you voted Tories \nhttps://tenor.com/73O7.gif")
    
    @slash_command()
    async def nephew(self, ctx):
        await ctx.respond("head of dinosaurs \nhttps://tinyurl.com/bdfmkupv")
    
    @slash_command()
    async def best(self, ctx):
        await ctx.respond("back Boris \nhttps://tinyurl.com/5yrzz5x6")

    @slash_command()
    async def economy(self, ctx):
        await ctx.respond('https://tenor.com/h83HQdByMTa.gif')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        try:
            if '/cum' in ctx.content:
                await ctx.author.timeout_for(datetime.timedelta(minutes=10), reason='Engaging in forbidden activity')
        except Exception as e:
            self.bot.logging.exception('')

def setup(client):
    client.add_cog(Memes(client))