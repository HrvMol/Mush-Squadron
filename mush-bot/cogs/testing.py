import discord
from discord.ext import commands
from discord.commands import slash_command
import requests
import json

class Testing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Testing Cog Loaded")

    @slash_command(description="test if the api is working")
    async def api(self, ctx, discord_id: discord.Option(str, description='make a query to the api')):
        # jsonQuery = f'"query":"{query}"'
        # jsonQuery = '{' + jsonQuery + '}'

        # print(json.loads(jsonQuery))
        # x = requests.post("http://localhost:5000/users", json=json.loads(jsonQuery))
        
        x = requests.get(f"http://localhost:5000/users/{discord_id}")

        await ctx.respond(f'Response: {x.text}')


def setup(client):
    client.add_cog(Testing(client))