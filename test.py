import psycopg2

def connect():
    con = psycopg2.connect(
        host='localhost',
        port=5432,
        database='postgres',
        user='postgres',
        password='postgres'
    )

    cur = con.cursor()

    return con, cur

# Close the connection
def close(con, cur):
    cur.close()
    con.close()


con, cur = connect()

# update 1 setting from database
sql = '''
UPDATE settings SET information = information || '"test_item"=>"100"' :: hstore;
'''
cur.execute(sql)

# close connection
close(con, cur)