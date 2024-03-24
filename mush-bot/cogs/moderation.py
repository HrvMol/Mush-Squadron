from discord import Option
from discord.ext import commands
from discord.commands import slash_command

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation Cog Loaded")

    # Purge command
    @slash_command(description="remove a certain number of messages")
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, messages: Option(int, description="How may messages do you want to purge?", requires=True)):
        try:
            # deletes selected number of messages
            i = await ctx.channel.purge(limit = messages)
            await ctx.respond(f'I have purged {len(i)} messages')
        except Exception as e:
            self.bot.logging.exception('')
            await ctx.respond('An error has occurred')

    # @slash_command(description="update a setting")
    # async def settings(self, ctx):
    #     self.bot.settings.updateSetting('a', 'b')
    #     await ctx.respond(f'Modified Setting')

def setup(client):
    client.add_cog(Moderation(client))