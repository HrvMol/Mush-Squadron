from cogs.db import connect, close

class Settings:
    def retrieveSetting(id):
        # open connection
        con, cur = connect()

        # retrieve 1 setting from database
        sql = 'SELECT information -> %(id)s as information FROM settings WHERE information -> %(id)s is NOT NULL'
        cur.execute(sql, {'id': id})
        data = cur.fetchone()

        # close connection
        close(con, cur)

        return data[0]
