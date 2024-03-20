import datetime
now = int(str(datetime.datetime.now().timestamp()).split('.')[0])
print(now)
print(now+86400)
