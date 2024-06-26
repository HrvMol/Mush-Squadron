import discord
from discord.ext import commands
from discord.commands import slash_command

class Testing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Testing Cog Loaded")


def setup(client):
    client.add_cog(Testing(client))