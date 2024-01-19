import discord
from discord.ext import commands
import datetime
from discord.commands import slash_command

class Srb(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("SRB Cog Loaded")

    @slash_command(description="Create a signup embed for squadron battles.")
    async def signup(self, ctx, br: discord.Option(str, description='Battle Rating'), window: discord.Option(str, description='SRB Window', choices=['US', 'EU']),):
        accepted_users = []
        declined_users = []
        tentative_users = []

        role = discord.utils.get(ctx.guild.roles, name = 'Mussh Members')
        
        embed = discord.Embed(
            title=f'Sign up for {window} {br} SRB',
            description='Mark your attendance below.',
            color=discord.Colour.from_rgb(255, 255, 255)
        )

        if window == 'US':
            # -/-/-/-/-/-/- NOT SET YET -/-/-/-/-/-/-
            start = int(datetime.datetime.strptime(f'{datetime.date.today()} 01:00', '%Y-%m-%d %H:%M').timestamp())
            end = int(datetime.datetime.strptime(f'{datetime.date.today()} 07:00', '%Y-%m-%d %H:%M').timestamp())
        else:
            start = int(datetime.datetime.strptime(f'{datetime.date.today()} 14:00', '%Y-%m-%d %H:%M').timestamp())
            end = int(datetime.datetime.strptime(f'{datetime.date.today()} 22:00', '%Y-%m-%d %H:%M').timestamp())
        
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

def setup(client):
    client.add_cog(Srb(client))
