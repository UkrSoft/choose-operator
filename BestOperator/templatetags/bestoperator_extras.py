from django import template
import re

register = template.Library()

@register.filter(name='row_data')
def get_row_data(rows, keys_str):
    """Get namedtuple' row values for the specified key.
    Returns a simple tuple with values of with dictionary
    of key:value pair depending on the amount of keys specified."""
    ret_res = []
    for row in rows:
        try:
            keys = re.split(' ?, ?', keys_str)
            keys_len = keys.__len__()
            if keys_len==1:
                res=eval('row.'+keys[0])
            else:
                res={key: val for (key, val) in list(map(lambda key, row:(key, eval('row.'+key)), keys, [row]*keys_len))}
            ret_res.append(res)
        except NameError as e:
            ret_res.append(e.__str__())
    return ret_res

@register.filter(name='gv')
def get_value(struct, key):
    """Get value from dict object by the given key"""
    if (isinstance(struct, dict)):
        if (key in struct.keys()):
            return struct.get(key)
        return 'gv:key \''+key+'\' doesn\'t exist'
    return 'gv:<unknown type>:'+struct