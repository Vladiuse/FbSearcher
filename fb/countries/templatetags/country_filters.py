from django import template

register = template.Library()



def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'k', 'M', 'G', 'T', 'P'][magnitude])

def population_short(value):
    """Removes all values of arg from the given string"""
    return human_format(value)


register.filter("population_short", population_short)