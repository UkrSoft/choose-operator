from django.db import connection

class MagicSql:
    """
        Executes and parses SQL to tuple of tuples (many dimensioned array)

        @param sql the query which should be executed
        @fields names of columns to be outputted as result of this query execution or <code>False<code> if do not need this
        @trans transformation to be applied to each cell prior returning its value
    """
    def __init__(self, sql, column_names = None, trans = None):
        if trans is None:
            trans = {}
        self.sql = sql
        self.column_names = column_names
        self.trans = trans
        self.rowset, self.column_names = self.get_raw()
    def get_raw(self):
        sql = self.sql
        column_names = self.column_names
        rowset = None
        if sql:
            cursor = connection.cursor()
            cursor.execute(sql)
            if (column_names is None):
                if not cursor.description:
                    column_names = ()
                else:
                    column_names = tuple([d[0] for d in cursor.description])
            rowset = cursor.fetchall()
            cursor.close()
        return rowset, column_names
    def get_results(self):
        rowset = self.rowset
        column_names = self.column_names
        trans = self.trans
        if column_names:
            result_set = (column_names, )
        else:
            result_set = ()
        if rowset:
            for row in rowset:
                t = []
                if column_names:
                    for field in column_names:
                        try:
                            cell = row[column_names.index('%s' % field)] #get value of dedicated cell
                            saved_cell = cell
                        except KeyError:
                            cell = '' #or return empty cell
                        try:
                            if trans and field in trans:
                                exec ("cell = " + trans[field]) % {'cell' : cell} #apply transformation described in 'trans' dict; '%(cell)s macros allowable'
                            t.append("%s" % cell)
                        except Exception as e:
                            if field in trans.keys():
                                print('Exception while processing \'%(col)s\' column, value = \'%(cell)s\' with message \'%(message)s\'' % {'col' : field, 'cell' : saved_cell, 'message': trans[field]})
                            else:
                                print('Exception while processing \'%(col)s\' column, value = \'%(cell)s\'' % {'col' : field, 'cell' : saved_cell})
                            t.append("%s" % saved_cell)
                else:
                    i = 0
                    while True:
                        try:
                            t.append("%s" % row[i])
                            i += 1
                        except IndexError:
                            break
                result_set += (tuple(t), )
        return result_set