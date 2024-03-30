import requests
from bs4 import BeautifulSoup

r = requests.get("https://warthunder.com/en/community/claninfo/MUSH/")

# print(r.content)

soup = BeautifulSoup(r.content, 'html.parser')

# Get all users from table
s = soup.find('div', class_="squadrons-members__table")
names = s.find_all('a')

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

    print(name)