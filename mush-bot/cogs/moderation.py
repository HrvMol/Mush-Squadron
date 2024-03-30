import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
from discord.ext.pages import Paginator, PaginatorButton
from cogs.db import connect, close

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

    @slash_command(description="Display a list of the order in which members should be removed from the squadron")
    @commands.has_permissions(administrator = True)
    async def removal_list(self, ctx):
        try:
            itemsPerPage=10
            my_pages=[]
            
            # PLACEHOLDER
            names=['MUDD (geckos daddy)', 'Staem1', 'wall763abrasive', 'TOTOINOZ', 'MrTacoDoesGames', 'arnobvo', 'WOLFPACK0581869', 'Ph4atomPB', 'Tcrawl4539', 'blondiefrodo', 'geckojesus', 'briocheman21', 'header1234', 'youssef_18', 'Jhozep', 'MeatisOmalley', '_Zr0_', 'chogchey', 'fams_4', 'DDawg', 'Jadjood']

            for i in range(0, len(names), itemsPerPage):
                pageNames=''
                page = discord.Embed(
                title=f'Removal List',
                color=discord.Colour.from_rgb(255, 255, 255)
                )

                for j in range(0, len(names[i:i+itemsPerPage])):
                    pageNames += f'`{names[i:i+itemsPerPage][j]}`'
                    pageNames += '\n'

                page.add_field(name='Member', value=pageNames, inline=True)
                my_pages.append(page)

            paginator = Paginator(pages=my_pages)
            await paginator.respond(ctx.interaction, ephemeral=False)
        except Exception as e:
            self.bot.logging.exception('')
            await ctx.respond('An error has occurred')

    @slash_command(description="Display the list of people who are not in the discord")
    @commands.has_permissions(administrator = True)
    async def recruitment(self, ctx):
        # try:
        #     itemsPerPage=10
        #     my_pages=[]

        #     # retrive users from database
        #     con, cur = connect()
        #     cur.execute('SELECT player FROM webscraper WHERE (in_discord IS NULL or in_discord = %s) and in_squadron = %s ORDER BY entry_date DESC;', (False, True))
        #     names = cur.fetchall()
        #     close(con, cur)

        #     # turn the array into pages for the 
        #     for i in range(0, len(names), itemsPerPage):
        #         pageNames=''
        #         page = discord.Embed(
        #         title=f'Recruitment List',
        #         color=discord.Colour.from_rgb(255, 255, 255)
        #         )

        #         for j in range(0, len(names[i:i+itemsPerPage])):
        #             pageNames += f'`{names[i:i+itemsPerPage][j][0]}`'
        #             pageNames += '\n'

        #         page.add_field(name='Member', value=pageNames, inline=True)
        #         my_pages.append(page)


        #     # set up buttons
        #     paginator = Paginator(pages=my_pages)
        #     paginator.remove_button("first")
        #     paginator.remove_button("last")
        #     paginator.add_button(PaginatorButton("Refresh", label="⟳", style=discord.ButtonStyle.blurple))

        #     await paginator.respond(ctx.interaction, ephemeral=False)
        # except Exception as e:
        #     self.bot.logging.exception('')
        #     await ctx.respond('An error has occurred')


        my_pages = CreateEmbed('SELECT player FROM webscraper WHERE (in_discord IS NULL or in_discord = %s) and in_squadron = %s ORDER BY entry_date DESC;', (False, True))
        view = PaginationView()

        

        currentPage = 1
        finalPage = 12

        button = discord.ui.Button(label=f'{currentPage} / {finalPage}')
        button.disabled = True

        midpoint = len(view.children)//2
        view.children = view.children[0:midpoint] + [button] + view.children[midpoint:] 


        # view.children.append(view.children[1])
        # view.children[1] = button
        # print(view.children)
        await ctx.respond(embed=my_pages[1], view=view)


    # @slash_command(description="update a setting")
    # async def settings(self, ctx):
    #     self.bot.settings.updateSetting('a', 'b')
    #     await ctx.respond(f'Modified Setting')

class PaginationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.embed = CreateEmbed('SELECT player FROM webscraper WHERE (in_discord IS NULL or in_discord = %s) and in_squadron = %s ORDER BY entry_date DESC;', (False, True))

    @discord.ui.button(label='<<', custom_id='first', style=discord.ButtonStyle.blurple)
    async def button1_callback(self, button, interaction):
        currentPage = 1
        finalPage = int(interaction.message.components[0].children[2].label.split('/')[1].strip())
        
        button3 = discord.ui.Button(label=f'{currentPage} / {finalPage}')
        button3.disabled = True

        view = PaginationView()
        midpoint = len(view.children)//2
        view.children = view.children[0:midpoint] + [button3] + view.children[midpoint:] 

        if currentPage == finalPage:
            view.children[3].disabled = True
            view.children[4].disabled = True
        elif currentPage == 1:
            view.children[0].disabled = True
            view.children[1].disabled = True

        await interaction.message.edit(embed=self.embed[currentPage], view=view)
        await interaction.response.edit_message()
        
    @discord.ui.button(label='<', custom_id='prev', style=discord.ButtonStyle.red)
    async def button2_callback(self, button, interaction):
        currentPage = int(interaction.message.components[0].children[2].label.split('/')[0].strip()) - 1
        finalPage = int(interaction.message.components[0].children[2].label.split('/')[1].strip())
        
        button3 = discord.ui.Button(label=f'{currentPage} / {finalPage}')
        button3.disabled = True

        view = PaginationView()
        midpoint = len(view.children)//2
        view.children = view.children[0:midpoint] + [button3] + view.children[midpoint:] 

        if currentPage == finalPage:
            view.children[3].disabled = True
            view.children[4].disabled = True
        elif currentPage == 1:
            view.children[0].disabled = True
            view.children[1].disabled = True

        await interaction.message.edit(embed=self.embed[currentPage], view=view)
        await interaction.response.edit_message()

    @discord.ui.button(label='>', custom_id='next', style=discord.ButtonStyle.green)
    async def button4_callback(self, button, interaction):
        currentPage = int(interaction.message.components[0].children[2].label.split('/')[0].strip()) + 1
        finalPage = int(interaction.message.components[0].children[2].label.split('/')[1].strip())

        button3 = discord.ui.Button(label=f'{currentPage} / {finalPage}')
        button3.disabled = True

        view = PaginationView()
        midpoint = len(view.children)//2
        view.children = view.children[0:midpoint] + [button3] + view.children[midpoint:] 

        if currentPage == finalPage:
            view.children[3].disabled = True
            view.children[4].disabled = True
        elif currentPage == 1:
            view.children[0].disabled = True
            view.children[1].disabled = True

        print(view.children)

        await interaction.message.edit(embed=self.embed[currentPage], view=view)
        await interaction.response.edit_message()

    
    
    @discord.ui.button(label='>>', custom_id='last', style=discord.ButtonStyle.blurple)
    async def button5_callback(self, button, interaction):
        finalPage = int(interaction.message.components[0].children[2].label.split('/')[1].strip())
        currentPage = finalPage
        
        button3 = discord.ui.Button(label=f'{currentPage} / {finalPage}')
        button3.disabled = True

        view = PaginationView()
        midpoint = len(view.children)//2
        view.children = view.children[0:midpoint] + [button3] + view.children[midpoint:] 

        if currentPage == finalPage:
            view.children[3].disabled = True
            view.children[4].disabled = True
        elif currentPage == 1:
            view.children[0].disabled = True
            view.children[1].disabled = True

        await interaction.message.edit(embed=self.embed[currentPage], view=view)
        await interaction.response.edit_message()



def CreateEmbed(sql, data):
    itemsPerPage=10
    my_pages=[]

    # retrive users from database
    con, cur = connect()
    cur.execute(sql, data)
    names = cur.fetchall()
    close(con, cur)

    # turn the array into pages for the 
    for i in range(0, len(names), itemsPerPage):
        pageNames=''
        page = discord.Embed(
        title=f'Recruitment List',
        color=discord.Colour.from_rgb(255, 255, 255)
        )

        for j in range(0, len(names[i:i+itemsPerPage])):
            pageNames += f'`{names[i:i+itemsPerPage][j][0]}`'
            pageNames += '\n'

        page.add_field(name='Member', value=pageNames, inline=True)
        my_pages.append(page)
    
    return my_pages


def setup(client):
    client.add_cog(Moderation(client))