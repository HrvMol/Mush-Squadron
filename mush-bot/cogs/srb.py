import discord
from discord.ext import commands
import datetime
from discord.commands import slash_command

class Srb(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(signupButtons())
        print("SRB Cog Loaded")

    @slash_command(description="Create a signup embed for squadron battles.")
    @commands.has_permissions(manage_messages = True)
    async def signup(self, ctx, br: discord.Option(str, description='Battle Rating'), window: discord.Option(str, description='SRB Window', choices=['US', 'EU']),): # type: ignore
        try:
            accepted_users = []
            declined_users = []
            tentative_users = []

            role = discord.utils.get(ctx.guild.roles, name = 'Mussh Members')
            
            embed = discord.Embed(
                title=f'Sign up for {window} {br} SRB',
                description='Mark your attendance below.',
                color=discord.Colour.from_rgb(255, 255, 255)
            )

            startUS = int(datetime.datetime.strptime(f'{datetime.date.today()} 01:00', '%Y-%m-%d %H:%M').timestamp())
            endUS = int(datetime.datetime.strptime(f'{datetime.date.today()} 07:00', '%Y-%m-%d %H:%M').timestamp())
            startEU = int(datetime.datetime.strptime(f'{datetime.date.today()} 14:00', '%Y-%m-%d %H:%M').timestamp())
            endEU = int(datetime.datetime.strptime(f'{datetime.date.today()} 22:00', '%Y-%m-%d %H:%M').timestamp())

            # Setting Times
            if window == 'US':
                # -/-/-/-/-/-/- NOT SET YET -/-/-/-/-/-/-
                start = startUS
                end = endUS
            else:
                start = startEU
                end = endEU

            # Ensuring times are correct
            now = int(str(datetime.datetime.now().timestamp()).split('.')[0])

            # set time to next day if window has already passed
            if now > end:
                start += 86400
                end += 86400
            
            embed.add_field(name='Begins at', value=f'<t:{start}:t>, <t:{start}:R>', inline=True)
            embed.add_field(name='Ends at', value=f'<t:{end}:t>, <t:{end}:R>', inline=True)
            
            # BE WARNED THIS CONTAINS \u200b ZERO WIDTH CHARACTER
            embed.add_field(name='\n ​', value='\n ​', inline=False)
            
            embed.add_field(name='✅ Accepted (0)', value=f'-', inline=True)
            embed.add_field(name='❌ Declined (0)', value=f'-', inline=True)
            embed.add_field(name='❔ Tentative (0)', value=f'-', inline=True)

            # Create buttons
            button1 = discord.ui.Button(label="Accept", emoji='✅')
            button2 = discord.ui.Button(label="Decline", emoji='❌')
            button3 = discord.ui.Button(label="Tentative", emoji='❔')

            # Button callbacks
            async def button1_callback(interaction):
                name = interaction.user.display_name

                # Remove name if in list, else add to list
                if name in accepted_users:
                    accepted_users.remove(name)
                else:
                    accepted_users.append(name)

                # Update message with new data
                if accepted_users: embed.set_field_at(index=3, name=f'✅ Accepted ({len(accepted_users)})', value='\n'.join([str(i) for i in accepted_users]), inline=True)
                else: embed.set_field_at(index=3, name=f'✅ Accepted ({len(accepted_users)})', value='-', inline=True)
                await interaction.response.edit_message(embed=embed)

            async def button2_callback(interaction):
                name = interaction.user.display_name

                # Remove name if in list, else add to list
                if name in declined_users:
                    declined_users.remove(name)
                else:
                    declined_users.append(name)
                
                # Update message with new data
                if declined_users: embed.set_field_at(index=4, name=f'❌ Declined ({len(declined_users)})', value='\n'.join([str(i) for i in declined_users]), inline=True)
                else: embed.set_field_at(index=4, name=f'❌ Declined ({len(declined_users)})', value='-', inline=True)
                await interaction.response.edit_message(embed=embed)

            async def button3_callback(interaction):
                name = interaction.user.display_name

                # Remove name if in list, else add to list
                if name in tentative_users:
                    tentative_users.remove(name)
                else:
                    tentative_users.append(name)

                # Update message with new data
                if tentative_users: embed.set_field_at(index=5, name=f'❔ Tentative ({len(tentative_users)})', value='\n'.join([str(i) for i in tentative_users]), inline=True)
                else: embed.set_field_at(index=5, name=f'❔ Tentative ({len(tentative_users)})', value='-', inline=True)
                await interaction.response.edit_message(embed=embed)

            # Assign button callbacks
            button1.callback = button1_callback
            button2.callback = button2_callback
            button3.callback = button3_callback

            # Create view and add buttons
            view = discord.ui.View(button1, button2, button3, timeout=None)

            print(role.mention)

            await ctx.respond(embed=embed, view=view)
            await ctx.send(role.mention)
        
        except Exception as e:
            self.bot.logging.exception()
            await ctx.respond('An error has occurred')

    @slash_command(description='List the next EU and US SRB windows')
    async def srb_when(self, ctx):
        try:
            # Ensuring times are correct
            now = int(str(datetime.datetime.now().timestamp()).split('.')[0])

            startUS = self.startUS
            endUS = self.endUS
            startEU = self.startEU
            endEU = self.endEU

            # set time to next day if window has already passed
            if now > self.endUS:
                startUS += 86400
                endUS += 86400
            if now > self.endEU:
                startEU += 86400
                endEU += 86400

            await ctx.respond(f'The next EU window starts at <t:{startEU}:t> and ends at <t:{endEU}:t> \nThe next US window starts at <t:{startUS}:t> and ends at <t:{endUS}:t>')
        
        except Exception as e:
            self.bot.logging.exception()
            await ctx.respond('An error has occurred')
    
    @slash_command(description='Explain SRB')
    async def srb_explain(self, ctx):
        try:
            await ctx.respond(f'SRB is an 8 vs 8 version of ground RB with a few other changes.```\n- You only get 1 spawn in SRB. No respawning.\n- Each team can spawn a maximum of 4 aircraft.\n- Only bomber aircraft get air spawns. This makes bombers very powerful.\n- Ground units can only detect friendly aircraft within 1 kilometer, and vice versa.\n``` The schedule for SRB is as follows:\n__EU__\n<t:{self.startEU}:t> - <t:{self.endEU}:t>\n\n__US__\n<t:{self.startUS}:t> - <t:{self.endUS}:t>\n\nWe will call through the srb-signup channel. Keep your notifications on.')

        except Exception as e:
            self.bot.logging.exception()
            await ctx.respond('An error has occurred')
        
    @slash_command()
    async def better_signup(self, ctx, br: discord.Option(str, description='Battle Rating'), window: discord.Option(str, description='SRB Window', choices=['US', 'EU']),): # type: ignore
        embed = createSignupEmbed(window, br)
        view = signupButtons()

        await ctx.respond(embed=embed, view=view)

def createSignupEmbed(window, br):
    embed = discord.Embed(
        title=f'Sign up for {window} {br} SRB',
        description='Mark your attendance below.',
        color=discord.Colour.from_rgb(255, 255, 255)
    )

    startUS = int(datetime.datetime.strptime(f'{datetime.date.today()} 01:00', '%Y-%m-%d %H:%M').timestamp())
    endUS = int(datetime.datetime.strptime(f'{datetime.date.today()} 07:00', '%Y-%m-%d %H:%M').timestamp())
    startEU = int(datetime.datetime.strptime(f'{datetime.date.today()} 14:00', '%Y-%m-%d %H:%M').timestamp())
    endEU = int(datetime.datetime.strptime(f'{datetime.date.today()} 22:00', '%Y-%m-%d %H:%M').timestamp())

    # Setting Times
    if window == 'US':
        # -/-/-/-/-/-/- NOT SET YET -/-/-/-/-/-/-
        start = startUS
        end = endUS
    else:
        start = startEU
        end = endEU

    # Ensuring times are correct
    now = int(str(datetime.datetime.now().timestamp()).split('.')[0])

    # set time to next day if window has already passed
    if now > end:
        start += 86400
        end += 86400

    embed.add_field(name='Begins at', value=f'<t:{start}:t>, <t:{start}:R>', inline=True)
    embed.add_field(name='Ends at', value=f'<t:{end}:t>, <t:{end}:R>', inline=True)

    # BE WARNED THIS CONTAINS \u200b ZERO WIDTH CHARACTER
    embed.add_field(name='\n ​', value='\n ​', inline=False)

    embed.add_field(name='✅ Accepted (0)', value=f'-', inline=True)
    embed.add_field(name='❌ Declined (0)', value=f'-', inline=True)
    embed.add_field(name='❔ Tentative (0)', value=f'-', inline=True)

    return embed

async def handleSignupButtons(self, interaction, field):
    window, br = interaction.message.embeds[0].title[12:-4].split(' ')

    accepted = interaction.message.embeds[0].fields[3]
    declined = interaction.message.embeds[0].fields[4]
    tentative = interaction.message.embeds[0].fields[5]

    embed = createSignupEmbed(window, br)

    if field == 'accepted':
        print('accepted')
        
        acceptedUsers = accepted.value
        print(acceptedUsers)

    
    for i in range(len(embed.fields)):
        if field in embed.fields[i].name:
            print(embed.fields[i].value)

            col, num = embed.fields[i].name.split('(')
            num = num[:-1]
            print(col)
            print(num)
            print(interaction.user.display_name)
            embed.set_field_at(index=i, name=f'{col}({num})', value=('\n'.join([])), inline=True)

    # update message
    await interaction.message.edit(embed=embed)
    # prevent interaction failed error
    await interaction.response.edit_message()

class signupButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Accept', custom_id='Accepted', style=discord.ButtonStyle.green)
    async def button1_callback(self, button, interaction):
        await handleSignupButtons(self, interaction, button.custom_id)

    @discord.ui.button(label='Decline', custom_id='Declined', style=discord.ButtonStyle.red)
    async def button2_callback(self, button, interaction):
        await handleSignupButtons(self, interaction, button.custom_id)
    
    @discord.ui.button(label='Tentative', custom_id='Tentative', style=discord.ButtonStyle.gray)
    async def button3_callback(self, button, interaction):
        await handleSignupButtons(self, interaction, button.custom_id)

def setup(client):
    client.add_cog(Srb(client))
