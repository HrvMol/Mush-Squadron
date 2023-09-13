join_date = '29.08.2020'

join_date = join_date.split('.')
print(join_date)
formatted_date = '-'.join([join_date[2], join_date[1], join_date[0]])

print(formatted_date)