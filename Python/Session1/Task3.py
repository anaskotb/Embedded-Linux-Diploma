'''
 Print the calendar of a given month and year
'''

import calendar

year=int(input("please input the year"))
month=int(input("please input month"))
print(calendar.month(year,month))
