""" Generates data for HIS system testing based on random data (seeded) """
import argparse
import random

from datetime import datetime, timedelta

size = 250000

parser = argparse.ArgumentParser()
parser.add_argument('--sets')
parser.add_argument('--methods')
parser.add_argument('--sites')
parser.add_argument('--sources')
parser.add_argument('--variables')
args = parser.parse_args()

sets = int(args.sets)
methods = int(args.methods)
sites = int(args.sites)
sources = int(args.sources)
variables = int(args.variables)

random.seed(4)

for i in range(0, sets):
    filename = 'Precip_DataValues_{}.csv'.format(i)
    with open(filename, 'w') as datavalues_file:
        datavalues_file.write('SiteCode,VariableCode,DataValue,LocalDateTime,' +
                              'UTCOffset,DateTimeUTC,QualityControlLevelCode,' +
                              'CensorCode,MethodCode,SourceCode\n')

    for j in range(0, size):
        site_code = str(random.randint(1, sites))
        var_code = str(random.randint(1, variables))
        data_value = str(100*random.random())[:8]
        local_dt = datetime(1990, 1, 1) + timedelta(days=random.randint(1, 10000))
        local_dt = local_dt.strftime('%m/%d/%Y')
        utc_offset = '1'
        dt_utc = local_dt
        quality_code = '-9999'
        censor_code = 'nc'
        method_code = str(random.randint(1, methods))
        source_code = str(random.randint(1, sources))
        unquoted_row = [site_code, var_code, data_value, local_dt, utc_offset,
                        dt_utc, quality_code, censor_code, method_code, source_code]
        row = ['"{}"'.format(field) for field in unquoted_row]
        with open(filename, 'a') as datavalues_file:
            datavalues_file.write(','.join(row) + '\n')
