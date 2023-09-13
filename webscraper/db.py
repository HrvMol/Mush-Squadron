import psycopg2

#connect to db
con = psycopg2.connect(
    host='localhost',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres'
)

cur = con.cursor()

# cur.execute('UPDATE webscraper SET clan_rating = %s, activity = %s, role = %s WHERE id = %s;', (100, 1000, 'lmao', 1))

# cur.execute('INSERT INTO players (player, clan_rating, activity, role, entry_date) VALUES (%s, %s, %s, %s, %s)', ('header1234', 15, 600, 'Deputy', '2022-03-29'))
# print('added')

sql = ''' DELETE FROM webscraper WHERE role='Deputy' '''

cur.execute(sql)

cur.execute('SELECT * FROM webscraper')

rows = cur.fetchall()

for r in rows:
    print(r)
#commit changes
con.commit()

#close the cursor
cur.close()

#close the connection
con.close()