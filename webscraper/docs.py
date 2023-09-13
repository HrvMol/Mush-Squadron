from selenium import webdriver
from bs4 import BeautifulSoup

#Configure driver to run Chrome headless
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Making a GET request
driver.get("https://warthunder.com/en/community/claninfo/MUSH/")

# Parsing the HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Get all users from table
s = soup.find('div', class_="squadrons-members__table")
names = s.find_all('a')

for i in range(len(names)):
    name = names[i].text

    #get 4 divs after the name for the user stats
    user_data = names[i].find_all_next(limit=4)

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

    #format date into format accepted by postgres
    join_date = join_date.split('.')
    formatted_date = '-'.join([join_date[2], join_date[1], join_date[0]])

    print(name, clan_rating, activity, role, formatted_date)