from datetime import date


def date_difference():
    current_date = date.today()
    year = int(input('Enter a year: '))
    month = int(input('Enter a month: '))
    day = int(input('Enter a day: '))
    given_date = date(year, month, day)
    diff = current_date - given_date
    return int(diff.days // 365.2425)

print(date_difference())