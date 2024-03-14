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

    #     role = discord.utils.get(ctx.guild.roles, name = 'Mussh Members')
        
    #     embed = discord.Embed(
    #         title=f'Sign up for {window} {br} SRB',
    #         description='Mark your attendance below.',
    #         color=discord.Colour.from_rgb(255, 255, 255)
    #     )
        
    #     msg = await ctx.respond(role.mention, embed=embed)


def setup(client):
    client.add_cog(Testing(client))