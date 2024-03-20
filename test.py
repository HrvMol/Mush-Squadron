import datetime

# US
# end = int(datetime.datetime.strptime(f'{datetime.date.today()} 07:00', '%Y-%m-%d %H:%M').timestamp())

# EU
end = int(datetime.datetime.strptime(f'{datetime.date.today()} 22:00', '%Y-%m-%d %H:%M').timestamp())

now = int(str(datetime.datetime.now().timestamp()).split('.')[0])
# now = int(datetime.datetime.strptime(f'{datetime.datetime.now()}', '%Y-%m-%d %H:%M').timestamp())

print(datetime.date.today())

print(end)
print(now)

if now > end:
    print('ended')
if now < end:
    print('running')
