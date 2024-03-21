import discord
from discord.ext import commands
import datetime
from discord.commands import slash_command

class Srb(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        self.startUS = int(datetime.datetime.strptime(f'{datetime.date.today()} 01:00', '%Y-%m-%d %H:%M').timestamp())
        self.endUS = int(datetime.datetime.strptime(f'{datetime.date.today()} 07:00', '%Y-%m-%d %H:%M').timestamp())
        self.startEU = int(datetime.datetime.strptime(f'{datetime.date.today()} 14:00', '%Y-%m-%d %H:%M').timestamp())
        self.endEU = int(datetime.datetime.strptime(f'{datetime.date.today()} 22:00', '%Y-%m-%d %H:%M').timestamp())
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("SRB Cog Loaded")

    @slash_command(description="Create a signup embed for squadron battles.")
    @commands.has_permissions(manage_messages = True)
    async def signup(self, ctx, br: discord.Option(str, description='Battle Rating'), window: discord.Option(str, description='SRB Window', choices=['US', 'EU']),):
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

            # Setting Times
            if window == 'US':
                # -/-/-/-/-/-/- NOT SET YET -/-/-/-/-/-/-
                start = self.startUS
                end = self.endUS
            else:
                start = self.startEU
                end = self.endEU

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
            view = discord.ui.View(button1, button2, button3)

            msg = await ctx.respond(role.mention, embed=embed, view=view)
        
        except Exception as e:
            self.bot.logging.error(e)
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
            self.bot.logging.error(e)
            await ctx.respond('An error has occurred')
    
    @slash_command(description='Explain SRB')
    async def srb_explain(self, ctx):
        try:
            await ctx.respond(f'SRB is an 8 vs 8 version of ground RB with a few other changes.```\n- You only get 1 spawn in SRB. No respawning.\n- Each team can spawn a maximum of 4 aircraft.\n- Only bomber aircraft get air spawns. This makes bombers very powerful.\n- Ground units can only detect friendly aircraft within 1 kilometer, and vice versa.\n``` The schedule for SRB is as follows:\n__EU__\n<t:{self.startEU}:t> - <t:{self.endEU}:t>\n\n__US__\n<t:{self.startUS}:t> - <t:{self.endUS}:t>\n\nWe will call through the srb-signup channel. Keep your notifications on.')

        except Exception as e:
            self.bot.logging.error(e)
            await ctx.respond('An error has occurred')


def setup(client):
    client.add_cog(Srb(client))
