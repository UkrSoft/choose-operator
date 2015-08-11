from django.db import connection

class MagicSql:
    """
        Parse SQL to tuple of tuples (many dimensioned array)
    """
    def __init__(self, sql, fields = None, trans = None):
        if trans is None:
            trans = {}
        self.sql = sql
        self.fields = fields
        self.trans = trans
        self.rowset = self.execute_sql()
    def execute_sql(self):
        sql = self.sql
        rowset = None
        if sql:
            cursor = connection.cursor()
            cursor.execute(sql)
            rowset = cursor.fetchall()
        return rowset
    def get_dict(self):
        rowset = self.rowset
        fields = self.fields
        trans = self.trans
        if fields:
            result_set = (fields, )
        else:
            result_set = ()
        if rowset:
            for row in rowset:
                t = []
                if fields:
                    for field in fields:
                        try:
                            cell = row[fields.index('%s' % field)] #get value of dedicated cell
                            saved_cell = cell
                        except KeyError:
                            cell = '' #or return empty cell
                        try:
                            if trans and field in trans:
                                exec ("cell = " + trans[field]) % {'cell' : cell} #apply transformation described in 'trans' dict; '%(cell)s macros allowable'
                            t.append("%s"%(cell))
                        except Exception as e:
                            if field in trans.keys():
                                print('Exception while processing \'%(col)s\' column, value = \'%(cell)s\' with message \'%(message)s\'' % {'col' : field, 'cell' : saved_cell, 'message': trans[field]})
                            else:
                                print('Exception while processing \'%(col)s\' column, value = \'%(cell)s\'' % {'col' : field, 'cell' : saved_cell})
                            t.append("%s"%(saved_cell))
                else:
                    i = 0
                    while True:
                        try:
                            t.append("%s"%(row[i]))
                            i += 1
                        except IndexError:
                            break
                result_set += (tuple(t), )
        return result_set