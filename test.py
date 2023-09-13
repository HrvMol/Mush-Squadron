import datetime

timestamp = int(datetime.datetime.strptime(f'{datetime.date.today()} 14:00', '%Y-%m-%d %H:%M').timestamp())
print(timestamp)