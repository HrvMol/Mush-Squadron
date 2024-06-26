import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
from cogs.db import connect, close, databaseUpdate

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(PaginationView())
        print("Moderation Cog Loaded")

    # Purge command
    @slash_command(description="Remove a certain number of messages")
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, messages: Option(int, description="How may messages do you want to purge?", requires=True)): # type: ignore
        try:
            # deletes selected number of messages
            i = await ctx.channel.purge(limit = messages)
            await ctx.respond(f'I have purged {len(i)} messages')
        except Exception as e:
            self.bot.logging.exception('')
            await ctx.respond('An error has occurred')

    # @slash_command(description="Display a list of the order in which members should be removed from the squadron")
    # @commands.has_permissions(administrator = True)
    # async def removal_list(self, ctx):
    #     try:
            
    #     except:
    #         self.bot.logging.exception('')
    #         await ctx.respond('An error has occurred')

    @slash_command(description="Display the list of people who are not in the discord")
    @commands.has_permissions(administrator = True)
    async def no_discord_list(self, ctx):
        try:
            # get data
            embed = CreateEmbed('SELECT player FROM webscraper WHERE (in_discord IS NULL or in_discord = %s) and in_squadron = %s ORDER BY entry_date DESC;', (False, True))
            view = PaginationView()

            # set start info
            currentPage = 1
            finalPage = len(embed)

            button = discord.ui.Button(label=f'{currentPage} / {finalPage}')
            button.disabled = True

            # put page button in the middle of the 1st row
            midpoint = len(view.children)//4
            view.children = view.children[0:midpoint] + [button] + view.children[midpoint:] 

            await ctx.respond(embed=embed[1], view=view)
        except:
            self.bot.logging.exception('')
            await ctx.respond('An error has occurred')

    # @slash_command(description="update a setting")
    # async def settings(self, ctx):
    #     self.bot.settings.updateSetting('a', 'b')
    #     await ctx.respond(f'Modified Setting')

class PaginationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='<<', custom_id='first', style=discord.ButtonStyle.blurple)
    async def button1_callback(self, button, interaction):
        # setting current page
        nextPage = 1
        await handleButtons(self, interaction, nextPage)
        
    @discord.ui.button(label='<', custom_id='prev', style=discord.ButtonStyle.red)
    async def button2_callback(self, button, interaction):
        # setting current page
        nextPage = int(interaction.message.components[0].children[2].label.split('/')[0].strip()) - 1
        await handleButtons(self, interaction, nextPage)

    @discord.ui.button(label='>', custom_id='next', style=discord.ButtonStyle.green)
    async def button4_callback(self, button, interaction):
        # setting current page
        nextPage = int(interaction.message.components[0].children[2].label.split('/')[0].strip()) + 1
        await handleButtons(self, interaction, nextPage)
    
    @discord.ui.button(label='>>', custom_id='last', style=discord.ButtonStyle.blurple)
    async def button5_callback(self, button, interaction):
        # setting current page
        finalPage = int(interaction.message.components[0].children[2].label.split('/')[1].strip())
        nextPage = finalPage
        await handleButtons(self, interaction, nextPage)

    # BE WARNED THIS CONTAINS \u200b ZERO WIDTH CHARACTER
    @discord.ui.button(label='​', custom_id='space1', row=1, disabled=True)
    async def space1_callback():
        print()
    # BE WARNED THIS CONTAINS \u200b ZERO WIDTH CHARACTER
    @discord.ui.button(label='​', custom_id='space2', row=1, disabled=True)
    async def space2_callback():
        print()

    @discord.ui.button(label='↻', custom_id='refresh', row=1, style=discord.ButtonStyle.blurple)
    async def button6_callback(self, button, interaction):
        # Not necessary as war thunder's website takes a long time to update
        # databaseUpdate(interaction)

        # setting current page
        currentPage = int(interaction.message.components[0].children[2].label.split('/')[0].strip())
        await handleButtons(self, interaction, currentPage)
        
    # BE WARNED THIS CONTAINS \u200b ZERO WIDTH CHARACTER
    @discord.ui.button(label='​', custom_id='space3', row=1, disabled=True)
    async def space3_callback():
        print()
    # BE WARNED THIS CONTAINS \u200b ZERO WIDTH CHARACTER
    @discord.ui.button(label='​', custom_id='space4', row=1, disabled=True)
    async def space4_callback():
        print()

def CreateEmbed(sql, data):
    itemsPerPage=10
    my_pages=[]

    # retrive users from database
    con, cur = connect()
    cur.execute(sql, data)
    names = cur.fetchall()
    close(con, cur)

    # turn the array into pages of embeds
    for i in range(0, len(names), itemsPerPage):
        pageNames=''
        page = discord.Embed(
        title=f'No Discord List',
        description='It takes a while for War Thunder to update the database.\nBe patient when refreshing doesnt update it instantly.',
        color=discord.Colour.from_rgb(255, 255, 255)
        )

        # add names to list
        for j in range(0, len(names[i:i+itemsPerPage])):
            pageNames += f'`{names[i:i+itemsPerPage][j][0]}`'
            pageNames += '\n'

        # print(pageNames)

        # add list to embed and return page
        page.add_field(name='Member', value=pageNames, inline=True)
        my_pages.append(page)
    
    # returns an array of embeds
    return my_pages

async def handleButtons(self, interaction, nextPage):
    # set final page
    # finalPage = int(interaction.message.components[0].children[2].label.split('/')[1].strip())

    # retrieve data from database
    embed = CreateEmbed('SELECT player FROM webscraper WHERE (in_discord IS NULL or in_discord = %s) and in_squadron = %s ORDER BY entry_date DESC;', (False, True))

    finalPage = len(embed)
    
    # create the button that shows page number
    button3 = discord.ui.Button(label=f'{nextPage} / {finalPage}')
    button3.disabled = True

    # insert the page number button in the middle of all the buttons
    view = PaginationView()
    midpoint = len(view.children)//4
    view.children = view.children[0:midpoint] + [button3] + view.children[midpoint:] 

    # disable buttons when at min/max values to prevent overflow
    if nextPage == finalPage:
        view.children[3].disabled = True
        view.children[4].disabled = True
    elif nextPage == 1:
        view.children[0].disabled = True
        view.children[1].disabled = True

    # update message
    await interaction.message.edit(embed=embed[nextPage - 1], view=view)
    # prevent interaction failed error
    await interaction.response.edit_message()


def setup(client):
    client.add_cog(Moderation(client))