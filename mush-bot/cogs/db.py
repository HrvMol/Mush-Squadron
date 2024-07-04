import discord
from discord.commands import slash_command
from discord.ext import commands
# import psycopg2
from datetime import datetime, timedelta
import os

import requests
import json

class Db(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.vc = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("Db Cog Loaded")

    # Increases user score when message is sent
    @commands.Cog.listener()
    async def on_message(self, ctx):
        try:
            # Checks if the author is a bot and ignores if true
            if ctx.author.bot:
                return
                
            # Connect to the database and iterate the number of messages sent
            # con, cur = connect()
            # cur.execute('UPDATE webscraper SET messages_sent = messages_sent + 1 WHERE discord_id = %s;', (ctx.author.id,))
            databasePost(f'UPDATE webscraper SET messages_sent = messages_sent + 1 WHERE discord_id = {ctx.author.id};')

            # con.commit()
            # close(con, cur)
        except Exception as e:
            self.bot.logging.exception('')
            pass

    # NOT TESTED YET
    # Flag that a user has left
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        try:
            # Connect to the database and iterate the number of messages sent
            # con, cur = connect()
            # cur.execute('UPDATE webscraper SET in_discord=%s WHERE discord_id = %s;', (False, member.id))
            databasePost(f'UPDATE webscraper SET in_discord=False WHERE discord_id = {member.id};')

            # con.commit()
            # close(con, cur)

            channel = self.bot.get_channel(1128381656609341442)
            await channel.send(f'{member.display_name} has left the discord!')

        except Exception as e:
            self.bot.logging.exception('')
            pass
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if before.bot:
                return
            # For some reason it doesnt allow it condensed down
            before_roles = before.roles
            before_roles.reverse()
            after_roles = after.roles
            after_roles.reverse()
            
            print(before_roles[0].name)
            # If display name changes, register user as on discord and transfer from previous name
            if before.display_name != after.display_name:
                # con, cur = connect()

                print(after.id)

                # Create new entry if name is not in table, else if user is not in squadron allow them to edit their name in db.
                # sql = '''
                # DO
                # $do$
                # BEGIN
                # IF NOT EXISTS ( SELECT id FROM webscraper WHERE discord_id = %(discord_id)s ) THEN
                #     INSERT INTO webscraper ( player, role, messages_sent, vc_time, in_discord, discord_id )
                #     VALUES ( %(player)s, %(role)s, %(messages_sent)s, %(vc_time)s, %(in_discord)s, %(discord_id)s );
                # ELSEIF EXISTS ( SELECT id FROM webscraper WHERE player = %(before)s AND (in_squadron IS null OR in_squadron = false) ) THEN
                #     UPDATE webscraper SET player = %(player)s, in_discord = %(in_discord)s, discord_id = %(discord_id)s WHERE player = %(before)s;
                # END IF;
                # end;
                # $do$
                # '''
                # cur.execute(sql, {'before': before.display_name, 'player': after.display_name, 'role':after_roles[0].name, 'messages_sent': 0, 'vc_time': 0, 'in_discord': True, 'discord_id': after.id})
                databasePost(f'''
                    DO
                    $do$
                    BEGIN
                    IF NOT EXISTS ( SELECT id FROM webscraper WHERE discord_id = {after.id} ) THEN
                        INSERT INTO webscraper ( player, role, messages_sent, vc_time, in_discord, discord_id )
                        VALUES ( {after.display_name}, {after_roles[0].name}, 0, 0, True, {after.id} );
                    ELSEIF EXISTS ( SELECT id FROM webscraper WHERE player = {before.display_name} AND (in_squadron IS null OR in_squadron = false) ) THEN
                        UPDATE webscraper SET player = {after.display_name}, in_discord = True, discord_id = {after.id} WHERE player = {before.display_name};
                    END IF;
                    end;
                    $do$
                ''')

                # removing duplicate entries in database
                # cur.execute('''
                #     DELETE FROM webscraper
                #     WHERE CONCAT(player,messages_sent) NOT IN 
                #         (
                #         SELECT CONCAT(player,MAX(messages_sent))
                #         FROM webscraper
                #         GROUP BY player
                #         );
                    
                #     DELETE FROM webscraper
                #     WHERE CONCAT(player,id) NOT IN 
                #         (
                #         SELECT CONCAT(player,MAX(id))
                #         FROM webscraper
                #         GROUP BY player
                #         );
                #     ''')

                databasePost('''
                    DELETE FROM webscraper
                    WHERE CONCAT(player,messages_sent) NOT IN 
                        (
                        SELECT CONCAT(player,MAX(messages_sent))
                        FROM webscraper
                        GROUP BY player
                        );
                    
                    DELETE FROM webscraper
                    WHERE CONCAT(player,id) NOT IN 
                        (
                        SELECT CONCAT(player,MAX(id))
                        FROM webscraper
                        GROUP BY player
                        );
                ''')

                # con.commit()
                # close(con, cur)

            # Update role in db
            if before_roles[0] != after_roles[0]:
                # con, cur = connect()
                # cur.execute('UPDATE webscraper SET role = %s, in_discord = %s WHERE discord_id = %s', (after_roles[0].name, True, after.id))
                databasePost(f'UPDATE webscraper SET role = {after_roles[0].name}, in_discord = True WHERE discord_id = {after.id};')
                # con.commit()
                # close(con, cur)
        
        except Exception as e:
            self.bot.logging.exception('')
            pass

    # Record time spent in VC
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if before.channel != after.channel:
                print('done1')
                if before.channel == None:
                    print('done2')
                    self.vc.update({member.display_name: datetime.now()})
                else:
                    # pop member from dictionary and get delta time
                    joined = self.vc.pop(member.display_name)
                    difference = datetime.now() - joined

                    # Convert the total seconds to string, then discard the parts after the decimal, then convert back to int
                    seconds = int(str(difference.total_seconds()).split('.')[0])

                    # NOT TESTED YET
                    # con, cur = connect()
                    # cur.execute('UPDATE webscraper SET vc_time=vc_time+%s WHERE discord_id = %s;', (seconds, member.id))
                    databasePost(f'UPDATE webscraper SET vc_time=vc_time+{seconds} WHERE discord_id = {member.id};')

                    # con.commit()
                    # close(con, cur)
                    print('done3')
                    
        except Exception as e:
            self.bot.logging.exception('')
            pass
    
    @slash_command(description="Force an update of the entire database")
    async def update_database(self, ctx):
        await ctx.response.defer()
        try:
            databaseUpdate(ctx)
            await ctx.respond('Updated Database')
        except:
            self.bot.logging.exception('')
            await ctx.respond("Error")

    @slash_command(description="View the information on a member")
    async def stats(self, ctx, member: discord.Option(discord.Member, description='User you would like to see')): # type: ignore
        # retrieve data from database
        # con, cur = connect()
        # cur.execute('SELECT clan_rating, activity, role, entry_date, messages_sent, vc_time FROM webscraper WHERE discord_id = %s;', (member.id,))
        # userData = cur.fetchone()
        # close(con, cur)
        userData = json.loads(databaseGetUser(member.id))[0]

        embed = discord.Embed(title=member.display_name, description=f'`{userData["role"]}`', color=discord.Colour.from_rgb(255, 255, 255))

        # BE WARNED THIS CONTAINS \u200b ZERO WIDTH CHARACTER
        embed.add_field(name='\n ​', value='\n ​', inline=False)

        # add fields for all the data
        embed.add_field(name='SRB Points', value=f'`{userData["clan_rating"]}`')
        embed.add_field(name='Activity', value=f'`{userData["activity"]}`')
        embed.add_field(name='Messages Sent', value=f'`{userData["messages_sent"]}`')

        if userData["vc_time"] == None: embed.add_field(name='Time in VC', value='`None`')
        else: embed.add_field(name='Time in VC', value=f'`{str(timedelta(seconds=userData["vc_time"]))}`')

        convertedDate = userData["entry_date"][:10]
        embed.add_field(name='Date Joined', value=f'`{convertedDate}`')

        embed.set_thumbnail(url=member.avatar)

        await ctx.respond(embed=embed)
        
def databaseUpdate(ctx):
    con, cur = connect()
    for member in ctx.guild.members:
        memberRole = member.roles[::-1][0]
        print(member.display_name, memberRole.name)

        cur.execute('''
                    UPDATE webscraper SET discord_id = %(discord_id)s WHERE player = %(name)s;
                    UPDATE webscraper SET role = %(role)s, in_discord = %(in_discord)s WHERE discord_id = %(discord_id)s;
                    DELETE FROM webscraper
                    WHERE CONCAT(player,messages_sent) NOT IN 
                        (
                        SELECT CONCAT(player,MAX(messages_sent))
                        FROM webscraper
                        GROUP BY player
                        );
                    
                    DELETE FROM webscraper
                    WHERE CONCAT(player,id) NOT IN 
                        (
                        SELECT CONCAT(player,MAX(id))
                        FROM webscraper
                        GROUP BY player
                        );
                    ''', {'role': memberRole.name, 'in_discord': True, 'discord_id': member.id, 'name': member.display_name})

    con.commit()
    close(con, cur)
    
    os.system('python ./webscraper.py')

# Creates connection to the database
def connect():
    try:
        con = psycopg2.connect(
            # host='192.168.0.231',
            host='localhost',
            port=5432,
            database='postgres',
            user='postgres',
            password='postgres'
        )

        cur = con.cursor()

        return con, cur

    except Exception as e:
        print(e)
        print('Could not connect to database')

# Close the connection
def close(con, cur):
    cur.close()
    con.close()

def databasePost(sql):
    jsonQuery = f'"query":"{sql}"'
    jsonQuery = '{' + jsonQuery + '}'

    print(json.loads(jsonQuery))
    requests.post("http://localhost:5000/users", json=json.loads(jsonQuery))

def databaseGetUser(discord_id):
    x = requests.get(f"http://localhost:5000/users/{discord_id}")
    return x.text
    

def setup(client):
    client.add_cog(Db(client))