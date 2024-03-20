import discord
from discord.ext import commands
from discord.commands import slash_command

class Testing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Testing Cog Loaded")

    # @slash_command(description="Create a signup embed for squadron battles.")
    # async def test_embed(self, ctx, br: discord.Option(str, description='Battle Rating'), window: discord.Option(str, description='SRB Window', choices=['US', 'EU']),):
    #     try:
    #         msg = await ctx.respond(role.mention, embed=embed)
    #     except Exception as e:
    #         self.bot.logging.error(e)
    #         await ctx.respond('An error has occurred')


def setup(client):
    client.add_cog(Testing(client))