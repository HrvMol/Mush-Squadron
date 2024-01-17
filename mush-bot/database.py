from cogs.db import connect, close

class Settings:
    def retrieveSetting(id):
        # open connection
        con, cur = connect()

        # retrieve 1 setting from database
        # sql = 'SELECT information -> %(id)s as information FROM settings WHERE information -> %(id)s is NOT NULL'
        sql = '''SELECT attr -> 'webscrape_interval_minutes' AS interval FROM keypair;'''
        cur.execute(sql, {'id': id})
        data = cur.fetchone()

        # close connection
        close(con, cur)

        return data[0]
    
    def updateSetting(id, data):
        con, cur = connect()

        # update 1 setting from database
        sql = '''
        UPDATE keypair SET attr = attr || '"webscrape_interval_seconds"=>"100"' :: hstore;
        '''
        cur.execute(sql)
        # cur.execute(sql, {'id': id, 'data': data})

        # close connection
        close(con, cur)

