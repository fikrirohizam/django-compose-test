from datetime import date
from django import template

register = template.Library()

def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def space_to_dash(string):
    return string.replace(' ','-')

register.filter('get_age', age)
register.filter('spacetodash', space_to_dash)

