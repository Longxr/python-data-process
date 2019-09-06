# coding=utf-8

import json
import os
import sqlite3


def end_width(*suffix):
    # find a specific suffix file
    def end_check(str):
        f = map(str.endswith, suffix)
        return any(f)
    return end_check

def dict_factory(cursor, row):
    # tuple to dict
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def remove_keys(d, *args):
    for key in args:
        if d.__contains__(key):
            del d[key]

def export_database_data(f_dir, f_name):
    # create export dir
    export_dir = os.path.join(os.path.join(f_dir, 'export'), os.path.splitext(f_name)[0])
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # connect to the SQlite databases
    connection = sqlite3.connect(os.path.join(f_dir, f_name))
    connection.row_factory = dict_factory

    cursor = connection.cursor()

    # select all the tables from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # for each of the bables , select all the records from the table
    for table_name in tables:
        # table_name = table_name[0]
        print(table_name['name'])

        cursor.execute('SELECT * FROM "%s"' % (table_name['name']))

        # fetch all or one we'll go for all.
        table_data = cursor.fetchall()

        print(table_data)

        # delete useless key
        useless_key = ('delete_flag', 'restart_time', 'sku', 'summary', 'suspend_time')

        for dic in table_data:
            remove_keys(dic, *useless_key)

        # generate and save JSON files with the table name for each of the database tables
        with open(os.path.join(export_dir, table_name['name'] + '.json'), 'w') as the_file:
            the_file.write(json.dumps(table_data, sort_keys=True, indent=4, separators=(',', ': ')))

    cursor.close()
    connection.close()


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    list_file = os.listdir(root_dir)

    # search database file
    f_func = end_width('.db')
    f_file = filter(f_func, list_file)

    # export each database file
    for i in f_file:
        export_database_data(root_dir, i)
