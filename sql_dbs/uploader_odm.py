import argparse
import datetime
import pyodbc
import time

parser = argparse.ArgumentParser()
parser.add_argument('--datavalues')
parser.add_argument('--sites')
args = parser.parse_args()

server = os.environ['GENSERVER']
database = os.environ['GENDB']
username = os.environ['GENUSER']
password = os.environ['GENPASS']
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+
                      server+';PORT=1443;DATABASE='+database+
                      ';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
result_set = [args.datavalues, args.sites]
# First run stored procedure to delete duplicate data values
print('exec spdeleteduplicatesdatavalues')
init_time = time.time()
cursor.execute("exec spdeleteduplicatesdatavalues;")
cursor.commit()
end_time = time.time()
print(end_time-init_time, ' sec')
result_set += [str(end_time-init_time)]
# Second run stored procedure to delete duplicate data values
print('exec spupdateseriescatalog')
init_time = time.time()
cursor.execute("exec spupdateseriescatalog;")
cursor.commit()
end_time = time.time()
print(end_time-init_time, ' sec')
result_set += [str(end_time-init_time) + '\n']

with open('stored-proc.txt', 'a') as f:
    f.write(','.join(result_set))
