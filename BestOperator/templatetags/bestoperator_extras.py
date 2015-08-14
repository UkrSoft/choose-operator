from django import template

register = template.Library()

@register.filter(name='row_data')
def get_row_data(rows, key):
    """Get namedtuple' row values for the specified key. Returns a simple tuple."""
    ft = []
    for row in rows:
        ft.append(eval('row.'+key))
    return ft