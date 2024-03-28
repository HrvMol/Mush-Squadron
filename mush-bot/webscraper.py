# FIND OUT HOW TO INSTALL FIREFOX ON SERVER TO USE IN HEADLESS MODE
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup
from cogs.db import connect, close

logging.basicConfig(filename='app.log', format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s() - %(message)s', datefmt='%d-%m-%y %H:%M:%S')

try:
    # retrieving the interval setting from the database
    # waitInterval = int(self.bot.settings.retrieveSetting('webscrape_interval_minutes'))
    # self.scraper.change_interval(minutes=waitInterval)

    # Configure driver to run Chrome headless
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    # driver = webdriver.Chrome(options=options)

    options = Options()
    options.add_argument('--headless')
    service = webdriver.FirefoxService(executable_path='/home/pi/.cargo/bin/geckodriver')
    driver = webdriver.Firefox(options=options, service=service)

    con, cur = connect()

    # Making a GET request
    driver.get("https://warthunder.com/en/community/claninfo/MUSH/")

    # Parsing the HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Get all users from table
    s = soup.find('div', class_="squadrons-members__table")
    names = s.find_all('a')

    players_in_squad = []

    for i in range(len(names)):
        name = names[i].text

        # Get 4 divs after the name for the user stats
        user_data = names[i].find_all_next(limit=4)

        # Remove whitespaces, newlines and format
        name = " ".join(name.split())
        clan_rating = int(" ".join(user_data[0].contents[0].split()))
        activity = int(" ".join(user_data[1].contents[0].split()))
        role = " ".join(user_data[2].contents[0].split())
        join_date = " ".join(user_data[3].contents[0].split())

        # Remove device identifier
        if name.endswith('@psn'):
            name = name[:-4]
        elif name.endswith('@live'):
            name = name[:-5]

        # Format date into format accepted by postgres
        join_date = join_date.split('.')
        formatted_date = '-'.join([join_date[2], join_date[1], join_date[0]])

        # Update if user is already in the table, if not, create new entry
        sql = '''
        DO
        $do$
        BEGIN
        IF NOT EXISTS ( SELECT id FROM webscraper WHERE player = %(name)s ) THEN
            INSERT INTO webscraper ( player, clan_rating, activity, entry_date, messages_sent, vc_time, in_squadron )
            VALUES ( %(name)s, %(clan_rating)s, %(activity)s, %(entry_date)s, %(messages_sent)s, %(vc_time)s, %(in_squadron)s );
        ELSE 
            UPDATE webscraper SET player = %(name)s, clan_rating = %(clan_rating)s, activity = %(activity)s, in_squadron = %(in_squadron)s WHERE player = %(name)s;
        END IF;
        end;
        $do$
        '''

        cur.execute(sql, {'name': name, 'clan_rating': clan_rating, 'activity': activity, 'entry_date': formatted_date, 'messages_sent': 0, 'vc_time': 0, 'in_squadron': True})

        print('added:', name, clan_rating, activity, role, formatted_date)

        players_in_squad.append(name)
        
    # Update users who are not in the squadron in game
    cur.execute('UPDATE webscraper SET in_squadron = False WHERE NOT (player = ANY (%s));', (players_in_squad,))

    # remove users who are no longer part of the squadron in game.
    # NEED TO UPDATE TO ONLY REMOVE IF USER IS NOT IN DISCORD AND IN GAME
    cur.execute('DELETE FROM webscraper WHERE in_discord=%s AND in_squadron=%s;', (False,False))


    con.commit()
    # close the connection and cursor
    close(con, cur)

except Exception as e:
    logging.exception('')
    pass

    # HOW TO FIND POSTGRES CONTAINER IP
    # docker ps, COPY CONTAINER ID, docker inspect [ID]