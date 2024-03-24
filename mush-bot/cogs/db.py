import discord
from discord.ext import commands
import psycopg2
from datetime import datetime

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
            con, cur = connect()
            cur.execute('UPDATE webscraper SET messages_sent = messages_sent + 1 WHERE player=%s;', (ctx.author.display_name,))

            con.commit()
            close(con, cur)
        except Exception as e:
            self.bot.logging.exception('')
            pass

    # NOT TESTED YET
    # Flag that a user has left
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        try:
            if member.bot:
                return
                
            # Connect to the database and iterate the number of messages sent
            con, cur = connect()
            cur.execute('UPDATE webscraper SET in_discord=%s WHERE player=%s;', (False, member.display_name))

            con.commit()
            close(con, cur)

            channel = self.bot.get_channel(1128381656609341442)
            await channel.send(f'{member.display_name} has left the discord!')

        except Exception as e:
            self.bot.logging.exception('')
            pass
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:

            # For some reason it doesnt allow it condensed down
            before_roles = before.roles
            before_roles.reverse()
            after_roles = after.roles
            after_roles.reverse()
            
            print(before_roles[0].name)
            # If display name changes, register user as on discord and transfer from previous name
            if before.display_name != after.display_name:
                con, cur = connect()

                # Create new entry if name is not in table, else update with old data.
                sql = '''
                DO
                $do$
                BEGIN
                IF NOT EXISTS ( SELECT id FROM webscraper WHERE player = %(before)s ) THEN
                    INSERT INTO webscraper ( player, in_discord )
                    VALUES ( %(player)s, %(in_discord)s );
                ELSE 
                    UPDATE webscraper SET player = %(player)s, in_discord = %(in_discord)s WHERE player = %(before)s;
                END IF;
                end;
                $do$
                '''
                cur.execute(sql, {'before': before.display_name, 'player': after.display_name, 'messages_sent': 0, 'vc_time': 0, 'in_discord': True})

                con.commit()
                close(con, cur)

            # Update role in db
            if before_roles[0] != after_roles[0]:
                con, cur = connect()
                cur.execute('UPDATE webscraper SET role = %s, in_discord = %s WHERE player = %s', (after_roles[0].name, True, after.display_name))

                con.commit()
                close(con, cur)
        
        except Exception as e:
            self.bot.logging.exception('')
            pass

    # Record time spent in VC
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if before.channel != after.channel:
                if before.channel == None:
                    self.vc.update({member.display_name: datetime.now()})
                else:
                    # pop member from dictionary and get delta time
                    joined = self.vc.pop(member.display_name)
                    difference = datetime.now() - joined

                    # Convert the total seconds to string, then discard the parts after the decimal, then convert back to int
                    seconds = int(str(difference.total_seconds()).split('.')[0])

                    # NOT TESTED YET
                    con, cur = connect()
                    cur.execute('UPDATE webscraper SET vc_time=vc_time+%s WHERE player=%s;', (seconds, member.display_name))

                    con.commit()
                    close(con, cur)
                    
        except Exception as e:
            self.bot.logging.exception('')
            pass

    

# Creates connection to the database
def connect():
    try:
        con = psycopg2.connect(
            host='192.168.0.231',
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

def setup(client):
    client.add_cog(Db(client))