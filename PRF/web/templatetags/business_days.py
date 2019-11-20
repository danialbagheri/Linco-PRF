from django import template
from datetime import timedelta, date


register = template.Library()

@register.filter(name='convert_to_deadline')
def convert_to_deadline(from_date):
    number_of_days = 1
    to_date = from_date
    while number_of_days:
       to_date += timedelta(1)
       if to_date.weekday() < 5: # i.e. is not saturday or sunday
           number_of_days -= 1
    return to_date