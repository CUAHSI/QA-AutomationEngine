import argparse
import os
import pyodbc
import time

parser = argparse.ArgumentParser()
parser.add_argument('--datavalues')
parser.add_argument('--sites')
args = parser.parse_args()


def deduplication(cursor):
    print('exec spdeleteduplicatesdatavalues')
    init_time = time.time()
    cursor.execute("exec spdeleteduplicatesdatavalues;")
    cursor.commit()
    end_time = time.time()
    exec_time = str(end_time-init_time)
    print('{} sec'.format(exec_time))
    return exec_time


def seriescatalog(cursor):
    print('exec spupdateseriescatalog')
    init_time = time.time()
    cursor.execute("exec spupdateseriescatalog;")
    cursor.commit()
    end_time = time.time()
    exec_time = str(end_time-init_time)
    print('{} sec'.format(exec_time))
    return exec_time


driver = '{ODBC Driver 13 for SQL Server}'
sql_server = os.environ['GENSERVER']
db_name = os.environ['GENDB']
user = os.environ['GENUSER']
passwd = os.environ['GENPASSWD']
cnxn = pyodbc.connect('DRIVER={};PORT={};'.format(driver, 1433) +
                      'SERVER={};PORT={};'.format(sql_server, 1443) +
                      'DATABASE={};UID={};PWD={};'.format(db_name, user, passwd))
cursor = cnxn.cursor()
deduplication_time = deduplication(cursor)
seriescatalog_time = seriescatalog(cursor)
result = [args.datavalues, args.sites, deduplication_time, seriescatalog_time]

with open('stored-proc.txt', 'a') as f:
    f.write(','.join(result))
