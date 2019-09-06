# coding=utf-8

import getopt
import json
import os
import sqlite3
import sys


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

def usage_help():
    print('This is a program that exports sqlite tables to json files')
    print('-i \tinput database file')
    print('-o \toutput dir')
    print('-h \tshow help')

def export_database_data(i_path, o_dir):
    # create export dir
    if not os.path.exists(o_dir):
        os.makedirs(o_dir)
        
    print('input file path: ' + i_path)
    print('output dir path: ' + o_dir)

    # connect to the SQlite databases
    connection = sqlite3.connect(i_path)
    connection.row_factory = dict_factory

    cursor = connection.cursor()

    # select all the tables from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # for each of the bables , select all the records from the table
    for table_name in tables:
        # table_name = table_name[0]
        print('export table name: ' + table_name['name'])

        cursor.execute('SELECT * FROM "%s"' % (table_name['name']))

        # fetch all or one we'll go for all.
        table_data = cursor.fetchall()

        # print(table_data)

        # delete useless key
        useless_key = ('delete_flag', 'restart_time', 'sku', 'summary', 'suspend_time')

        for dic in table_data:
            remove_keys(dic, *useless_key)

        # generate and save JSON files with the table name for each of the database tables
        with open(os.path.join(o_dir, table_name['name'] + '.json'), 'w') as the_file:
            the_file.write(json.dumps(table_data, sort_keys=True, indent=4, separators=(',', ': ')))

    cursor.close()
    connection.close()


if __name__ == '__main__':
    input_file =''
    output_dir = ''
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:")

    for op, value in opts:
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_dir = value
        elif op == "-h":
            usage_help()
            sys.exit()

    if output_dir == '':
        output_dir = os.path.dirname(os.path.abspath(__file__))

    if input_file == '':
        list_file = os.listdir(output_dir)

        # search database file
        f_func = end_width('.db')
        f_file = filter(f_func, list_file)

        # export each database file
        for i in f_file:
            export_database_data(os.path.join(output_dir, i), os.path.join(output_dir, os.path.splitext(i)[0]))

    elif os.path.exists(input_file):
        dirname, filename = os.path.split(input_file)
        export_database_data(input_file, os.path.join(output_dir, filename.split('.',1)[0]))

    else:
        print('input file is not exists')
