date = int(input('whats the year?'))

if date%4 == 0 and date%400==0:
    print('this is a leap year')
else:
    print('Not a leap year.')